# Environment setup

```sh
conda env create --file environment.yml
```

# Activate the environment and configure/run the model1 dag

```sh
conda activate edo_mle
./run.sh
```

The first time it's run, `run.sh` will initialize the airflow environment (and SQLite database) in the `./airflow_storage` folder.


In another shell, start the airflow webserver

```sh
# NOTE: must run this in the git repo root, or adjust AIRFLOW_HOME to point to the absolute path of ./airflow_storage
AIRFLOW_HOME="$(pwd)/airflow_storage" airflow scheduler
```

You can then log into the airflow UI at http://localhost:8080 as admin/admin.

# Forcing everything to reset
If you delete `./airflow_storage`, rerunning `run.sh` will re-initialize airflow completely

```sh
rm -r ./airflow_storage/
./run.sh
```

# Cleaning up

Remove the `edo_mle` conda environment.
```sh
conda deactivate
conda remove --name edo_mle --all
```

Delete the git repository (this folder).
