import inspect
from typing import Any, Set

from dspygen.experiments.gherkin_gen.gherkin_models import GherkinDocument
from dspygen.utils.dsl_tools import DSLModel


import inspect
from typing import Any, Set

def collect_class_sources(cls: Any, collected_sources: Set[str]) -> None:
    """
    Recursively collect source code for the given class and all related classes
    (based on fields' type annotations) that inherit from DSLModel.
    """
    # Skip if we've already processed this class by its name
    if cls.__name__ in collected_sources:
        return

    # Collect the source code for the class itself
    try:
        source_code = inspect.getsource(cls)
        collected_sources.add(source_code)  # Add the source code as a string, not the class object
    except (TypeError, OSError) as e:
        print(f"Unable to retrieve source for {cls.__name__}: {str(e)}")

    # Now process the fields of the class
    if hasattr(cls, 'model_fields'):  # Pydantic v2
        fields = cls.model_fields
    elif hasattr(cls, '__fields__'):  # Pydantic v1
        fields = cls.__fields__
    else:
        print(f"{cls.__name__} does not appear to be a Pydantic model.")
        return

    # Recursively check if any field annotations are also DSLModel classes
    for field_name, field in fields.items():
        field_type = field.annotation
        if hasattr(field_type, '__bases__') and issubclass(field_type, DSLModel):
            collect_class_sources(field_type, collected_sources)

def collect_all_sources_as_string(cls: Any) -> str:
    """
    Collects the source code for the class and all related DSLModel classes,
    returns them as a single string.
    """
    collected_sources = set()

    # Collect sources starting from the given class
    collect_class_sources(cls, collected_sources)

    # Join all collected source codes into a single string
    return "\n\n".join(collected_sources)



def test_all():
    # Now, let's collect all the fields from the GherkinDocument class:
    all_fields_string = collect_class_sources(GherkinDocument, set())

    # Print the result
    print(all_fields_string)
