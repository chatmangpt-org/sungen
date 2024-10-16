"""
Module for leveraging DSPy Typed Predictors with Pydantic models to enforce input-output type constraints.
This module provides utilities for initializing and optimizing language models, generating context-based predictions,
and running typed prediction tasks concurrently using custom input-output models.

The core functionality revolves around TypedPredictors and ChainOfThought Predictors, enabling users to enforce
type safety on the inputs and outputs of prediction pipelines.

Additionally, this module supports concurrent execution of multiple typed prediction tasks, optimized with a
thread pool, and includes dynamic input model generation based on input data structures.
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from typing import TypeVar, Type, Generic, List, Optional
# typed_predictors_tools.py

from pydantic import BaseModel, create_model

import dspy


GPT_DEFAULT_MODEL = "gpt-4o-mini"

# Define a type variable for the output model
T = TypeVar('T', bound=BaseModel)


class PredictType:
    """
    Represents a single prediction task.

    Attributes:
        input_data (dict): The input data for the prediction.
        output_model (Type[T]): The Pydantic model to use for the prediction output.
    """
    input_data: dict
    output_model: Type[T]


def init_dspy(model: str = GPT_DEFAULT_MODEL,
              lm_class=dspy.OpenAI,
              max_tokens: int = 800,
              lm_instance=None,
              api_key=None,
              temperature=0.6,
              experimental=True):
    """
    Initialize and configure a DSPy language model.

    This function initializes a DSPy language model instance using the specified model, token limits, temperature
    settings, and other parameters. It also allows you to provide an existing language model instance for configuration
    or create a new one.

    :param model: The name of the model to use (default: "gpt-4o-mini").
    :param lm_class: The class of the language model to initialize (default: `dspy.OpenAI`).
    :param max_tokens: Maximum number of tokens to use in each prediction (default: 800).
    :param lm_instance: Optional, an existing instance of the language model to configure. If provided, a new instance
                        will not be created.
    :param api_key: Optional, an API key for the language model service (if required).
    :param temperature: The temperature setting for controlling randomness in predictions (default: 0.6).
    :param experimental: A flag to enable experimental settings in DSPy (default: True).

    :returns: The configured language model instance.
    :rtype: `dspy.LM`
    """
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance
    else:
        lm = lm_class(max_tokens=max_tokens, model=model, api_key=api_key, temperature=temperature)
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm


def init_ol(model: str = "qwen2",
            base_url="http://localhost:11434",
            max_tokens: int = 2000,
            lm_instance=None,
            lm_class=dspy.OllamaLocal,
            timeout=100,
            temperature=0.6,
            experimental=True):
    """
    Initialize and configure a local Ollama language model for DSPy predictions.

    This function sets up a local Ollama language model instance, providing control over the model configuration and parameters such as API URL, timeout, token limit, and temperature settings. It can also configure an existing instance if provided.

    :param model: The name of the local Ollama model to use (default: "qwen2").
    :param base_url: The URL for the local Ollama API (default: "http://localhost:11434").
    :param max_tokens: Maximum number of tokens allowed in a single prediction (default: 2000).
    :param lm_instance: Optional, an existing Ollama model instance to configure.
    :param lm_class: The class to use for the local language model (default: `dspy.OllamaLocal`).
    :param timeout: Timeout in seconds for API requests (default: 100).
    :param temperature: The temperature setting for randomness in predictions (default: 0.6).
    :param experimental: A flag to enable experimental settings in DSPy (default: True).

    :returns: The configured Ollama language model instance.
    :rtype: `dspy.LM`
    """
    raise NotImplementedError("This function is obsolete and should not be used.")
    # if lm_instance:
    #     dspy.settings.configure(lm=lm_instance, experimental=experimental)
        # return lm_instance
    # else:
    #     lm = lm_class(model=model, base_url=base_url, max_tokens=max_tokens, timeout_s=timeout, temperature=temperature)
    #     dspy.settings.configure(lm=lm, experimental=experimental)
    #     return lm


class PredictType(BaseModel, Generic[T]):
    """
    Represents a single prediction task.

    Attributes:
        input_data (dict): The input data for the prediction.
        output_model (Type[T]): The Pydantic model to use for the prediction output.
    """
    input_data: dict
    output_model: Type[T]


def predict_type(input_data: dict, output_model: Type[T]) -> T:
    """
    Generate a prediction using GenPydanticInstance with dynamic input-output models.

    This function dynamically creates an input model based on the provided input data, initializes a GenPydanticInstance,
    and generates a prediction that adheres to the output model's type constraints.

    :param input_data: A dictionary containing the input data for the prediction.
    :param output_model: The output model type, a Pydantic model class, to enforce type constraints on the output.

    :returns: The predicted output as an instance of the output model.
    :rtype: T
    """
    # Create an instance of GenPydanticInstance
    from sungen.dspy_modules.gen_pydantic_instance import gen_instance
    model_instance = gen_instance(output_model, prompt=input_data)

    # Return the generated model instance
    return model_instance


def predict_types(type_pairs: List[PredictType], max_workers=5) -> List[BaseModel]:
    """
    Execute a list of typed prediction tasks concurrently while preserving input order.

    This function accepts a list of PredictType tasks, runs them concurrently using a thread pool, and returns
    their prediction results in the same order as the input list.

    :param type_pairs: A list of PredictType instances representing individual prediction tasks.
                       Each task contains input data and the output model.

    :returns: A list of prediction results as instances of the respective output models, in the same order as input.
    :rtype: List[BaseModel]

    :raises Exception: If any prediction task fails, it logs the error and raises an exception.
    """
    results = []

    # Initialize logging
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO)

    def run_prediction(index: int, task: PredictType) -> (int, BaseModel):
        """
        Runs a single prediction task.

        Args:
            index (int): The index of the task in the original list.
            task (PredictType): The prediction task to execute.

        Returns:
            Tuple[int, BaseModel]: A tuple containing the index and the result of the prediction.
        """
        try:
            # Log the prediction start
            logger.debug(f"Starting prediction with input: {task.input_data} using model: {task.output_model.__name__}")

            # Execute the prediction
            prediction = predict_type(task.input_data, task.output_model)

            # Log the successful prediction
            logger.debug(f"Prediction successful for task at index {index}: {prediction}")

            return index, prediction
        except Exception as e:
            # Log the exception with input data for context
            logger.error(f"Prediction failed for task at index {index} with input {task.input_data}: {e}")
            raise

    # Use ThreadPoolExecutor to run predictions concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all prediction tasks to the executor with their index
        future_to_task = {executor.submit(run_prediction, i, task): i for i, task in enumerate(type_pairs)}

        # Iterate over the futures as they complete and store the results
        for future in as_completed(future_to_task):
            try:
                index, result = future.result()  # Retrieve the result and its index
                results.append((index, result))  # Store the result with its index
                logger.info(f"Prediction succeeded for task at index {index}")
            except Exception as e:
                index = future_to_task[future]
                logger.error(f"Prediction failed for task at index {index} with error: {e}")

    # Sort results by the original task index and return only the predictions (discard the index)
    results.sort(key=lambda x: x[0])
    return [result for _, result in results]


def init_lm(model: str = "openai/gpt-4o-mini",
            api_key: Optional[str] = None,
            api_base: Optional[str] = None,
            temperature: float = 0.0,
            max_tokens: int = 1000,
            cache: bool = True,
            model_type: Optional[str] = "text",
            stop: Optional[list] = None,
            experimental: bool = True) -> dspy.LM:
    """
    Initialize a language model using the new DSPy 2.5 setup.

    Args:
        model (str): Model name, with support for openai/ prefixed endpoints (default: 'openai/gpt-4o-mini').
        model_type (Optional[str]): Specify the model type, such as 'text' for text-based predictions (default: None).
        api_key (Optional[str]): Optional API key for authentication, if required.
        api_base (Optional[str]): Optional API base URL for specific LMs (e.g., localhost setups).
        temperature (float): Temperature for controlling randomness in the model's predictions (default: 0.7).
        max_tokens (int): Maximum number of tokens to allow for a single prediction (default: 1000).
        cache (bool): Whether to cache results from the LM (default: False).
        model_type (Optional[str]): Specify the model type, such as 'text' for text-based predictions (default: None).
        stop (Optional[list]): Tokens or strings to stop generating at (default: None).
        adapter (Optional[dspy.ChatAdapter]): DSPy Adapter to manage input/output formatting (default: None).
        experimental (bool): Enable experimental DSPy settings for the LM (default: True).

    Returns:
        dspy.LM: Configured LM object.
    """
    # Initialize the LM with flexible configuration options
    if model == "openai/gpt-4o-mini":
        lm = dspy.LM('openai/gpt-4o-mini')
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm

    lm = dspy.LM(model=model)

    # Configure the LM with DSPy settings
    dspy.settings.configure(lm=lm, adapter=None, experimental=experimental)

    return lm


def init_instant():
    """Initialize the instant version of the model."""
    return init_lm("groq/llama-3.1-8b-instant", model_type="chat", max_tokens=8000)


def init_versatile():
    """Initialize the versatile version of the model."""
    return init_lm("groq/llama-3.1-70b-versatile", model_type="chat", max_tokens=8000)


def init_text():
    """Initialize the text preview version of the model."""
    return init_lm("groq/llama-3.2-90b-text-preview", model_type="chat", max_tokens=8000)


def main():
    """Main function"""
    init_dspy()


if __name__ == '__main__':
    main()
