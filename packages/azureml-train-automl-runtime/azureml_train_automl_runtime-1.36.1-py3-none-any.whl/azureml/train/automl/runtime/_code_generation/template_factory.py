# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Optional

from sklearn.pipeline import Pipeline

from .data_featurizer_template import DataFeaturizerTemplate
from .featurizer_template import AbstractFeaturizerTemplate, NoFeaturizerTemplate
from .preprocessor_template import (
    AbstractPreprocessorTemplate,
    NamedPreprocessorTemplate,
    NoPreprocessorTemplate,
    PreprocessorTemplate,
)
from .timeseries_featurizer_template import TimeSeriesFeaturizerTemplate


class FeaturizerTemplateFactory:
    def select_template(self, pipeline: Pipeline, task_type: str) -> AbstractFeaturizerTemplate:
        if DataFeaturizerTemplate.can_handle(pipeline):
            return DataFeaturizerTemplate(pipeline, task_type)
        elif TimeSeriesFeaturizerTemplate.can_handle(pipeline):
            return TimeSeriesFeaturizerTemplate(pipeline)
        elif NoFeaturizerTemplate.can_handle(pipeline):
            return NoFeaturizerTemplate()
        raise NotImplementedError


class PreprocessorTemplateFactory:
    def select_template(self, pipeline: Pipeline, name: Optional[Any] = None) -> AbstractPreprocessorTemplate:
        if name is not None:
            if NamedPreprocessorTemplate.can_handle(pipeline):
                return NamedPreprocessorTemplate(pipeline, name)
        elif PreprocessorTemplate.can_handle(pipeline):
            return PreprocessorTemplate(pipeline)
        if NoPreprocessorTemplate.can_handle(pipeline):
            return NoPreprocessorTemplate()
        raise NotImplementedError


featurizer_template_factory = FeaturizerTemplateFactory()
preprocessor_template_factory = PreprocessorTemplateFactory()
