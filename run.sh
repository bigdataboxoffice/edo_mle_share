#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

export AIRFLOW_HOME="${SCRIPT_DIR}/airflow_storage"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__EXECUTOR=DebugExecutor
export AIRFLOW__DEBUG__FAIL_FAST=True
DAGS_FOLDER="${SCRIPT_DIR}/src/edo_mle/dags"

mkdir -p "$AIRFLOW_HOME"
ln -sfn "$DAGS_FOLDER" "$AIRFLOW_HOME/dags"
# DB_FILE is something that exists only if airflow db has been initialied
DB_FILE="${AIRFLOW_HOME}/airflow.db"
if [ ! -f "$DB_FILE" ]; then
    airflow db init
    airflow users create \
        --role Admin --username admin --password admin \
        --email EMAIL --firstname ADMIN --lastname USER
fi

python3 -m airflow_storage.dags.model1 


