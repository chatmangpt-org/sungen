# **Sungen**

**Sungen** is a versatile utility package derived from `sungen` that offers an extensive suite of tools and utilities designed for AI development, project management, and workflow automation. With a user-friendly command-line interface (CLI), Sungen streamlines the development process, automates repetitive tasks, and enhances productivity, making it an essential toolkit for AI projects and modern software architectures.

## **Key Features**

- **Unified CLI Interface**: A single command-line tool to manage diverse tasks across the development lifecycle.
- **Workflow Automation**: Supports automation using BPMN (Business Process Model and Notation), YAML workflows, and other standards.
- **Code Generation & Optimization**: Tools to generate code, manage software projects, and optimize workflows for large-scale systems.
- **Integrated Development Support**: Compatible with Docker, VS Code, PyCharm, and other popular development environments.
- **Plugin Architecture**: Extend functionality through a marketplace of plugins (e.g., Ansible, AI model management, deployment tools).
- **Comprehensive AI Toolkit**: Leverages LLMs (Large Language Models) for code generation, project planning, and solution architecture design.

## **Installation**

To install the Sungen package, use `pip`:

```sh
pip install sungen
```

## **Documentation**

For detailed guidance on configuring Aider for optimal AI coding, refer to the [Configuring Aider for Optimal AI Coding](src/sungen/plugins/aider/devlog/chapters/configuring_aider.md) chapter.

## **Getting Started**

To get an overview of the available commands, use the help option:

```sh
sungen --help
```

## **CLI Overview**

The `sungen` CLI provides several commands, each tailored for specific tasks:

- **`init`**: Initialize a new Sungen project, setting up configuration files and directories.
- **`cmd`**: Create and manage subcommands within the Sungen ecosystem.
- **`api`**: Interact with external APIs, including those for AI services.
- **`deploy`**: Deploy applications, services, or workflows.
- **`fgn`**: Handle foreign integrations and tasks that extend beyond the core functionalities.
- **`inhabitant`**: Manage autonomous service components in a distributed architecture.
- **`issue`**: Track and manage project issues or tasks.
- **`marketplace`**: Browse, install, or manage plugins and extensions.
- **`optimize`**: Optimize codebases, workflows, or configurations to improve performance and efficiency.
- **`pln`**: Plan and manage tasks, milestones, and deliverables within a project.
- **`pr`**: Manage pull requests for seamless collaboration.
- **`project`**: Configure and manage project settings.
- **`proposal`**: Generate or manage project proposals.
- **`repo`**: Perform repository-related tasks, such as cloning, pushing, or tagging.
- **`support`**: Access support commands for debugging or troubleshooting.
- **`ticket`**: Manage tickets for support or issue tracking.

## **Core Capabilities**

### **Workflow Automation**
- Automate complex workflows using BPMN and YAML, integrating various plugins and external services.
- Streamline processes like continuous integration, deployment, and AI model lifecycle management.

### **AI Development Tools**
- Leverage built-in support for Large Language Models (LLMs) to generate, optimize, and refactor code.
- Use `mdbook` and other plugins to generate entire books or documentation sets with AI assistance.

### **Integrated Development Environment Support**
- Seamlessly integrates with popular tools such as Docker, VS Code, and PyCharm.
- Enables containerized development for consistent environments across the team.

## **Contributing to Sungen**

We welcome contributions! To contribute, set up your development environment by following these steps:

### **Prerequisites**

1. **SSH Configuration for Git**
   - [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add it to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
   - Configure SSH to load your keys automatically:
    ```sh
    cat << EOF >> ~/.ssh/config
    
    Host *
      AddKeysToAgent yes
      IgnoreUnknown UseKeychain
      UseKeychain yes
      ForwardAgent yes
    EOF
    ```

2. **Docker Installation**
   - [Install Docker Desktop](https://www.docker.com/get-started) to facilitate containerized development.
   - _Linux users_: Export your user ID and group ID:
    ```sh
    cat << EOF >> ~/.bashrc
    
    export UID=$(id --user)
    export GID=$(id --group)
    EOF
    ```

3. **IDE Installation**
   - Install [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), or install [PyCharm](https://www.jetbrains.com/pycharm/download) for a more customized Python development experience.

### **Development Environments**

You can set up your development environment using the following methods:

1. **GitHub Codespaces**: Quickly start a Dev Container using [GitHub Codespaces](https://github.com/features/codespaces).
2. **Dev Container with Volume**: Clone the repository into a container volume using VS Code.
3. **VS Code Local Development**: Open the repository in VS Code and use the _Dev Containers: Reopen in Container_ command.
4. **PyCharm Remote Development**: Configure Docker Compose as a remote interpreter in PyCharm.
5. **Terminal**: Use Docker Compose to manage and run development environments.

### **Development Workflow**

- Use **`poe`** to list and manage available tasks.
- Use **`poetry add {package}`** to install dependencies.
- Use **`poetry update`** to upgrade all dependencies to their latest versions.

## **Community and Support**

Join the Sungen community to discuss features, share use cases, and get help:

- [GitHub Issues](https://github.com/your-repo/sungen/issues): Report bugs or request new features.
- [Discussions](https://github.com/your-repo/sungen/discussions): Participate in discussions or start a new topic.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## **Acknowledgments**

We appreciate the contributions and support from the open-source community. Special thanks to all contributors and maintainers.

---

### **Revision Summary**

- **Expanded Features and Capabilities**: More detail on each feature and its impact on productivity, automation, and project management.
- **CLI Command Descriptions**: Improved descriptions of the CLI commands to better convey their functionality.
- **Development Environment Setup**: Clearer guidance on setting up a development environment, with more options and details.
- **Community and Support**: Added information about where to find help and how to contribute to the project.

This updated README provides a comprehensive overview of what `sungen` offers, making it more accessible to new users and contributors.
