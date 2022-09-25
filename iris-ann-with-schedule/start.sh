#!/bin/bash

# Dataset and Model
model_dir="./project/model"
artefact_dir="./project/model"

# Requirements
requirements="./project/requirements.txt"

# Airflow
data_dir="./airflow/data"
logs_dir="./airflow/logs"
plugins_dir="./airflow/plugins"

choose=${1}

serve() {
    if [[ ! -d ${model_dir} ]]; then
        echo "[ERROR] The model directory not Found. Please execute \"make build\" first!"
        exit
    fi

    if [[ ! -d ${artefact_dir} ]]; then
        echo "[ERROR] The artefact directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    echo "[DEBUG] Start the model serving test.."
    cd project && python endpoint.py
}

train() {
    if [[ ! -d ${model_dir} ]]; then
        echo "[ERROR] The model directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    if [[ ! -d ${artefact_dir} ]]; then
        echo "[ERROR] The artefact directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    echo "[DEBUG] Start the model training test.."
    cd project && python train.py
}

airflow() {
    if [[ ! -d ${data_dir} ]]; then
        echo "[ERROR] The data directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    if [[ ! -d ${logs_dir} ]]; then
        echo "[ERROR] The logs directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    if [[ ! -d ${plugins_dir} ]]; then
        echo "[ERROR] The plugins directory not Found. Please execute \"make build\" first!!"
        exit
    fi

    echo "[DEBUG] Start the model serving test.."
    cd airflow && docker-compose up --build --detach
}

model() {
    docker_requirements_dir="./docker"

    if [[ ! -f ${requirements} ]]; then
        echo "[ERROR] The requirement file not Found. Please copy the lates \"requirements.txt\" to \"${requirements}\"!"
        exit
    else
        echo "[DEBUG] Copying the lates \"requirements.txt\" file.."
        cp ${requirements} ${docker_requirements_dir}
    fi

    if [[ ! -d ${model_dir} ]]; then
        echo "[ERROR] The model directory not Found. Please execute \"make build\" first!"
        exit
    fi

    if [[ ! -d ${artefact_dir} ]]; then
        echo "[ERROR] The artefact directory not Found. Please execute \"make build\" first!"
        exit
    fi

    echo "[DEBUG] Start to composing the docker.."
    docker-compose --file docker-compose.yml up --build --detach
}

case ${choose} in
    serve)
        serve
        ;;
    train)
        train
        ;;
    model)
        model
        ;;
    airflow)
        airflow
        ;;
    *) 
        echo "[ERROR] Your input not recognized. Please choose demo, train, or serve!"
        ;;
esac
