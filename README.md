# Environment setup

```sh
conda env create --file environment.yml
```

# Activate the environment and configure/run the model1 dag

```sh
conda activate edo_mle
./run.sh
```

The first time it's run, `run.sh` will initialize the airflow environment (and SQLite database) in the `./airflow` folder.

`run.sh` runs airflow in standalone mode after setting various environment variables. Once it's started, the `model1` dag should appear in http://localhost:8080/home and you should be able to run it.



After you've run `run.sh` at least once to initialize sqlite, you can exit it (ctrl-c in the terminal it's running) and run `model1` in debug mode using

```
# be sure you're running in the edo_mle conda environment
./debug.sh
```

# Forcing everything to reset
If you delete `./airflow/airflow.db`, rerunning `run.sh` will re-initialize airflow completely

```sh
rm ./airflow/airflow.db
./run.sh
```

# Cleaning up

Remove the `edo_mle` conda environment.
```sh
conda deactivate
conda remove --name edo_mle --all
```

Delete the git repository (this folder).
