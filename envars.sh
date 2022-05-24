#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

export AIRFLOW_HOME="${SCRIPT_DIR}/airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER="${SCRIPT_DIR}/src/edo_mle/dags"

# needed to dodge https://github.com/apache/airflow/issues/12808#issuecomment-738854764
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
