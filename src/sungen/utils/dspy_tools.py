from typing import TypeVar, Type

import dspy

from sungen.utils.str_tools import pythonic_str

GPT_DEFAULT_MODEL = "gpt-4o-mini"


def init_dspy(model: str = GPT_DEFAULT_MODEL,
              lm_class=dspy.OpenAI,
              max_tokens: int = 800,
              lm_instance=None,
              api_key=None,
              temperature=0.6,
              experimental=True):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance
    else:
        lm = lm_class(max_tokens=max_tokens, model=model, api_key=api_key, temperature=temperature)
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm


def init_ol(model: str = "qwen2:instruct",
            base_url="http://localhost:11434",
            max_tokens: int = 2000,
            lm_instance=None,
            lm_class=dspy.OllamaLocal,
            timeout=100,
            temperature=0.6,
            experimental=True):
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance
    else:
        lm = lm_class(model=model, base_url=base_url, max_tokens=max_tokens, timeout_s=timeout, temperature=temperature)
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm

# typed_predictors_tools.py

from dspy import TypedPredictor, InputField, OutputField, Signature
from pydantic import BaseModel as PydanticBaseModel, create_model


# Define a type variable for the output model
T = TypeVar('T', bound=PydanticBaseModel)

def predict_type(input_data: dict, output_model: Type[T]) -> T:
    """
    Generic function to generate context parts using TypedPredictor.

    Args:
        input_data (dict): A dictionary containing input data.
        output_model (Type[T]): The output model type (a Pydantic model).

    Returns:
        T: The predicted output as an instance of the output model.
    """

    # Dynamically create the input model using Pydantic's `create_model` function
    InputModel = create_model('InputModel', **{key: (type(value), ...) for key, value in input_data.items()})

    # Create a new Signature class dynamically
    class DynamicSignature(Signature):
        input: InputModel = InputField()
        output: output_model = OutputField()

    # Initialize the TypedPredictor with the dynamic signature
    predictor = TypedPredictor(DynamicSignature)

    # Convert input data to the Input model instance
    input_instance = InputModel(**input_data)

    # Perform prediction
    prediction = predictor(input=input_instance)

    # Retrieve and return the predicted output as an instance of the output model
    return prediction.output



