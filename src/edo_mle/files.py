import os
import pickle

from airflow.configuration import get_airflow_home
from airflow.operators.python import get_current_context


def root_dir():
    home = get_airflow_home()
    return f"{home}/data"


def run_dir():
    context = get_current_context()
    run_id = context["run_id"]
    return f"{root_dir()}/{run_id}"


def task_dir():
    context = get_current_context()
    task_key = context["task_instance_key_str"]
    return f"{root_dir()}/{task_key}"


def save(x, name):
    dirname = task_dir()
    os.makedirs(dirname, exist_ok=True)
    filename = f"{dirname}/{name}.pkl"
    with open(filename, "wb") as f:
        pickle.dump(x, f)
    return filename


def load(path):
    with open(path, "rb") as f:
        res = pickle.load(f)
    return res
