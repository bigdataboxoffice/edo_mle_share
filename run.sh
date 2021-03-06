#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# load envars
. "${SCRIPT_DIR}/envars.sh"

# actually run airflow
airflow standalone
