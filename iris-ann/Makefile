MAIN_DIR = ./project
MODEL_DIR = $(MAIN_DIR)/model
ARTEFACT_DIR = $(MAIN_DIR)/output

# BUILD
build:
	mkdir -p $(MODEL_DIR)
	mkdir -p $(ARTEFACT_DIR)

	chmod +x permission.sh
	./permission.sh

# EXECUTE
train:
	./start.sh

# CLEAN BUILD
clean:
	rm -r $(MODEL_DIR)
	rm -r $(ARTEFACT_DIR)
