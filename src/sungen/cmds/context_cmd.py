"""context"""
import dspy
import typer
from dspy import Signature, InputField, OutputField
from munch import Munch

app = typer.Typer()


@app.command(name="create")
def create():
    """create"""
    _create()

def _create():
    """create"""
    typer.echo("Running create subcommand.")

epic_tmpl = """
Here's how you can create a **Jinja template** that converts the response outputs of `GenerateRequirements` (which include requirements, user stories, workflows, and architecture diagrams) into epics for the `GenerateProjectRequirements` Signature class. 

The goal is to map the generated requirements and user stories into the format expected by `GenerateProjectRequirements`, which takes a high-level **context** (i.e., the structured output from the meta-generator) and **question** (i.e., what you're trying to solve or answer with these requirements) and produces a list of epics.

### Jinja Template:

```jinja
{% for user_story in user_stories %}
- User story: {{ user_story }}
  Description: 
  - Based on the context of {{ project_description }}, the system should fulfill the following requirement: {{ user_story }}.
{% endfor %}

{% if workflow_diagram %}
- Epic: Workflow and Interaction Diagrams
  Description:
  - The system should visualize the project's workflow using the following Mermaid.js diagram.
  ```mermaid
  {{ workflow_diagram }}
  ```
{% endif %}

{% if architecture_diagram %}
- Epic: Architecture Design
  Description:
  - The system should provide an architectural overview using the C4 Model.
  ```c4
  {{ architecture_diagram }}
  ```
{% endif %}
"""

input_str = '''### Meta-Generator for Requirements Creation

The **Meta-Generator** is a tool designed to take a brief set of sentences or a high-level project description and generate detailed requirements, including user stories, diagrams, and workflows for developing a specific tool or software component. In this case, the **meta-generator** will generate the requirements for the **Codebase Context Generator** described above.

This meta-generator will leverage large language models (LLMs) to transform a high-level description into comprehensive requirements documents, user stories, and technical diagrams. It will also generate diagrams using **Mermaid.js** for flowcharts and sequence diagrams, and **C4 DSL** for architecture visualization, following the C4 Model conventions.

### Signature for the Meta-Generator

Here’s a DSPy **Signature** class to define the structure of this meta-generator:

```python
class GenerateRequirements(Signature):
    """
    Generate detailed requirements, user stories, and technical diagrams from high-level project descriptions.
    The generated output will include user stories, workflows, and diagrams in Mermaid.js and C4 DSL.
    """
    
    project_description = InputField(desc="A high-level description of the tool or feature to be developed.")
    
    requirements = OutputField(desc="A structured list of requirements based on the project description.")
    user_stories = OutputField(desc="Generated user stories broken down from the project description.")
    workflow_diagram = OutputField(desc="A Mermaid.js diagram showing the flow or interactions within the tool.")
    architecture_diagram = OutputField(desc="A C4 DSL diagram outlining the system's architecture.")
```

---

### How the Meta-Generator Works

- **Input**: The meta-generator takes a couple of sentences or a high-level project description as input, such as: 
  - *"We need a tool that generates .context.md files for a project based on user inputs, detects project dependencies, and provides suggestions for technologies and architecture."*
  
- **Output**: The meta-generator processes this input and generates:
  1. **Detailed Requirements**: A structured list of functional and non-functional requirements.
  2. **User Stories**: Concrete user stories for developers to work on.
  3. **Mermaid.js Diagrams**: Visual representations of workflows, processes, or interactions within the system.
  4. **C4 Model Diagrams**: High-level architectural diagrams (Context, Container, Component) to help understand system structure and design.

---

### Example Output of the Meta-Generator

#### 1. **Generated Requirements**

```markdown
### Functional Requirements:
1. The generator should create `.context.md`, `.context.yaml`, and `.context.json` files based on user inputs.
2. It should automatically detect project dependencies from files like `package.json`, `requirements.txt`, or `build.gradle`.
3. The generator must allow the user to provide metadata like `module_name`, `version`, `description`, and `architecture`.
4. A CLI should be provided to run the generator with options like `--format`, `--output-directory`.
5. The tool should generate user story diagrams and workflows in Mermaid.js.
6. The generator should also output architecture diagrams using the C4 model (Context, Container, and Component views).

### Non-Functional Requirements:
1. The system should be scalable to handle large codebases with many dependencies.
2. It should support extensibility to include new file formats for context generation.
3. The tool must ensure that the context files adhere to the latest version of the Codebase Context Specification.
4. Generated context files should be human-readable and easy for AI to parse.
```

#### 2. **Generated User Stories**

```markdown
### User Stories:
1. **As a developer**, I want to generate a `.context.md` file from my project’s existing metadata so that I can provide a high-level overview of my codebase.
2. **As a developer**, I want to scan my project directory for dependencies and automatically include them in the context file so that I don’t have to manually input them.
3. **As a product manager**, I want to provide business requirements and directives to be included in the context file to ensure alignment with project goals.
4. **As a developer**, I want to use the CLI to run the generator with different output formats (`.md`, `.yaml`, `.json`) so that I can choose the format that best fits my project needs.
5. **As an architect**, I want the generator to produce architecture diagrams (using C4 DSL) to better visualize the system’s design.
6. **As a developer**, I want the generator to produce workflows (using Mermaid.js) to represent key interactions and processes in my project.
```

#### 3. **Generated Workflow Diagram (Mermaid.js)**

```mermaid
graph TD
    A[User Provides Project Metadata] --> B[Run Generator via CLI]
    B --> C{Format Selection}
    C -->|.context.md| D[Generate .context.md]
    C -->|.context.yaml| E[Generate .context.yaml]
    C -->|.context.json| F[Generate .context.json]
    B --> G[Scan Project for Dependencies]
    G --> H[Include Detected Dependencies in Context File]
    D --> I[User Reviews Generated File]
```

This diagram shows the workflow from when the user provides metadata to when the `.context.md` file is generated and dependencies are scanned.

#### 4. **Generated Architecture Diagram (C4 Model - Context Diagram)**

```c4
Person(dev, "Developer", "A developer who uses the generator to create context files.")
System(Generator, "Codebase Context Generator", "Generates .context files for a codebase based on user input.")
System_Ext(DependencyScanner, "Dependency Scanner", "Scans the project for dependencies and libraries.")

Rel(dev, Generator, "Uses CLI to generate context files")
Rel(Generator, DependencyScanner, "Scans project files to identify dependencies")
```

This C4 Context diagram shows the relationship between the **developer**, the **Codebase Context Generator**, and the **Dependency Scanner** system.

---

### Key Features of the Meta-Generator

1. **Automated Requirements Generation**: The meta-generator will produce a complete set of requirements based on high-level input, saving time for product managers and architects in defining the scope of the project.
  
2. **Mermaid.js Workflow Diagrams**: The generator will create visual workflow diagrams representing system interactions, processes, and user actions.

3. **C4 Model Architecture Diagrams**: The meta-generator will output high-level architecture diagrams that follow the C4 model to illustrate the structure of the system being developed.

4. **Adaptability**: The tool can generate different types of files (requirements, user stories, diagrams) for a wide variety of development projects, making it highly versatile.

---

### Conclusion

The **Meta-Generator for Requirements Creation** will streamline the process of converting project descriptions into detailed requirements, user stories, and technical diagrams. By using large language models and integrating with **Mermaid.js** and **C4 DSL**, this tool will help teams more quickly and efficiently design and plan their development projects. The resulting documentation will enhance communication, ensure clear project goals, and improve the overall design and development process.'''

class GenerateRequirements(Signature):
    """
    Generate detailed requirements, user stories, and technical diagrams from high-level project descriptions.
    The generated output will include user stories, workflows, and diagrams in Mermaid.js and C4 DSL.
    """

    project_description = InputField(desc="A high-level description of the tool or feature to be developed.")

    requirements = OutputField(desc="A structured list of requirements based on the project description.")
    user_stories = OutputField(desc="Generated user stories broken down from the project description.")
    workflow_diagram = OutputField(desc="A Mermaid.js diagram showing the flow or interactions within the tool.")
    architecture_diagram = OutputField(desc="A C4 DSL diagram outlining the system's architecture.")


def main():
    """Main function"""
    from sungen.utils.dspy_tools import init_dspy
    init_dspy()

    # reqs = dspy.Predict(GenerateRequirements).forward(project_description=input_str)

    # print(reqs)

    reqs = Munch(
        requirements='### Generated Requirements\n\n```markdown\n\n### Functional Requirements:\n\n1. The generator '
                     'should create `.context.md`, `.context.yaml`, and `.context.json` files based on user '
                     'inputs.\n\n2. It should automatically detect project dependencies from files like '
                     '`package.json`, `requirements.txt`, or `build.gradle`.\n\n3. The generator must allow the user '
                     'to provide metadata like `module_name`, `version`, `description`, and `architecture`.\n\n4. A '
                     'CLI should be provided to run the generator with options like `--format`, '
                     '`--output-directory`.\n\n5. The tool should generate user story diagrams and workflows in '
                     'Mermaid.js.\n\n6. The generator should also output architecture diagrams using the C4 model ('
                     'Context, Container, and Component views).\n\n### Non-Functional Requirements:\n\n1. The system '
                     'should be scalable to handle large codebases with many dependencies.\n\n2. It should support '
                     'extensibility to include new file formats for context generation.\n\n3. The tool must ensure '
                     'that the context files adhere to the latest version of the Codebase Context '
                     'Specification.\n\n4. Generated context files should be human-readable and easy for AI to '
                     'parse.\n\n```\n\n### Generated User Stories\n\n```markdown\n\n### User Stories:\n\n1. **As a '
                     'developer**, I want to generate a `.context.md` file from my project’s existing metadata so '
                     'that I can provide a high-level overview of my codebase.\n\n2. **As a developer**, '
                     'I want to scan my project directory for dependencies and automatically include them in the '
                     'context file so that I don’t have to manually input them.\n\n3. **As a product manager**, '
                     'I want to provide business requirements and directives to be included in the context file to '
                     'ensure alignment with project goals.\n\n4. **As a developer**, I want to use the CLI to run the '
                     'generator with different output formats (`.md`, `.yaml`, `.json`) so that I can choose the '
                     'format that best fits my project needs.\n\n5. **As an architect**, I want the generator to '
                     'produce architecture diagrams (using C4 DSL) to better visualize the system’s design.\n\n6. '
                     '**As a developer**, I want the generator to produce workflows (using Mermaid.js) to represent '
                     'key interactions and processes in my project.\n\n```\n\n### Generated Workflow Diagram ('
                     'Mermaid.js)\n\n```mermaid\n\ngraph TD\n\nA[User Provides Project Metadata] --> B[Run Generator '
                     'via CLI]\n\nB --> C{Format Selection}\n\nC -->|.context.md| D[Generate .context.md]\n\nC '
                     '-->|.context.yaml| E[Generate .context.yaml]\n\nC -->|.context.json| F[Generate '
                     '.context.json]\n\nB --> G[Scan Project for Dependencies]\n\nG --> H[Include Detected '
                     'Dependencies in Context File]\n\nD --> I[User Reviews Generated File]\n\n```\n\n### Generated '
                     'Architecture Diagram (C4 Model - Context Diagram)\n\n```c4\n\nPerson(dev, "Developer", '
                     '"A developer who uses the generator to create context files.")\n\nSystem(Generator, '
                     '"Codebase Context Generator", "Generates .context files for a codebase based on user '
                     'input.")\n\nSystem_Ext(DependencyScanner, "Dependency Scanner", "Scans the project for '
                     'dependencies and libraries.")\n\nRel(dev, Generator, "Uses CLI to generate context '
                     'files")\n\nRel(Generator, DependencyScanner, "Scans project files to identify '
                     'dependencies")\n\n```',
        user_stories='### Generated User Stories\n\n```markdown\n\n### User Stories:\n\n1. **As a developer**, '
                     'I want to generate a `.context.md` file from my project’s existing metadata so that I can '
                     'provide a high-level overview of my codebase.\n\n2. **As a developer**, I want to scan my '
                     'project directory for dependencies and automatically include them in the context file so that I '
                     'don’t have to manually input them.\n\n3. **As a product manager**, I want to provide business '
                     'requirements and directives to be included in the context file to ensure alignment with project '
                     'goals.\n\n4. **As a developer**, I want to use the CLI to run the generator with different '
                     'output formats (`.md`, `.yaml`, `.json`) so that I can choose the format that best fits my '
                     'project needs.\n\n5. **As an architect**, I want the generator to produce architecture diagrams '
                     '(using C4 DSL) to better visualize the system’s design.\n\n6. **As a developer**, I want the '
                     'generator to produce workflows (using Mermaid.js) to represent key interactions and processes '
                     'in my project.\n\n```\n\n### Generated Workflow Diagram (Mermaid.js)\n\n```mermaid\n\ngraph '
                     'TD\n\nA[User Provides Project Metadata] --> B[Run Generator via CLI]\n\nB --> C{Format '
                     'Selection}\n\nC -->|.context.md| D[Generate .context.md]\n\nC -->|.context.yaml| E[Generate '
                     '.context.yaml]\n\nC -->|.context.json| F[Generate .context.json]\n\nB --> G[Scan Project for '
                     'Dependencies]\n\nG --> H[Include Detected Dependencies in Context File]\n\nD --> I[User Reviews '
                     'Generated File]\n\n```\n\n### Generated Architecture Diagram (C4 Model - Context '
                     'Diagram)\n\n```c4\n\nPerson(dev, "Developer", "A developer who uses the generator to create '
                     'context files.")\n\nSystem(Generator, "Codebase Context Generator", "Generates .context files '
                     'for a codebase based on user input.")\n\nSystem_Ext(DependencyScanner, "Dependency Scanner", '
                     '"Scans the project for dependencies and libraries.")\n\nRel(dev, Generator, "Uses CLI to '
                     'generate context files")\n\nRel(Generator, DependencyScanner, "Scans project files to identify '
                     'dependencies")\n\n```',
        workflow_diagram='### Workflow Diagram (Mermaid.js)\n\n```mermaid\n\ngraph TD\n\nA[User Provides Project '
                         'Metadata] --> B[Run Generator via CLI]\n\nB --> C{Format Selection}\n\nC -->|.context.md| '
                         'D[Generate .context.md]\n\nC -->|.context.yaml| E[Generate .context.yaml]\n\nC '
                         '-->|.context.json| F[Generate .context.json]\n\nB --> G[Scan Project for Dependencies]\n\nG '
                         '--> H[Include Detected Dependencies in Context File]\n\nD --> I[User Reviews Generated '
                         'File]\n\n```\n\n### Architecture Diagram (C4 Model - Context Diagram)\n\n```c4\n\nPerson('
                         'dev, "Developer", "A developer who uses the generator to create context files.")\n\nSystem('
                         'Generator, "Codebase Context Generator", "Generates .context files for a codebase based on '
                         'user input.")\n\nSystem_Ext(DependencyScanner, "Dependency Scanner", "Scans the project for '
                         'dependencies and libraries.")\n\nRel(dev, Generator, "Uses CLI to generate context '
                         'files")\n\nRel(Generator, DependencyScanner, "Scans project files to identify '
                         'dependencies")\n\n```',
        architecture_diagram='Diagram (C4 Model - Context Diagram)\n\n```c4\n\nPerson(dev, "Developer", "A developer '
                             'who uses the generator to create context files.")\n\nSystem(Generator, '
                             '"Codebase Context Generator", "Generates .context files for a codebase based on user '
                             'input.")\n\nSystem_Ext(DependencyScanner, "Dependency Scanner", "Scans the project for '
                             'dependencies and libraries.")\n\nRel(dev, Generator, "Uses CLI to generate context '
                             'files")\n\nRel(Generator, DependencyScanner, "Scans project files to identify '
                             'dependencies")\n\n```'
    )

    print(reqs.workflow_diagram)

mmd = """
graph TD
    A[User Provides Project Metadata] --> B[Run Generator via CLI]

    B --> C{Format Selection}

    C -->|.context.md| D[Generate .context.md]

    C -->|.context.yaml| E[Generate .context.yaml]

    C -->|.context.json| F[Generate .context.json]

    B --> G[Scan Project for Dependencies]

    G --> H[Include Detected Dependencies in Context File]

    D --> I[User Reviews Generated File]
"""

if __name__ == '__main__':
    main()
