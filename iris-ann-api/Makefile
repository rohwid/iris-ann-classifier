CMD = ./start.sh

NAME = iris-ann
VER = 0.0.1

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
deploy:
	$(CMD) deploy

# AIRFLOW
airflow:
	$(CMD) deploy

# CLEAN IRIS ANN
clean_deploy:
	sudo docker-compose down

# CLEAN AIRFLOW
clean_airflow:
	cd airflow && sudo docker-compose down

# CLEAN BUILD
clean:
	rm -r $(MODEL_DIR)
	rm -r $(ARTEFACT_DIR)
