from pydantic import BaseModel, Field
from typing import List


class ProjectOverview(BaseModel):
    """
    Represents the foundational overview of a software project, including key details
    such as the project name, version, description, primary programming language, and
    technologies used. This model captures the high-level context required for
    understanding the scope and purpose of the project.

    The project overview serves as the initial point of reference for stakeholders,
    providing a concise summary that helps in aligning the development team, business
    objectives, and technical goals. It ensures that all team members and external
    collaborators have a shared understanding of the project's identity and its core
    components, establishing a common language for further discussion and planning.
    """
    software_project: str = Field(
        ...,
        description="The formal name of the software project, providing a unique identifier for all references."
    )
    version: str = Field(
        ...,
        description="The current version of the project, indicating the release stage or iteration."
    )
    description: str = Field(
        ...,
        description="A concise summary explaining the project's purpose, goals, and key features."
    )
    programming_language: str = Field(
        ...,
        description="The primary programming language utilized in the project, essential for development and maintenance."
    )
    technologies: List[str] = Field(
        default_factory=list,
        description="A comprehensive list of frameworks, libraries, and tools used in the project, indicating technological choices."
    )


class ArchitectureModel(BaseModel):
    """
    Describes the architecture of the software project, detailing the style, components,
    data flow, and any relevant diagrams. This model defines the structural blueprint of
    the system, capturing the high-level design choices that impact scalability,
    maintainability, and overall performance.

    The architecture model is essential for communicating the technical vision of the
    system to both development and operations teams. It helps in identifying critical
    components, defining the flow of data and control within the system, and ensuring
    that the architecture aligns with the project's strategic objectives. This model
    provides the foundation for making informed decisions about system modifications,
    enhancements, and optimizations.
    """
    architecture_style: str = Field(
        ...,
        description="The architectural pattern (e.g., microservices, monolithic) that defines the overall structure and design principles."
    )
    architecture_components: List[str] = Field(
        default_factory=list,
        description="Key components or modules within the architecture, such as services, databases, or layers."
    )
    data_flow: str = Field(
        ...,
        description="A detailed description of how data moves through the system, including sources, transformations, and destinations."
    )
    diagrams: List[dict] = Field(
        default_factory=list,
        description="Graphical representations (e.g., UML, sequence diagrams) illustrating the architecture and its components."
    )


class DevelopmentModel(BaseModel):
    """
    Specifies the development practices, environment setup, and coding standards followed
    within the project. This model captures the critical elements required to efficiently
    onboard developers and maintain a high standard of code quality.

    The development model outlines the procedures and commands necessary to set up the
    development environment, build and test the project, and adhere to coding conventions
    and directives. It plays a crucial role in fostering a consistent development workflow,
    minimizing errors, and reducing the time required for new developers to become
    productive members of the team.
    """
    setup_steps: List[str] = Field(
        default_factory=list,
        description="Instructions for setting up the development environment, including dependencies and configurations."
    )
    build_command: str = Field(
        ...,
        description="The command to compile or build the project from source, ensuring a consistent build process."
    )
    test_command: str = Field(
        ...,
        description="The command to execute the project's test suite, ensuring code quality and correctness."
    )
    conventions: List[str] = Field(
        default_factory=list,
        description="Coding standards, naming conventions, and best practices that developers must follow."
    )
    directives: List[str] = Field(
        default_factory=list,
        description="Guidelines or recommendations for developers to optimize performance, security, and maintainability."
    )


class BusinessRequirementsModel(BaseModel):
    """
    Captures the business requirements that guide the development of the project,
    including key features, target audience, objectives, and success metrics. This model
    ensures that the software solution aligns with the strategic goals and needs of the
    organization.

    The business requirements model is used to articulate the primary functionalities
    that the project must deliver, identify the intended user base, and define how success
    will be measured. It serves as a bridge between the technical team and business
    stakeholders, helping to prioritize features, plan releases, and ensure that the
    project delivers value to its users and the business as a whole.
    """
    key_features: List[str] = Field(
        default_factory=list,
        description="Primary features and functionalities that deliver value to the users and stakeholders."
    )
    target_audience: str = Field(
        ...,
        description="The specific group of users or customers the project is intended to serve, including demographics and needs."
    )
    business_objectives: List[str] = Field(
        default_factory=list,
        description="High-level goals that the project aims to achieve, such as revenue growth, market penetration, or user engagement."
    )
    success_metrics: List[str] = Field(
        default_factory=list,
        description="Quantifiable criteria used to measure the project's success and impact, like user growth, retention rate, or ROI."
    )


class QualityAssuranceModel(BaseModel):
    """
    Defines the quality assurance practices for the project, including testing frameworks,
    code coverage thresholds, performance benchmarks, and standards. This model ensures
    that the software meets the required quality criteria before it is released.

    The quality assurance model is critical for maintaining a high level of software
    reliability and performance. It provides a framework for testing the software at
    various stages of development, setting benchmarks for acceptable performance, and
    adhering to quality standards. This model helps to identify defects early, reduce
    technical debt, and ensure that the final product meets the expectations of end users
    and stakeholders.
    """
    testing_frameworks: List[str] = Field(
        default_factory=list,
        description="Testing tools and frameworks (e.g., pytest, JUnit) used to verify code functionality and performance."
    )
    coverage_threshold: str = Field(
        ...,
        description="Minimum acceptable code coverage percentage, ensuring sufficient test coverage for reliability."
    )
    performance_benchmarks: List[str] = Field(
        default_factory=list,
        description="Standards or targets for evaluating the project's performance, like response time or throughput."
    )
    quality_standards: List[str] = Field(
        default_factory=list,
        description="Industry or internal standards the project must comply with, such as ISO, OWASP, or internal QA policies."
    )


class DeploymentModel(BaseModel):
    """
    Outlines the deployment strategy for the project, detailing the platform, CI/CD pipeline,
    environments, and rollback procedures. This model ensures that the deployment process
    is robust, repeatable, and aligned with organizational policies.

    The deployment model provides a clear and detailed roadmap for deploying the software
    to various environments, including staging and production. It covers the steps
    involved in setting up and maintaining these environments, managing deployment
    pipelines, and handling failures through rollback procedures. This model is crucial
    for minimizing downtime, ensuring reliability, and maintaining the integrity of the
    production environment.
    """
    deployment_platform: str = Field(
        ...,
        description="The infrastructure or service provider (e.g., AWS, Azure, GCP) where the application is deployed."
    )
    cicd_pipeline: List[str] = Field(
        default_factory=list,
        description="Stages in the CI/CD pipeline, from code integration to deployment, ensuring automated delivery."
    )
    staging_environment: str = Field(
        ...,
        description="The URL or endpoint of the staging environment where pre-release testing and validation occur."
    )
    production_environment: str = Field(
        ...,
        description="The URL or endpoint of the production environment where the final application is live and accessible to users."
    )
    rollback_procedures: List[str] = Field(
        default_factory=list,
        description="Step-by-step actions to revert the application to a previous stable state in case of deployment issues."
    )
