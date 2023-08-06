# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import itertools
from collections import defaultdict
from typing import DefaultDict, List, Mapping, Tuple, Union, cast

from sklearn.pipeline import Pipeline
from sklearn_pandas import DataFrameMapper
from sklearn_pandas.pipeline import TransformerPipeline

from azureml.automl.core import _codegen_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.runtime.featurization import DataTransformer
from azureml.automl.runtime.featurization.transformer_and_mapper import TransformerAndMapper

from .constants import FunctionNames
from .featurizer_template import AbstractFeaturizerTemplate, IndividualFeaturizerTemplate

FeatureType = Tuple[Union[str, List[str]], Pipeline, Mapping[str, object]]


class DataFeaturizerTemplate(AbstractFeaturizerTemplate):
    def __init__(self, pipeline: Pipeline, task_type: str) -> None:
        Contract.assert_true(
            self.can_handle(pipeline), "A pipeline without DataTransformer was provided.", log_safe=True
        )
        self.featurizer = cast(DataTransformer, pipeline.steps[0][1])
        self.task_type = task_type

    @staticmethod
    def can_handle(obj: Pipeline) -> bool:
        return isinstance(obj, Pipeline) and len(obj.steps) > 1 and isinstance(obj.steps[0][1], DataTransformer)

    def _get_step_name(self) -> str:
        return "dt"

    def generate_featurizer_code(self) -> List[str]:
        transformer_and_mapper_list = self.featurizer.transformer_and_mapper_list
        output = [f"def {FunctionNames.FEATURIZE_FUNC_NAME}():"]

        imports = {
            _codegen_utilities.get_import(DataFrameMapper),
            _codegen_utilities.get_import(DataTransformer),
            _codegen_utilities.get_import(TransformerAndMapper),
        }

        individual_featurizer_templates = defaultdict(int)  # type: DefaultDict[IndividualFeaturizerTemplate, int]

        output.extend(_codegen_utilities.generate_import_statements(imports))
        output.append("")

        output.append("transformer_and_mapper_list = []")

        if transformer_and_mapper_list is not None:
            for i, trm in enumerate(transformer_and_mapper_list):
                i += 1
                tr_str = f"transformer{i}"

                # Use a function placeholder in place of the default repr() output
                # The general idea: we want to deduplicate featurizers without modifying the source object.
                # Therefore, we can intercept the repr() calls for TransformerPipeline/Pipeline
                # at the first level, keep a reference to this pipeline, and in the meantime return a placeholder.
                # We need to swap the repr() implementation back to the old one inside this new implementation because
                # the IndividualFeaturizerTemplate needs to store the full representation of the pipeline.
                def use_function_placeholder(obj):
                    with _codegen_utilities.use_custom_repr(cls=Pipeline, func=cached):
                        template = IndividualFeaturizerTemplate(obj)
                        individual_featurizer_templates[template] += 1
                        return f"{template.get_function_name()}()"

                with _codegen_utilities.use_custom_repr(cls=Pipeline, func=use_function_placeholder) as cached:
                    output.append(f"{tr_str} = {trm.mapper.features}")

                params = {"input_df": trm.mapper.input_df, "sparse": trm.mapper.sparse}
                repr_str = _codegen_utilities.generate_repr_str(DataFrameMapper, params, features=tr_str)
                output.append(f"mapper{i} = {repr_str}")
                output.append(f"tm{i} = TransformerAndMapper(transformers={tr_str}, mapper=mapper{i})")
                output.append(f"transformer_and_mapper_list.append(tm{i})")
                output.append("")

        output.append(f"dt = DataTransformer(task='{self.task_type}')")
        output.append("dt.transformer_and_mapper_list = transformer_and_mapper_list")

        # TODO: Have a better way to set this without this hack (#1277252)
        #  Right now, we just dump the class and it results in a massive blob of unreadable bytestrings.
        #  Also problematic if the user changes the list of featurizers.
        output.append("dt._engineered_feature_names_class = None")
        output.append("")
        output.append("return dt")
        output.append("\n")

        output = "\n".join(output).split("\n")
        output = _codegen_utilities.indent_function_lines(output)

        # Generate code for each featurizer, then flatten it and prepend it to the output
        featurizer_funcs = [template.generate_featurizer_code() for template in individual_featurizer_templates.keys()]
        return list(itertools.chain.from_iterable([*featurizer_funcs, output]))
