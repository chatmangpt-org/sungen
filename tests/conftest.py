import os
import sys


def docstring_to_feature_file(module):
    """
    Convert the module-level docstring to a .feature file.

    :param module: The module object to extract the docstring from.
    :return: The path to the created .feature file.
    """
    # Get the module-level docstring
    feature_description = module.__doc__

    if not feature_description:
        raise ValueError("The module does not have a docstring containing the feature description.")

    # Determine the feature file path based on the module file
    feature_file_path = os.path.splitext(module.__file__)[0] + ".feature"

    # Write the feature description to the feature file
    with open(feature_file_path, "w") as feature_file:
        feature_file.write(feature_description)

    return feature_file_path


def scenario_path(module_name):
    """
    Wrapper for pytest-bdd scenarios to use the correct feature file.

    :param module_name: The module name to extract the docstring from.
    """
    # Get the module object from sys.modules
    module = sys.modules[module_name]

    # Convert docstring to feature file and get the path
    return docstring_to_feature_file(module)
