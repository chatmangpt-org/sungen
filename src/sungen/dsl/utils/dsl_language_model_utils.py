import dspy

from sungen.dsl.dsl_pydantic_models import PipelineDSLModel


def _get_language_model_instance(pipeline: PipelineDSLModel, step):
    """
    Get the language model instance for a given step from the top level definition.
    """
    lm_label = step.lm_model
    # Find the lm class within the dspy module. Need to import the class dynamically from the dspy module
    lm_config = next((m for m in pipeline.lm_models if m.label in lm_label), None)

    if lm_config is None:
        raise ValueError(f"Language model with label {lm_label} not found in the pipeline configuration.")

    lm_class = getattr(dspy, lm_config.name)
    lm_inst = lm_class(**lm_config.args)
    return lm_inst