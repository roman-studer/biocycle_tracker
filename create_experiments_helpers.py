import random
import uuid

from typing import List

import scipy.stats
import pandas as pd
import numpy as np


def load_scipy_distribution_by_name(distribution_name: str, distribution_params: dict) -> object:
    """
    Load a scipy distribution from a name and parameters.
    :param distribution_name: Name of the distribution to load.
    :param distribution_params: Parameters of the distribution to load.
    :return: The distribution.
    """
    distribution = getattr(scipy.stats, distribution_name)
    return distribution(**distribution_params)


def stratified_sampler(df: pd.DataFrame, target_column: str, n_samples: int, random_state: int = 42) -> pd.DataFrame:
    """
    Stratified sampling of a dataframe based on a target column. Returns n_samples per target column value.
    :param df: pd.DataFrame to sample from, must contain target_column in columns.
    :param target_column: str, column to sample from.
    :param n_samples: int, number of samples to take.
    :param random_state: int, random state to use.
    :return: pd.DataFrame, sampled dataframe.
    """
    return df.groupby(target_column, group_keys=False).apply(lambda x: x.sample(min(len(x), n_samples),
                                                                                random_state=random_state))


def get_experiment_lengths(distribution: object, n_samples: int, min_length: int, max_length: int) -> List[int]:
    """
    Get a list of experiment lengths based on a given distribution.
    :param distribution: scipy distribution to sample from.
    :param n_samples: Number of samples to take.
    :param min_length: Minimum length of an experiment.
    :param max_length: Maximum length of an experiment.
    :return: List of experiment lengths.
    """
    samples = distribution.rvs(size=n_samples)
    samples = np.interp(samples, (samples.min(), samples.max()), (min_length, max_length))

    return [int(sample) for sample in samples]


def get_n_uuids(n: int, random_state: int = 42) -> List[str]:
    """
    Get n uuids in hex for.
    :param n: Number of uuids to get.
    :param random_state: Random state to use.
    :return: List of uuids.
    """
    rd = random.Random()
    return [uuid.UUID(int=rd.getrandbits(random_state), version=4).hex[-8:] for _ in range(n)]


def get_experiment_ids(start_id: str, n_experiments: int, prefix: str = 'E') -> List[str]:
    """
    Get a list of experiment ids starting at start_id.
    :param start_id: Starting id. Formatted as "{prefix}0000"
    :param n_experiments: Number of experiments to get ids for.
    :param prefix: Prefix of the experiment id.
    :return: List of experiment ids.
    """
    start_id = int(start_id[1:])
    return [f'{prefix}{i:04}' for i in range(start_id, start_id + n_experiments)]
