from typing import List, Optional, Dict, Any, Callable, Union
from pydantic import BaseModel, Field
from enum import Enum

class AttributeType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    UUID = "uuid"
    MAP = "map"
    LIST = "list"
    STRUCT = "struct"
    # Add more types as needed

class Attribute(BaseModel):
    name: str
    type: AttributeType
    writable: bool = True
    default: Optional[Union[Any, Callable]] = None
    update_default: Optional[Union[Any, Callable]] = None
    primary_key: bool = False
    allow_nil: bool = True
    generated: bool = False
    match_other_defaults: bool = False
    constraints: List[Dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def create_timestamp(cls, name: str = "inserted_at"):
        return cls(
            name=name,
            type=AttributeType.DATETIME,
            writable=False,
            default="&DateTime.utc_now/0",
            match_other_defaults=True,
            allow_nil=False
        )

    @classmethod
    def update_timestamp(cls, name: str = "updated_at"):
        return cls(
            name=name,
            type=AttributeType.DATETIME,
            writable=False,
            default="&DateTime.utc_now/0",
            update_default="&DateTime.utc_now/0",
            match_other_defaults=True,
            allow_nil=False
        )

    @classmethod
    def uuid_primary_key(cls, name: str = "id"):
        return cls(
            name=name,
            type=AttributeType.UUID,
            writable=False,
            default="&Ash.UUID.generate/0",
            primary_key=True,
            allow_nil=False
        )

    @classmethod
    def integer_primary_key(cls, name: str = "id"):
        return cls(
            name=name,
            type=AttributeType.INTEGER,
            writable=False,
            generated=True,
            primary_key=True,
            allow_nil=False
        )

class Action(BaseModel):
    name: str
    type: str  # e.g., "create", "read", "update", "destroy", "custom"
    arguments: Dict[str, Any] = Field(default_factory=dict)
    returns: Optional[str] = None
    description: Optional[str] = None

class Calculation(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    arguments: Dict[str, Any] = Field(default_factory=dict)
    load: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

class Aggregate(BaseModel):
    name: str
    type: str
    field: str
    description: Optional[str] = None

class Relationship(BaseModel):
    name: str
    type: str  # e.g., "belongs_to", "has_many", "has_one", "many_to_many"
    destination: str
    source_field: Optional[str] = None
    destination_field: Optional[str] = None

class Validation(BaseModel):
    name: str
    type: str
    options: Dict[str, Any] = Field(default_factory=dict)
    message: Optional[str] = None

class Change(BaseModel):
    name: str
    type: str
    options: Dict[str, Any] = Field(default_factory=dict)

class Resource(BaseModel):
    name: str
    module: str
    attributes: List[Attribute] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    calculations: List[Calculation] = Field(default_factory=list)
    aggregates: List[Aggregate] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    validations: List[Validation] = Field(default_factory=list)
    changes: List[Change] = Field(default_factory=list)

class DataLayer(BaseModel):
    name: str
    options: Dict[str, Any] = Field(default_factory=dict)

class Identity(BaseModel):
    name: str
    keys: List[str]

class AshResource(BaseModel):
    name: str
    module: str
    description: Optional[str] = None
    base_filter: Optional[Dict[str, Any]] = None
    data_layer: DataLayer
    attributes: List[Attribute] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    calculations: List[Calculation] = Field(default_factory=list)
    aggregates: List[Aggregate] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    validations: List[Validation] = Field(default_factory=list)
    changes: List[Change] = Field(default_factory=list)
    identities: List[Identity] = Field(default_factory=list)

class AshRegistry(BaseModel):
    resources: List[AshResource] = Field(default_factory=list)

class ExecutionConfig(BaseModel):
    timeout: Optional[int] = None

class AuthorizationConfig(BaseModel):
    authorize: str = "default"

class GraphQLConfig(BaseModel):
    authorize: bool = True

class Policy(BaseModel):
    name: str
    type: str
    condition: str
    action: str

class AshDomain(BaseModel):
    name: str
    module: str
    resources: List[AshResource] = Field(default_factory=list)
    execution: Optional[ExecutionConfig] = None
    authorization: Optional[AuthorizationConfig] = None
    graphql: Optional[GraphQLConfig] = None
    policies: List[Policy] = Field(default_factory=list)
    extensions: List[str] = Field(default_factory=list)

    class Config:
        extra = "allow"

class AshApi(BaseModel):
    name: str
    module: str
    domains: List[AshDomain] = Field(default_factory=list)

class AshEngine(BaseModel):
    api: AshApi
    registry: AshRegistry


