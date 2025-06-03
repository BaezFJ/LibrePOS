# Installation Guide for LibrePOS

This guide explains how to install LibrePOS using different methods, including Git and PyPI. It also covers installation using `venv`, `poetry`, and the `uv` package manager from Astral.

---

## 1. Installing LibrePOS from GitHub

### Prerequisites

Ensure you have the following installed:

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/BaezFJ/LibrePOS.git
   cd LibrePOS
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask initdb
   ```

5. Run the application:
   ```bash
   flask run
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 2. Installing LibrePOS from PyPI

LibrePOS can also be installed directly as a Python package from [PyPI](https://pypi.org/project/librepos/).

### Steps

1. Ensure you have Python 3.9 or higher and pip installed.

2. Install the LibrePOS package from PyPI:
   ```bash
   pip install librepos
   ```

3. After installation, set up the database:
   ```bash
   flask initdb
   ```

4. Start the application:
   ```bash
   flask run
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 3. Using a Virtual Environment with `venv`

`venv` can be used to create an isolated Python environment for LibrePOS.

### Steps

1. Create a virtual environment:
   ```bash
   python3 -m venv env
   ```

2. Activate the virtual environment:
   ```bash
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the required dependencies via pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Follow the steps in Section 1 (Installing LibrePOS from GitHub) or Section 2 (Installing LibrePOS from PyPI) to complete the installation process.

---

## 4. Using Poetry

[Poetry](https://python-poetry.org/) is a dependency manager and build tool for Python projects.

### Prerequisites

- Poetry installed. Use the following command to install if needed:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LibrePOS.git
   cd LibrePOS
   ```

2. Install the project's dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Run the application in Poetry's virtual environment:
   ```bash
   poetry run flask initdb
   poetry run flask run
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 5. Using `uv` for Installation and Management

[uv](https://docs.astral.sh/uv/) is a lightweight Python package manager developed by Astral. You can use it to install and manage LibrePOS and its dependencies with ease.

### Prerequisites

- Install the `uv` package manager:
  ```bash
  pip install uv
  ```

### Steps

1. Use `uv` to install LibrePOS:
   ```bash
   uv install librepos
   ```

2. Set up the database:
   ```bash
   flask initdb
   ```

3. Run the LibrePOS application:
   ```bash
   flask run
   ```

4. Access the application in your browser at:
   ```
   http://127.0.0.1:5000
   ```

---

Choose the installation method that best fits your workflow. Options such as `venv`, `poetry`, or `uv` provide flexibility for both development and production setups.