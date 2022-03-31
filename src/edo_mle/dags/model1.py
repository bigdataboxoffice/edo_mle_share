import time
import logging
from pprint import pprint
from libcst import MultiplyAssign

import pendulum
import numpy as np

from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun
from edo_mle import data, files

log = logging.getLogger(__name__)


seven_days_ago = pendulum.today() - pendulum.duration(days=7)
one_day_ago = pendulum.today() - pendulum.duration(days=1)


@dag(
    schedule_interval="@daily",
    start_date=one_day_ago,
    catchup=False,
    tags=['model'],
)
def model1():
    n_cv_splits = 5
    @task(multiple_outputs=False)
    def load_data():
        iris = data.get_iris()
        data_path = files.save(iris, name="iris")
        return data_path
    
    @task(multiple_outputs=False)
    def define_splits():
        all_i = range(n_cv_splits)
        all_splits = [{"train":list(set(all_i)-{i}), "test":[i]} for i in all_i]
        return all_splits

    load_once = load_data()
    split_once = define_splits()

    # build model and prediction tasks for each cv split
    model_scores = []
    for fold in range(n_cv_splits):
        @task(multiple_outputs=False, task_id=f"model_fold_{fold}")
        def build_model_and_predict(iris_path, all_splits):
            iris = files.load(iris_path)
            xy = data.xy_species(iris)
            splits = data.extract_splits(xy, n_cv_splits, all_splits[fold])
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(multi_class='multinomial', penalty="l2", solver='lbfgs', max_iter=1e4, C=1e-6)
            train_x,train_y = splits["train"]
            test_x,test_y = splits["test"]
            model.fit(train_x, train_y)
            test_y_pred = model.predict_proba(test_x)
            from sklearn.metrics import roc_auc_score
            score = roc_auc_score(test_y, test_y_pred,  multi_class="ovo")
            return score

        model_scores += [build_model_and_predict(load_once, split_once)]
    
    # average the cv scores
    @task(task_id = "aggregate_scores")
    def aggregate_scores(model_scores):
        pprint(model_scores)
        return np.mean(model_scores)
    
    final_score = aggregate_scores(model_scores)


model1_dag = model1()

if __name__ == "__main__":
    from airflow.utils.state import State

    pprint("creating dag")
    try:
        model1_dag.clear()
    except ValueError:
        pass
    pprint("running dag")
    model1_dag.run(start_date=pendulum.today())
    pprint("dag completed")
    model1_dag
