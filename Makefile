# Name of the virtual environment directory
VENV_DIR = venv

# Python executable
PYTHON = python3

# Create the virtual environment
create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

# Install dependencies
install:
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Export dependencies to requirements.txt
freeze:
	$(VENV_DIR)/bin/pip freeze > requirements.txt

# Run the main python script, passing in audio file path as argument
run:
	$(VENV_DIR)/bin/python main.py $(AUDIO_FILE)
	
# Prevent "run" from being interpreted as a file
.PHONY: run

# Clean up the virtual environment
clean:
	rm -rf $(VENV_DIR)
	rm -f requirements.txt