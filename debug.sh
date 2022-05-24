#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# load envars
. "${SCRIPT_DIR}/envars.sh"

export AIRFLOW__CORE__EXECUTOR=DebugExecutor
export AIRFLOW__DEBUG__FAIL_FAST=True

# debug the model
python -m edo_mle.dags.model1
