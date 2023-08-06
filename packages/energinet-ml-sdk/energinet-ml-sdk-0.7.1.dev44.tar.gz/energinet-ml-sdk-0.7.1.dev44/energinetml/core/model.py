#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]"""

import importlib
import inspect
import os
import pickle
import random
import shutil
import sys
from dataclasses import dataclass, field
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    ContextManager,
    Dict,
    Iterable,
    List,
    Tuple,
    Union,
)

from energinetml.azure.datasets import MLDataStore
from energinetml.core.configurable import Configurable
from energinetml.core.files import FileMatcher, temporary_folder
from energinetml.core.logger import MetricsLogger
from energinetml.core.project import MachineLearningProject
from energinetml.core.requirements import RequirementList
from energinetml.settings import EMPTY_MODEL_TEMPLATE_DIR

if TYPE_CHECKING:
    from energinetml.core.predicting import PredictionInput

# Constants
# TODO Move to settings.py?
REQUIREMENTS_FILE_NAME = "requirements.txt"
DEFAULT_FILES_INCLUDE = ["**/*.py", "model.json", REQUIREMENTS_FILE_NAME]
DEFAULT_FILES_EXCLUDE = []


@dataclass
class Model(Configurable):
    """[summary]"""

    name: str
    experiment: str
    compute_target: str
    vm_size: str
    datasets: List[str] = field(default_factory=list)
    datasets_local: List[str] = field(default_factory=list)
    datasets_cloud: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    parameters_local: Dict[str, Any] = field(default_factory=dict)
    parameters_cloud: Dict[str, Any] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    files_include: List[str] = field(default_factory=list)
    files_exclude: List[str] = field(default_factory=list)

    # Constants
    CONFIG_FILE_NAME = "model.json"
    SCRIPT_FILE_NAME = "model.py"
    TRAINED_MODEL_FILE_NAME = "model.pkl"
    REQUIREMENTS_FILE_NAME = REQUIREMENTS_FILE_NAME

    @classmethod
    def create(cls, *args: Any, **kwargs: Dict[str, Any]) -> "Model":
        """[summary]

        Returns:
            Model: [description]
        """
        model = super().create(*args, **kwargs)

        # Copy template files
        for filename in os.listdir(EMPTY_MODEL_TEMPLATE_DIR):
            src = os.path.join(EMPTY_MODEL_TEMPLATE_DIR, filename)
            dst = os.path.join(model.path, filename)
            if os.path.isfile(src):
                shutil.copyfile(src, dst)

        return model

    @cached_property
    def project(self) -> Union[MachineLearningProject, None]:
        """Returns the Project which this model belongs to.

        Returns:
            Union[MachineLearningProject, None]: [description]
        """

        try:
            return MachineLearningProject.from_directory(self.path)
        except MachineLearningProject.NotFound:
            return None

    @cached_property
    def datasets_parsed(self) -> "ModelDatasets":
        """[summary]

        Returns:
            ModelDatasets: [description]
        """
        return ModelDatasets(self)

    @property
    def trained_model_path(self) -> str:
        """Returns path to the trained model.

        Returns:
            str: [description]
        """
        return self.get_file_path("outputs", self.TRAINED_MODEL_FILE_NAME)

    @property
    def data_folder_path(self) -> str:
        """Returns path to the data folder.

        Returns:
            str: [description]
        """
        return self.get_file_path("data")

    @property
    def requirements_file_path(self) -> str:
        """Absolute path to requirements.txt file.

        Returns:
            str: [description]
        """
        return self.get_file_path(self.REQUIREMENTS_FILE_NAME)

    @cached_property
    def requirements(self) -> RequirementList:
        """[summary]

        Returns:
            RequirementList: [description]
        """
        if os.path.isfile(self.requirements_file_path):
            return RequirementList.from_file(self.requirements_file_path)
        elif self.project:
            return self.project.requirements
        else:
            return RequirementList()

    @property
    def files(self) -> FileMatcher:
        """Returns an iterable of files to include when submitting a model to
        the cloud. These are the files necessary to run training in the cloud.

        File paths are relative to model root.

        NB: Does NOT include requirements.txt !!!

        Returns:
            FileMatcher: [description]
        """
        return FileMatcher(
            root_path=self.path,
            include=self.files_include,
            exclude=self.files_exclude,
            recursive=True,
        )

    def temporary_folder(
        self, include_trained_model: bool = False
    ) -> ContextManager[None]:
        """Returns a context manager which creates a temporary folder on the
        filesystem and copies all model's files into the folder including
        the project's requirements.txt file (if it exists).

        Usage example:

            with model.temporary_folder() as temp_path:
                # files are available in temp_path

        Args:
            include_trained_model (bool, optional): [description]. Defaults to False.

        Returns:
                ContextManager[str]: [description]
        """
        files_to_copy = []

        # Model-specific files (relative to model root)
        for relative_path in self.files:
            files_to_copy.append((self.get_file_path(relative_path), relative_path))

        # Trained model (model.pkl) if necessary
        if include_trained_model:
            files_to_copy.append(
                (
                    self.trained_model_path,
                    self.get_relative_file_path(self.trained_model_path),
                )
            )

        # requirements.txt from this folder or project folder
        if os.path.isfile(self.requirements_file_path):
            files_to_copy.append(
                (self.requirements_file_path, self.REQUIREMENTS_FILE_NAME)
            )
        elif self.project and os.path.isfile(self.project.requirements_file_path):
            files_to_copy.append(
                (self.project.requirements_file_path, self.REQUIREMENTS_FILE_NAME)
            )

        return temporary_folder(files_to_copy)

    # -- Partially abstract interface ----------------------------------------

    # The following methods are meant to be overwritten by inherited classes
    # if necessary. Some can be omitted, and will return default values.

    def extra_tags(self) -> Dict[str, Any]:
        """[summary]

        Returns:
            Dict[str, Any]: [description]
        """
        return {}

    def generate_seed(self) -> int:
        """[summary]

        Returns:
            int: [description]
        """
        return random.randint(0, 10 ** 9)

    def train(
        self,
        datasets: MLDataStore,
        logger: MetricsLogger,
        seed: int,
        **params: Dict[str, Any],
    ) -> None:
        """Define your training logic.

        Args:
            datasets (MLDataStore): A reference to the data set.
            logger (MetricsLogger): The logger argument handle metric logging, etc.
            seed (typing.Any): The seed argument tries to obtain a deterministic
            environment for model experiments.

        Raises:
            NotImplementedError: You need to implement the training logic.
        """
        raise NotImplementedError

    def predict(
        self,
        trained_model: "TrainedModel",
        input_data: "PredictionInput",
        identifier: str,
    ) -> None:
        """Define your prediction logic.

        Args:
            trained_model (TrainedModel): Your trained model object.
            input_data (PredictionInput): Data used for inference.
            identifier (str): A unique identifier which refers to a specific model in
            the model obejct.

        Raises:
            NotImplementedError: You need to implement the prediction logic.
        """
        raise NotImplementedError


class ModelDatasets:
    """
    A wrapper for parsing datasets in string-format to specific
    name and version. Distinguishes between datasets for local
    and cloud training.
    """

    def __init__(self, model: Model):
        """[summary]

        Args:
            model (Model): [description]
        """
        self.model = model

    def _parse_datasets(self, datasets: List[str]) -> Iterable[Tuple[str, str]]:
        """Parses datasets in the format of either "name" or "name:version"
        and returns an iterable of (name, version), where version is
        optional and can be None.

        Args:
            datasets (List[str]): [description]

        Raises:
            ValueError: [description]

        Returns:
            Iterable[Tuple[str, str]]: [description]

        Yields:
            Iterator[Iterable[Tuple[str, str]]]: [description]
        """
        for dataset in datasets:
            if dataset.count(":") > 1:
                raise ValueError(f"Invalid dataset '{dataset}'")
            colon_at = dataset.find(":")
            if colon_at != -1:
                yield dataset[:colon_at], dataset[colon_at + 1 :]
            else:
                yield dataset, None

    @property
    def local(self) -> List[Tuple[str, str]]:
        """[summary]

        Returns:
            List[Tuple[str, str]]: [description]
        """
        all_ = self._parse_datasets(self.model.datasets)
        local = self._parse_datasets(self.model.datasets_local)
        return list(all_) + list(local)

    @property
    def cloud(self) -> List[Tuple[str, str]]:
        """[summary]

        Returns:
            List[Tuple[str, str]]: [description]
        """
        all_ = self._parse_datasets(self.model.datasets)
        cloud = self._parse_datasets(self.model.datasets_cloud)
        return list(all_) + list(cloud)


@dataclass
class TrainedModel:
    """[summary]"""

    # TODO: Simon will look into the field typing
    model: Any = field(default=None)
    models: Dict[str, Any] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)

    class Invalid(Exception):
        """[summary]"""

        pass

    def __new__(cls, **kwargs):
        """[summary]"""
        if "model" in kwargs and "models" in kwargs:
            raise ValueError(
                (
                    f"Can not instantiate {cls.__name__} using both 'model' and "
                    "'models' parameters. "
                    "Either provide a default model to the 'model' "
                    "parameter, or provide a series of identifiable models "
                    "to the 'models' parameter."
                )
            )
        return object.__new__(cls)

    @property
    def identifiers(self) -> List[str]:
        """[summary]

        Returns:
            List[str]: [description]
        """
        return list(self.models.keys())

    def has_model(self, identifier) -> bool:
        """[summary]

        Args:
            identifier ([type]): [description]

        Returns:
            bool: [description]
        """
        return identifier in self.models

    def get_model(self, identifier: str = None):
        """[summary]

        Args:
            identifier (str, optional): [description]. Defaults to None.

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        if identifier is None:
            return self.get_default_model()
        elif identifier in self.models:
            return self.models[identifier]
        else:
            raise ValueError(f"No model exists with identifier: {identifier}")

    def has_default_model(self) -> bool:
        """[summary]

        Returns:
            bool: [description]
        """
        return self.model is not None

    def get_default_model(self):
        """
        :rtype: object
        """
        if not self.has_default_model():
            raise ValueError(
                "No default model exists for this model. "
                "Use get_model() instead and provide a model identifier."
            )
        return self.model

    def verify(self):
        """
        TODO move to function outside class?
        """
        if not isinstance(self.features, list):
            features_type = str(type(self.features))
            raise self.Invalid(
                "Must provide a list of features. "
                f"You gave me something of type {features_type}"
            )
        if not all(isinstance(s, str) for s in self.features):
            raise self.Invalid("All features must be of type str")
        if not [f.strip() for f in self.features if f.strip()]:
            raise self.Invalid(
                (
                    "No feature names provided. "
                    f"Instantiate {self.__class__.__name__} with a list "
                    "of features using the 'features' parameter."
                )
            )

    def dump(self, file_path: str) -> None:
        """[summary]

        Args:
            file_path (str): [description]
        """
        folder = os.path.split(file_path)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, fp: str) -> "TrainedModel":
        """[summary]

        Args:
            fp (str): [description]

        Raises:
            cls.Invalid: [description]

        Returns:
            TrainedModel: [description]
        """
        with open(fp, "rb") as f:
            try:
                loaded_model = pickle.load(f)

                if not isinstance(loaded_model, cls):
                    raise cls.Invalid(
                        f"The file at {fp} does not contain a {cls.__name__} object."
                    )

                loaded_model.verify()

                return loaded_model
            except pickle.UnpicklingError:
                raise cls.Invalid()


# -- Model importing ---------------------------------------------------------


class ModelError(Exception):
    """[summary]"""

    pass


class ModelImportError(ModelError):
    """
    Raised if script does not contain a 'model' object
    in the global scope.
    """

    pass


class ModelNotClassError(ModelError):
    """
    Raised if imported 'model' object is not a class type.
    """

    pass


class ModelNotInheritModel(ModelError):
    """
    Raised if imported 'model' does not inherit from Model.
    """

    pass


def import_model_class(path):
    """
    Imports 'model' object from python-module at 'path'.
    Validates that its a class, and that it inherits from Model.

    Args:
        path (str): [description]

    Raises:
        ModelImportError: [description]
        ModelNotClassError: [description]
        ModelNotInheritModel: [description]

    Returns:
        Model: [description]
    """
    module_dir, module_name = os.path.split(os.path.normpath(path))
    if module_dir not in sys.path:
        sys.path.append(module_dir)

    module = importlib.import_module(module_name)

    if not hasattr(module, "model"):
        raise ModelImportError()

    sys.modules["model"] = module

    model_class = getattr(module, "model")

    if not inspect.isclass(model_class):
        raise ModelNotClassError()
    if not issubclass(model_class, Model):
        raise ModelNotInheritModel()

    return model_class
