SHELL=/bin/bash
ENV_NAME=pic2hubble-streamlit
PYTHON_VERSION=3.9


create_env:
	@if conda info --envs | grep $(ENV_NAME); then \
		echo "Environment $(ENV_NAME) already exists"; \
	else \
		echo "Creating environment $(ENV_NAME)"; \
		conda create --name $(ENV_NAME) python=$(PYTHON_VERSION) -y; \
	fi

setup: create_env
	@( \
		eval "$$(conda shell.bash hook)"; \
		conda activate $(ENV_NAME) || exit 1; \
		pip install --upgrade pip; \
		pip install -r requirements-dev.txt; \
		pip install -r requirements.txt; \
	)
