import inspect
import sys
from typing import Type
from pydantic import BaseModel

from dspygen.experiments.gherkin_gen.gherkin_models import *
from dspygen.utils.dsl_tools import DSLModel

import inspect
from typing import Type, Set, List, Union, get_args, get_origin
from pydantic import BaseModel
from dspygen.utils.dsl_tools import DSLModel


import os

def collect_model_sources(cls, already_seen: Set[Type[BaseModel]] = None) -> str:
    """
    Collects the source code of all classes in the given module that inherit from BaseModel,
    including those referenced in fields, excluding BaseModel and DSLModel.

    Args:
        module: The module to inspect.
        already_seen: A set of models that have already been processed to avoid duplicates.

    Returns:
        A string containing the source code of the relevant classes.
    """
    if already_seen is None:
        already_seen = set()

    source_codes = []

    """
    Recursively walk the inheritance chain and retrieve the source code for all base classes.
    """
    # Get the source code for the current class (this may raise an error if the source isn't available)
    source_code = inspect.getsource(cls)
    print(f"Source of {cls.__name__}:\n")
    print(source_code)

    # If there are base classes, walk through them recursively
    for base in cls.__bases__:
        if base is object:
            continue  # Skip built-in object class
        collect_model_sources(base)




def collect_field_models(field_type, already_seen: Set[Type[BaseModel]], source_codes: List[str]):
    """
    Recursively collect models referenced in fields that are of type BaseModel, List, or Union.

    Args:
        field_type: The type of the field (which may reference another BaseModel).
        already_seen: A set of models that have already been processed to avoid duplicates.
        source_codes: A list of source code strings for the collected models.
    """
    # Handle List[ModelType] or Union[ModelType1, ModelType2]
    origin = get_origin(field_type)  # Get the original type (List, Union, etc.)
    args = get_args(field_type)  # Get the arguments of the List or Union (e.g., List[Step])

    if origin in [list, List]:  # If the field is a List, process the inner type
        list_item_type = args[0]
        if issubclass(list_item_type, BaseModel) and list_item_type not in already_seen:
            collect_model_recursive(list_item_type, already_seen, source_codes)

    elif origin in [Union]:  # If the field is a Union, process each type
        for union_type in args:
            if issubclass(union_type, BaseModel) and union_type not in already_seen:
                collect_model_recursive(union_type, already_seen, source_codes)

    elif isinstance(field_type, type) and issubclass(field_type, BaseModel):  # If it's a single BaseModel type
        if field_type not in already_seen:
            collect_model_recursive(field_type, already_seen, source_codes)


def collect_model_recursive(model: Type[BaseModel], already_seen: Set[Type[BaseModel]], source_codes: List[str]):
    """
    Collect the source code of a model and its related models recursively.

    Args:
        model: The model to collect.
        already_seen: A set of models that have already been processed.
        source_codes: A list of source code strings for the collected models.
    """
    if model in already_seen:
        return

    already_seen.add(model)

    # Collect the source code for this model
    try:
        # Ensure the source file is accessible before getting the source code
        source_file = inspect.getfile(model)
        if os.path.exists(source_file):
            source = inspect.getsource(model)
            source_codes.append(source)
        else:
            print(f"Source file not found for {model.__name__}. Skipping.")
    except Exception as e:
        print(f"Failed to get source for {model.__name__}: {e}")
        return

    # Recursively check the model's fields
    for field_name, field_type in model.__annotations__.items():
        collect_field_models(field_type, already_seen, source_codes)


# Unit test for the collect_model_sources function
def test_collect_model_sources_recursive():
    """
    Test that collect_model_sources recursively collects the source code for all related Gherkin models,
    excluding BaseModel and DSLModel.
    """
    # Call the collect_model_sources function using the mock Gherkin models
    source_code = collect_model_sources(GherkinDocument)

    # Ensure the collected source code includes Step, Scenario, Feature, Tag, Rule, and ScenarioOutline classes
    assert "class Step" in source_code, "Step class source code should be included."
    assert "class Scenario" in source_code, "Scenario class source code should be included."
    assert "class Feature" in source_code, "Feature class source code should be included."
    assert "class Tag" in source_code, "Tag class source code should be included."
    assert "class Rule" in source_code, "Rule class source code should be included."
    assert "class ScenarioOutline" in source_code, "ScenarioOutline class source code should be included."

    # Ensure that DSLModel is excluded
    assert "class DSLModel" not in source_code, "DSLModel class source code should be excluded."

    # Ensure BaseModel is excluded (this would be indirectly tested by DSLModel exclusion)
    assert "class BaseModel" not in source_code, "BaseModel class source code should be excluded."


# Test case for models not inheriting from BaseModel
class NotBaseModelClass:
    pass

class InvalidModels:
    NotBaseModelClass = NotBaseModelClass


def test_collect_model_sources_with_invalid_models():
    """
    Test that collect_model_sources excludes models that do not inherit from BaseModel.
    """
    source_code = collect_model_sources(InvalidModels)

    # Ensure that NotBaseModelClass is not included in the source code
    assert "class NotBaseModelClass" not in source_code, "Classes not inheriting from BaseModel should be excluded."
