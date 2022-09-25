#!/bin/bash

# Dataset and Model
model_dir="./project/model"
artefact_dir="./project/output"


if [[ ! -d ${model_dir} ]]; then
    echo "[ERROR] The model directory not Found. Please execute \"make build\" command first!"
    exit
fi

if [[ ! -d ${artefact_dir} ]]; then
    echo "[ERROR] The artefact directory not Found. Please execute \"make build\" command first!"
    exit
fi

echo "[DEBUG] Start the model training test.."
cd project
python train.py
