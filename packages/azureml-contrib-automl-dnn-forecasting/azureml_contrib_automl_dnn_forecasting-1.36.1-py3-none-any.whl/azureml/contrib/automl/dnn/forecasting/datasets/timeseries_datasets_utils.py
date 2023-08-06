# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for creating training dataset from dapaprep Dataflow object."""
from typing import Any, Optional

import pandas as pd
from azureml.contrib.automl.dnn.forecasting.wrapper import _wrapper_util

from ..constants import ForecastConstant, TCNForecastParameters
from ..types import DataInputType, TargetInputType
from .timeseries_datasets import TimeSeriesDataset


def create_timeseries_dataset(X_train: DataInputType,
                              y_train: TargetInputType,
                              X_valid: DataInputType,
                              y_valid: TargetInputType,
                              horizon: int,
                              step: int = 1,
                              has_past_regressors: bool = False,
                              one_hot: bool = False,
                              save_last_lookback_data: bool = False,
                              min_grain_for_embedding:
                              int = TCNForecastParameters.MIN_GRAIN_SIZE_FOR_EMBEDDING_DEFAULT,
                              grain_feature_col_prefix: Optional[str] = None,
                              **settings: Any) -> TimeSeriesDataset:
    """
    Create a timeseries dataset.

    :param X_train: Training features in DataPrep DataFlow form(numeric data of shape(row_count, feature_count).
    :param y_train: Training label in DataPrep DataFlow for with shape(row_count, 1).
    :param X_valid: Training features in DataPrep DataFlow form(numeric data of shape(row_count, feature_count).
    :param y_valid: Training label in DataPrep DataFlow for with shape(row_count, 1).
    :param horizon: Number of time steps to forecast.
    :param step: Time step size between consecutive examples.
    :param has_past_regressors: data to populate past regressors for each sample
    :param one_hot: one_hot encode or not
    :param save_last_lookback_data: to save the last lookbackup items for future inferene when contsxt missing.
    :param min_grain_for_embedding: number of samples in the grain to enable embedding.
    :param grain_feature_col_prefix: prefix column name of transformed grains.
    :param settings: automl timeseries settings
    """
    X_df, y_df = _wrapper_util.convert_X_y_to_pandas(X_train, y_train)
    if X_valid is not None:
        X_valid_df, y_valid_df = _wrapper_util.convert_X_y_to_pandas(X_valid, y_valid)
        settings[ForecastConstant.cross_validations] = 1
        X_df = pd.concat([X_df, X_valid_df], axis=0)
        y_df = pd.concat([y_df, y_valid_df], axis=0)

    return TimeSeriesDataset(X_df,
                             y_df,
                             horizon,
                             step,
                             has_past_regressors=has_past_regressors,
                             one_hot=one_hot,
                             save_last_lookback_data=save_last_lookback_data,
                             min_grain_for_embedding=min_grain_for_embedding,
                             grain_feature_col_prefix=grain_feature_col_prefix,
                             **settings)
