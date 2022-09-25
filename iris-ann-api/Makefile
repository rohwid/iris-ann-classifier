CMD = ./start.sh

# PROJECT
PROJECT_DIR = ./project
MODEL_DIR = $(PROJECT_DIR)/model
ARTEFACT_DIR = $(PROJECT_DIR)/output

# BUILD
build:
	mkdir -p $(MODEL_DIR)
	mkdir -p $(ARTEFACT_DIR)

	chmod +x permission.sh
	./permission.sh

# EXECUTE - TEST
serve:
	$(CMD) serve

train:
	$(CMD) train

# DEPLOY IRIS ANN
deploy_model:
	$(CMD) model

# CLEAN IRIS ANN
clean_model:
	sudo docker-compose down

# CLEAN BUILD
clean:
	rm -r $(MODEL_DIR)
	rm -r $(ARTEFACT_DIR)
