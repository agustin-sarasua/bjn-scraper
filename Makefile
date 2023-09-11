APP_NAME = bjn-scraper
APP_VERSION = 0.0.1

TAG ?= $(APP_VERSION)

# Set the name of the virtual environment
VENV_NAME = .venv

# Create and activate the virtual environment
venv:
	python3 -m venv $(VENV_NAME)

# Install packages from requirements.txt
install:
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

# Target to setup the virtual environment
setup: venv install	
