#!/bin/bash

# Container controll script
chmod +x ./start.sh
chmod +x ./postgres/start-postgres.sh
chmod +x ./postgres/stop-postgres.sh
chmod +x ./airflow/start-airflow.sh
chmod +x ./airflow/stop-airflow.sh

# Installer script
chmod +x ./docker/scripts/install.sh

chmod -R 777 ./project