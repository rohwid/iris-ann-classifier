CMD = ./start.sh

# PROJECT
PROJECT_DIR = ./project
MODEL_DIR = $(PROJECT_DIR)/model
ARTEFACT_DIR = $(PROJECT_DIR)/output
AIRFLOW_DIR = ./airflow
DATA_DIR = $(AIRFLOW_DIR)/data
LOGS_DIR = $(AIRFLOW_DIR)/logs
PLUGINS_DIR = $(AIRFLOW_DIR)/plugins

# BUILD
build:
	mkdir -p $(MODEL_DIR)
	mkdir -p $(ARTEFACT_DIR)
	mkdir -p $(DATA_DIR)
	mkdir -p $(LOGS_DIR)
	mkdir -p $(PLUGINS_DIR)

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

# AIRFLOW
deploy_airflow:
	$(CMD) airflow

# CLEAN IRIS ANN
clean_model:
	docker-compose down

# CLEAN AIRFLOW
clean_airflow:
	cd airflow && docker-compose down

# CLEAN BUILD
clean:
	rm -r $(MODEL_DIR)
	rm -r $(ARTEFACT_DIR)
	rm -r $(DATA_DIR)
	rm -r $(LOGS_DIR)
	rm -r $(PLUGINS_DIR)
