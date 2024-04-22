# Development Environment

We will be using vscode, and Dev Containers to develop the project. This will allow us to have a consistent development environment across all developers.

## Getting Started

* Have [Docker](https://docs.docker.com/get-docker/) installed
  * Verify that docker is installed by running `docker --version`
* Install the [Dev Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for vscode
* Pull the latest changes from the repository
* Go to the "Remote Explorer" tab in vscode
* Click on the "Reopen in Container" button for the project
* Done! You should now have a fully functional development environment

## Extensions

The following extensions come with the dev container:

* Prettier
* Code spell checker (to keep the documentation  and code clean)
* Docker (in case we will be using docker more in the future)
* Markdownlint (to keep the documentation consistent and clean)
* The default python extensions
  * Python
  * Pylance
  * Debugpy

You can add more extensions by going to the "Extensions" tab in vscode and clicking on the "Install in Container" button for the extensions you cant live without.

## Dependencies
When you build the container, the dependencies will be installed. If you use a new pip dependency, make sure to add it to the `requirements.txt` file. This can be done by running 
```bash
pip freeze > requirements.txt
``` 
in the dev container, and then committing the changes.

## Structural Changes

In case of structural changes to the project, like adding a new service, or changing `devcontainer.json`, you will need to rebuild the dev container. You can do this by clicking on the "Rebuild Container" button in the "Remote Explorer" tab in vscode.
