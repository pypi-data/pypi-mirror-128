"""
/predict request body JSON example:

    {
        "inputs": [
            {
                "identifier": "foo",
                "features": {
                    "age": 20,
                    "height": 180
                }
            },
            {
                "identifier": "bar",
                "features": {
                    "age": 30,
                    "height": 200
                }
            },
            {
                "identifier": "foo",
                "features": {
                    "age": 20,
                    "height": 180
                }
            }
        ]
    }

"""
import json
import time
from enum import Enum
from functools import cached_property
from typing import Any, Dict, List, Tuple

import pandas as pd
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from pydantic import BaseModel, create_model

from energinetml.core.model import Model, TrainedModel

tracer = trace.get_tracer(__name__)


class PredictionInput(list):
    """[summary]"""

    def __init__(self, features: List[str], *args, **kwargs):
        """[summary]

        Args:
            features (List[str]): [description]
        """
        super().__init__(*args, **kwargs)
        self.features = features

    def as_dict_of_lists(self) -> Dict[str, Any]:
        """[summary]"""
        return {
            feature: [input[feature] for input in self] for feature in self.features
        }

    def as_pandas_dataframe(self) -> pd.DataFrame:
        """[summary]

        Raises:
            RuntimeError: [description]

        Returns:
            pd.DataFram: [description]
        """

        return pd.DataFrame(self.as_dict_of_lists())


# -- Data models -------------------------------------------------------------


class PredictRequest(BaseModel):
    """[summary]"""

    inputs: List[Any]

    def group_input_by_identifier(self):
        """[summary]

        Returns:
            [type]: TODO: I need help for this data structure.
        """
        inputs_per_identifier = {}

        for index, input in enumerate(self.inputs):
            if hasattr(input, "identifier"):
                identifier = input.identifier.value
            else:
                identifier = None

            inputs_per_identifier.setdefault(identifier, []).append(
                (index, dict(input.features))
            )

        return inputs_per_identifier.items()


class PredictResponse(BaseModel):
    """[summary]"""

    predictions: List[Any]


# -- Controller --------------------------------------------------------------


class PredictionController:
    """[summary]"""

    def __init__(
        self,
        model: Model,
        trained_model: TrainedModel,
        model_version: str = None,
    ):
        """[summary]

        Args:
            model (Model): [description]
            trained_model (TrainedModel): [description]
            model_version (str, optional): [description]. Defaults to None.
        """
        self.model = model
        self.trained_model = trained_model
        self.model_version = model_version

    @property
    def identifiers(self) -> List[str]:
        """[summary]

        Returns:
            List[str]: [description]
        """
        return self.trained_model.identifiers

    @property
    def features(self) -> List[str]:
        """[summary]

        Returns:
            List[str]: [description]
        """
        return self.trained_model.features

    @property
    def requires_identity(self) -> bool:
        """[summary]

        Returns:
            bool: [description]
        """
        return not self.trained_model.has_default_model()

    @cached_property
    def request_model(self):
        """
        Build a request model class (inherited from pydantic.BaseModel)
        based on a specific TrainedModel instance. The resulting model
        can be used for JSON input validation, Swagger docs etc.
        """
        predict_features = create_model(
            "PredictFeatures", **{feature: (Any, ...) for feature in self.features}
        )

        predict_input_attributes = {"features": (predict_features, ...)}

        if self.requires_identity:
            identifier_enum = Enum("IdentifierEnum", {i: i for i in self.identifiers})
            predict_input_attributes["identifier"] = (identifier_enum, ...)

        PredictInput = create_model(
            __model_name="PredictInput", **predict_input_attributes
        )

        return create_model(
            __model_name="PredictRequest",
            __base__=PredictRequest,
            inputs=(List[PredictInput], ...),
        )

    @property
    def response_model(self):
        """[summary]"""
        return PredictResponse

    def predict(
        self, request: PredictRequest, correlation_id: str = None
    ) -> PredictResponse:
        """[summary]

        Args:
            request (PredictRequest): [description]
            correlation_id (str, optional): [description]. Defaults to None.

        Returns:
            PredictResponse: [description]
        """
        start_span = tracer.start_span(name="prediction", kind=SpanKind.SERVER)

        with start_span as span:
            start = time.perf_counter()
            identifiers, features, predictions = self.invoke_model(request)
            end = time.perf_counter()

            if correlation_id:
                span.set_attribute("correlation_id", correlation_id)
            span.set_attribute("duration_model", str(end - start))
            span.set_attribute("model_name", self.model.name)
            if self.model_version is not None:
                span.set_attribute("model_version", self.model_version)
            span.set_attribute("identifiers", json.dumps(identifiers))
            span.set_attribute("features", json.dumps(features))
            span.set_attribute("predictions", json.dumps(predictions))

        return self.response_model(predictions=predictions)

    def invoke_model(
        self, request: PredictRequest
    ) -> Tuple[List[str], List[str], List[Any]]:
        """[summary]

        Args:
            request (PredictRequest): [description]

        Raises:
            RuntimeError: [description]

        Returns:
            PredictResponse: [description]
        """
        groups = list(request.group_input_by_identifier())
        identifiers_ordered = [... for _ in range(len(request.inputs))]
        features_ordered = [i for i in request.inputs]
        predictions_ordered = [... for _ in range(len(request.inputs))]

        # Invoke predict() for each unique identifier
        for identifier, inputs in groups:
            indexes = [i[0] for i in inputs]
            feature_sets = [i[1] for i in inputs]
            input_data = PredictionInput(self.features, feature_sets)

            predict_result = self.model.predict(
                trained_model=self.trained_model,
                identifier=identifier,
                input_data=input_data,
            )

            # TODO Verify predict_result?

            for index, features, prediction in zip(
                indexes, feature_sets, predict_result
            ):
                identifiers_ordered[index] = identifier
                features_ordered[index] = features
                predictions_ordered[index] = prediction

        if ... in predictions_ordered:
            # TODO Raise...
            raise RuntimeError()

        return (identifiers_ordered, features_ordered, predictions_ordered)
