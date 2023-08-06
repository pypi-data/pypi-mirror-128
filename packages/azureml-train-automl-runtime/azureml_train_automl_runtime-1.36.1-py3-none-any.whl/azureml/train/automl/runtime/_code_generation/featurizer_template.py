# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import functools
import hashlib
import re
from abc import abstractmethod
from typing import Any, List, cast

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline

from azureml.automl.core import _codegen_utilities
from azureml.automl.runtime.featurization import DataTransformer

from . import utilities
from .constants import FunctionNames
from .pipeline_step_template import NoOpTemplate, PipelineStepTemplate


class AbstractFeaturizerTemplate(PipelineStepTemplate):
    @staticmethod
    @abstractmethod
    def can_handle(obj: Any) -> bool:
        """
        Check whether this template can support this object.

        :param obj: the object to check
        :return: True if this template can handle this object, False otherwise
        """
        raise NotImplementedError

    def get_function_name(self) -> str:
        return FunctionNames.FEATURIZE_FUNC_NAME

    @abstractmethod
    def generate_featurizer_code(self) -> List[str]:
        """
        Generate code for this featurizer using this template.

        May return an empty list.

        :return: a list containing generated code
        """
        raise NotImplementedError


class NoFeaturizerTemplate(AbstractFeaturizerTemplate, NoOpTemplate):
    @staticmethod
    def can_handle(obj: Any) -> bool:
        return isinstance(obj, Pipeline) and not utilities.pipeline_has_featurizer(obj)

    def generate_featurizer_code(self) -> List[str]:
        return []


class IndividualFeaturizerTemplate(AbstractFeaturizerTemplate):
    def __init__(self, featurizer: BaseEstimator) -> None:
        self.featurizer = featurizer
        self._repr = re.sub(r"\s+", "", repr(self.featurizer))

    def _get_step_name(self) -> str:
        return cast(str, self.featurizer.__class__.__name__.lower())

    def _get_hash(self) -> str:
        hash_object = hashlib.sha256(self._repr.encode())
        return hash_object.hexdigest()

    def get_function_name(self) -> str:
        return f"get_{self._get_step_name()}_{self._get_hash()[:6]}"

    def __repr__(self) -> str:
        return self.get_function_name()

    def __hash__(self) -> int:
        return hash(self._repr)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self._repr == other._repr

    @staticmethod
    def can_handle(obj: Any) -> bool:
        return isinstance(obj, BaseEstimator)

    def generate_featurizer_code(self) -> List[str]:
        imports = set(_codegen_utilities.get_recursive_imports(self.featurizer))
        imports.update(_codegen_utilities.get_recursive_imports(self.featurizer.get_params()))

        # Hack for CountVectorizer
        if "DataTransformer._wrap_in_lst" in repr(self.featurizer):
            imports.add(_codegen_utilities.get_import(DataTransformer))

        output = [f"def {self.get_function_name()}():"]
        output.extend(_codegen_utilities.generate_import_statements(imports))
        output.append("")
        output.append(f"featurizer = {self.featurizer}")
        output.append("")
        output.append("return featurizer")
        output.append("\n")
        return _codegen_utilities.indent_function_lines(output)
