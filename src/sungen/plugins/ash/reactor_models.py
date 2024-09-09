"""Reactor models for Ash Studio Ecosystem."""

from typing import List, Dict, Any, Optional, Union, Callable
from pydantic import BaseModel, Field, constr
from enum import Enum

class StepType(str, Enum):
    STEP = "step"
    ASYNC_STEP = "async_step"

class CompensationStrategyType(str, Enum):
    RETRY = "retry"
    UNDO = "undo"

class ReactorStep(BaseModel):
    """Represents a step in an Ash Reactor workflow."""
    name: constr(min_length=1) = Field(..., description="Unique name for the step")
    type: StepType = Field(..., description="Type of step: synchronous or asynchronous")
    resource: str = Field(..., description="The Ash resource this step interacts with")
    action: str = Field(..., description="The action to be performed on the resource")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments to be passed to the action")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Inputs for the step, can reference previous steps or reactor inputs")
    wait_for: List[str] = Field(default_factory=list, description="List of step names this step should wait for before executing")
    compensate: Optional[Dict[str, Any]] = Field(None, description="Compensation logic in case of step failure")
    undo: Optional[Dict[str, Any]] = Field(None, description="Logic to undo the step's effects if a later step fails")

class ReactorInput(BaseModel):
    """Represents an input for an Ash Reactor."""
    name: constr(min_length=1) = Field(..., description="Name of the input")
    type: str = Field(..., description="Type of the input (e.g., string, integer)")

class ReactorOutput(BaseModel):
    """Represents an output from an Ash Reactor."""
    name: constr(min_length=1) = Field(..., description="Name of the output")
    source: Union[str, Dict[str, Any]] = Field(..., description="Source of the output, can be a step result or a transformation")

class Reactor(BaseModel):
    """Represents an Ash Reactor workflow."""
    name: constr(min_length=1) = Field(..., description="Name of the Reactor")
    inputs: List[ReactorInput] = Field(default_factory=list, description="List of inputs for the Reactor")
    steps: List[ReactorStep] = Field(default_factory=list, description="List of steps in the Reactor workflow")
    outputs: List[ReactorOutput] = Field(default_factory=list, description="List of outputs from the Reactor")

class CompensationStrategy(BaseModel):
    """Represents a compensation strategy for error handling in Ash Reactor."""
    type: CompensationStrategyType = Field(..., description="Type of compensation strategy")
    max_attempts: Optional[int] = Field(None, ge=1, description="Maximum number of retry attempts")
    delay: Optional[int] = Field(None, ge=0, description="Delay between retry attempts in milliseconds")

class ReactorError(BaseModel):
    """Represents an error that occurred during Reactor execution."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")

class ReactorResult(BaseModel):
    """Represents the result of a Reactor step execution."""
    status: str = Field(..., description="Status of the step execution (e.g., 'success', 'failure')")
    data: Optional[Dict[str, Any]] = Field(None, description="Result data from the step execution")
    error: Optional[ReactorError] = Field(None, description="Error information if the step failed")

class ReactorExecution(BaseModel):
    """Represents an instance of a Reactor being executed."""
    reactor: Reactor = Field(..., description="The Reactor being executed")
    inputs: Dict[str, Any] = Field(..., description="Input values for this execution")
    results: Dict[str, ReactorResult] = Field(default_factory=dict, description="Results of each step in the execution")
    status: str = Field("pending", description="Overall status of the Reactor execution")
    compensation_strategy: Optional[CompensationStrategy] = Field(None, description="Compensation strategy for this execution")

class ReactorBuilder(BaseModel):
    """Helper class for building Reactor workflows."""
    steps: List[ReactorStep] = Field(default_factory=list, description="Steps to be added to the Reactor")
    inputs: List[ReactorInput] = Field(default_factory=list, description="Inputs to be added to the Reactor")
    outputs: List[ReactorOutput] = Field(default_factory=list, description="Outputs to be added to the Reactor")

    def build(self, name: str) -> Reactor:
        """Build and return a Reactor instance."""
        return Reactor(name=name, inputs=self.inputs, steps=self.steps, outputs=self.outputs)

class ReactorConfig(BaseModel):
    """Configuration options for Ash Reactor."""
    max_concurrency: Optional[int] = Field(None, ge=1, description="Maximum number of steps to run concurrently")
    timeout: Optional[int] = Field(None, ge=0, description="Overall timeout for the Reactor execution in milliseconds")
    retry_strategy: Optional[CompensationStrategy] = Field(None, description="Default retry strategy for all steps")

class ReactorRegistry(BaseModel):
    """Registry for managing multiple Reactor workflows."""
    reactors: Dict[str, Reactor] = Field(default_factory=dict, description="Dictionary of registered Reactors")

    def register(self, reactor: Reactor):
        """Register a new Reactor workflow."""
        self.reactors[reactor.name] = reactor

    def get(self, name: str) -> Optional[Reactor]:
        """Retrieve a Reactor workflow by name."""
        return self.reactors.get(name)

class ReactorDsl(BaseModel):
    """Represents the Reactor DSL for defining workflows."""
    name: str = Field(..., description="Name of the Reactor module")
    inputs: List[str] = Field(default_factory=list, description="List of input names")
    steps: List[Dict[str, Any]] = Field(default_factory=list, description="List of step definitions")
    outputs: List[str] = Field(default_factory=list, description="List of output names")

class ReactorStep(BaseModel):
    """Represents a step in the Reactor DSL."""
    name: str = Field(..., description="Name of the step")
    resource: str = Field(..., description="Resource the step interacts with")
    action: str = Field(..., description="Action to be performed")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the action")
    async_: bool = Field(False, description="Whether the step should be executed asynchronously")
    compensate: Optional[Callable] = Field(None, description="Compensation function for the step")
    undo: Optional[Callable] = Field(None, description="Undo function for the step")