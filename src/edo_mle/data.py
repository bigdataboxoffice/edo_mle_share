from functools import cache
from typing import Dict, Set, Tuple, TypeVar

import numpy as np
import numpy.typing as npt
import pandas as pd


@cache
def get_iris() -> pd.DataFrame:
    csv_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    cols = {
        "sepal_length": np.float32,
        "sepal_width": np.float32,
        "petal_length": np.float32,
        "petal_width": np.float32,
        "species": pd.CategoricalDtype(),
    }
    iris = pd.read_csv(csv_url, names=list(cols), dtype=cols)
    iris["orig_row"] = np.arange(len(iris))
    return iris


def xy_species(iris=None) -> Tuple[pd.DataFrame, pd.Series]:
    iris = iris if iris is not None else get_iris()
    target = iris["species"]
    data = iris.drop("species", axis=1)
    return data, target


def cv_splits(n, k, seed):
    assignments = np.arange(n) % k
    randomizer = np.random.default_rng(seed)
    randomizer.shuffle(assignments)
    return assignments


XYDF = Tuple[pd.DataFrame, pd.Series]
IntArray = npt.NDArray[np.int_]
T = TypeVar("T")


def extract_splits(
    xy: XYDF, n_splits: int, this_split: Dict[T, Set[int]]
) -> Dict[T, Tuple[XYDF, XYDF]]:
    """
    Generator that returns (x,y) tuples for each cv split.
    where cv splits are defined by a dictionary that tells the indices to keep
    """
    x, y = xy
    i = cv_splits(len(x), n_splits, 1234)
    results: Dict[T, Tuple[XYDF, XYDF]] = dict()
    for label, set_of_i_to_keep in this_split.items():
        should_keep_row = np.isin(i, list(set_of_i_to_keep))
        kept_x = x[should_keep_row]
        kept_y = y[should_keep_row]
        results[label] = (kept_x, kept_y)
    return results
