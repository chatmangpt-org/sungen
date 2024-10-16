import dspy
import pytest
from dspy.utils import DummyLM
from pydantic import BaseModel
from sungen.utils.dspy_tools import PredictType, predict_type, predict_types, init_instant


# Example Pydantic models for testing
class CityModel(BaseModel):
    city: str


class MathModel(BaseModel):
    result: int


# Input data for testing
@pytest.fixture
def input_data_city():
    return {"prompt": "What is the capital of France?"}


@pytest.fixture
def input_data_math():
    return {"prompt": "What is 2 + 2?"}


# Create PredictType instances for testing predict_types
@pytest.fixture
def predict_type_tasks(input_data_city, input_data_math):
    return [
        PredictType(input_data=input_data_city, output_model=CityModel),
        PredictType(input_data=input_data_math, output_model=MathModel),
    ]


# Define a simple gen_instance function (replace your_module.gen_instance)
def gen_instance(model, prompt):
    if model == CityModel:
        # Simulate output based on prompt
        return CityModel(city="Paris")
    elif model == MathModel:
        # Simulate output based on prompt
        return MathModel(result=4)
    else:
        raise ValueError("Unsupported model")


# Test predict_type function with real input and output
def test_predict_type_city(input_data_city):
    # lm = DummyLM(["test output"])
    # dspy.settings.configure(lm=lm)
    init_instant()
    output = predict_type(input_data=input_data_city, output_model=CityModel)

    # Validate the output model and values
    assert isinstance(output, CityModel)
    assert output.city == "Paris"


def test_predict_type_math(input_data_math):
    output = predict_type(input_data=input_data_math, output_model=MathModel)

    # Validate the output model and values
    assert isinstance(output, MathModel)
    assert output.result == 4


# Test predict_types with real concurrent predictions
def test_predict_types(predict_type_tasks):
    # Run the predict_types function
    results = predict_types(type_pairs=predict_type_tasks, max_workers=2)

    # Validate that two results are returned
    assert len(results) == 2

    # Ensure that the results are instances of the expected models
    assert isinstance(results[0], CityModel)
    assert results[0].city == "Paris"

    assert isinstance(results[1], MathModel)
    assert results[1].result == 4


# Test the concurrency behavior of predict_types function
def test_predict_types_concurrency(predict_type_tasks):
    results = predict_types(type_pairs=predict_type_tasks, max_workers=2)

    # Ensure both predictions succeeded concurrently
    assert len(results) == 2

    # Validate the first result corresponds to the CityModel
    assert isinstance(results[0], CityModel)
    assert results[0].city == "Paris"

    # Validate the second result corresponds to the MathModel
    assert isinstance(results[1], MathModel)
    assert results[1].result == 4


# Test predict_types with invalid input, ensure that errors are raised when necessary
def test_predict_types_with_invalid_input():
    invalid_task = PredictType(input_data={"prompt": "Invalid prompt"}, output_model=BaseModel)

    with pytest.raises(ValueError):
        predict_types([invalid_task])
