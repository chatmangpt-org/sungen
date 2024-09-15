from pydantic import BaseModel, Field, HttpUrl
from typing import List, Union


class Resource(BaseModel):
    """
    Represents a single resource within the documentation context. Each resource can be a URL or
    a relative path to a local documentation file.
    """
    title: str = Field(
        ...,
        description="A short title or description of the resource, such as 'Official Documentation' or 'Getting Started Guide'."
    )
    url: Union[HttpUrl, str] = Field(
        ...,
        description="The URL of the resource, or a relative path to a local documentation file."
    )


class DocumentationSource(BaseModel):
    """
    Represents a documentation source, including its name, relationship to the project, and resources.
    Each source provides a set of resources that are relevant to the project context.
    """
    name: str = Field(
        ...,
        description="The name of the documentation source, such as 'TypeScript' or 'Node.js'."
    )
    relationship: str = Field(
        ...,
        description="A description of the relationship between the documentation source and the project, e.g., 'Main language for linter implementation'."
    )
    resources: List[Resource] = Field(
        default_factory=list,
        description="A list of resources related to the documentation source, such as URLs or file paths."
    )


class ContextDocsModel(BaseModel):
    """
    Represents the overall context documentation model that contains multiple documentation sources.
    This model is used to capture and validate the `.contextdocs` file content.
    """
    contextdocs: List[DocumentationSource] = Field(
        default_factory=list,
        description="A list of documentation sources to be incorporated into the project's context."
    )
