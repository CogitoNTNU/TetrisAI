# Development Environment

We will be utilizing a virtual environment to develop the project. This will allow us to have a consistent development environment across all developers.In this case we will be using `venv` to create the virtual environment.

## Getting Started

* Have [Python](https://www.python.org/downloads/) installed
  * Verify that python is installed by running `python --version`
* Pip install the virtual environment package
  * Verify that pip is installed by running `pip --version`
  * Install the virtual environment package by running `pip install virtualenv`
* In the root of the project, create a virtual environment by running `python -m venv .venv`
* Activate the virtual environment
  * On Windows, run `.venv\Scripts\activate`
  * On Mac/Linux, run `source .venv/bin/activate`
* Done! You should now have a fully functional development environment
* To deactivate the virtual environment, run `deactivate`

## Dependencies
Once you have entered venv you need to make sure the dependencies are installed by running `pip install -r requirements.txt`.
If you use a new pip dependency, make sure to add it to the `requirements.txt` file. This can be done by running:
```bash
pip freeze > requirements.txt
``` 
after you pip installed it locally, and then committing the changes.
