# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Tuning routines simplify the hyperparameter optimizations and
are the recommended way of tuning hyperparameters.
"""

import copy
import numbers
import time

import getml.communication as comm
import getml.pipeline
from getml.data import Container, StarSchema, TimeSeries
from getml.pipeline import metrics
from getml.pipeline.helpers import _print_time_taken, _transform_peripheral

# -----------------------------------------------------------------------------


def _infer_score(pipeline):
    if pipeline.is_classification:
        return getml.pipeline.metrics.auc
    return getml.pipeline.metrics.rmse


# -----------------------------------------------------------------------------


def _make_final_pipeline(
    pipeline,
    tuned_feature_learners,
    tuned_predictors,
    container,
    train,
    validation,
):

    print("Building final pipeline...")
    print()

    final_pipeline = copy.deepcopy(pipeline)

    final_pipeline.feature_learners = tuned_feature_learners
    final_pipeline.predictors = tuned_predictors

    final_pipeline.fit(
        population_table=container[train], validation_table=container[validation]
    )

    final_pipeline.score(container[validation])

    return final_pipeline


# -----------------------------------------------------------------------------


def _tune(
    what,
    pipeline,
    container,
    train,
    validation,
    n_iter=111,
    score=metrics.rmse,
    num_threads=0,
):
    """
    Internal base tuning function that is called by other tuning functions.
    """

    # -----------------------------------------------------------

    pipeline = copy.deepcopy(pipeline)

    # -----------------------------------------------------------

    if isinstance(container, (StarSchema, TimeSeries)):
        container = container.container

    # -----------------------------------------------------------

    pipeline.check(container[train])

    # -----------------------------------------------------------

    if not isinstance(container, Container):
        raise TypeError(
            "'container' must be a `~getml.data.Container`, "
            + "a `~getml.data.StarSchema` or a `~getml.data.TimeSeries`"
        )

    if not isinstance(train, str):
        raise TypeError("""'train' must be a string""")

    if not isinstance(validation, str):
        raise TypeError("""'validation' must be a string""")

    if not isinstance(n_iter, numbers.Real):
        raise TypeError("""'n_iter' must be a real number""")

    if not isinstance(num_threads, numbers.Real):
        raise TypeError("""'num_threads' must be a real number""")

    # -----------------------------------------------------------

    population_table_training = container[train].population

    population_table_validation = container[validation].population

    peripheral_tables = _transform_peripheral(
        container[train].peripheral, pipeline.peripheral
    )

    # -----------------------------------------------------------

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Hyperopt.tune"

    cmd["n_iter_"] = n_iter
    cmd["num_threads_"] = num_threads
    cmd["pipeline_"] = pipeline._getml_deserialize()
    cmd["score_"] = score
    cmd["what_"] = what

    cmd["population_training_df_"] = population_table_training._getml_deserialize()
    cmd["population_validation_df_"] = population_table_validation._getml_deserialize()
    cmd["peripheral_dfs_"] = [elem._getml_deserialize() for elem in peripheral_tables]

    sock = comm.send_and_get_socket(cmd)

    # ------------------------------------------------------------

    begin = time.time()

    msg = comm.log(sock)

    end = time.time()

    # ------------------------------------------------------------

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    print()
    _print_time_taken(begin, end, "Time taken: ")

    # ------------------------------------------------------------

    pipeline_name = comm.recv_string(sock)

    return getml.pipeline.load(pipeline_name)


# -----------------------------------------------------------------------------


def _tune_feature_learner(
    feature_learner,
    pipeline,
    container,
    train,
    validation,
    n_iter,
    score,
    num_threads,
):

    if feature_learner.type == "FastProp":
        return _tune(
            "FastProp",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "Multirel":
        return _tune(
            "Multirel",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "Relboost":
        return _tune(
            "Relboost",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    if feature_learner.type == "RelMT":
        return _tune(
            "RelMT",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    raise ValueError("Unknown feature learner: " + feature_learner.type + "!")


# -----------------------------------------------------------------------------


def _tune_predictor(
    predictor,
    pipeline,
    container,
    train,
    validation,
    n_iter,
    score,
    num_threads,
):

    if "XGBoost" in predictor.type:
        return _tune(
            "XGBoost",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    if "Regression" in predictor.type:
        return _tune(
            "Linear",
            pipeline,
            container,
            train,
            validation,
            n_iter,
            score,
            num_threads,
        )

    raise ValueError("Unknown predictor: '" + predictor.type + "'!")


# -----------------------------------------------------------------------------


def tune_feature_learners(
    pipeline,
    container,
    train="train",
    validation="validation",
    n_iter=0,
    score=None,
    num_threads=0,
):
    """
    A high-level interface for optimizing the feature learners of a
    :class:`~getml.pipelines.Pipeline`.

    Efficiently optimizes the hyperparameters for the set of feature learners
    (from :mod:`~getml.feature_learning`) of a given pipeline by breaking each
    feature learner's hyperparameter space down into :ref:`carefully curated
    subspaces<hyperopt_tuning_subspaces>` and optimizing the hyperparameters for
    each subspace in a sequential multi-step process.  For further details about
    the actual recipes behind the tuning routines refer
    to :ref:`tuning routines<hyperopt_tuning>`.

    Args:
        pipeline (:class:`~getml.Pipeline`):
            Base pipeline used to derive all models fitted and scored
            during the hyperparameter optimization. It defines the data
            schema and any hyperparameters that are not optimized.

        container (:class:`~getml.data.Container`):
            The data container used for the hyperparameter tuning.

        train (str, optional):
            The name of the subset in 'container' used for training.

        validation (str, optional):
            The name of the subset in 'container' used for validation.

        n_iter (int, optional):
            The number of iterations.

        score (str, optional):
            The score to optimize. Must be from
            :mod:`~getml.pipeline.metrics`.

        num_threads (int, optional):
            The number of parallel threads to use. If set to 0,
            the number of threads will be inferred.

    Example:
        We assume that you have already set up your
        :class:`~getml.Pipeline` and
        :class:`~getml.data.Container`.

        .. code-block:: python

            tuned_pipeline = getml.hyperopt.tune_predictors(
                pipeline=base_pipeline,
                container=container)

    Returns:
        A :class:`~getml.Pipeline` containing tuned versions
        of the feature learners.
    """

    if not isinstance(pipeline, getml.pipeline.Pipeline):
        raise TypeError("'pipeline' must be a pipeline!")

    pipeline._validate()

    if not score:
        score = _infer_score(pipeline)

    tuned_feature_learners = []

    for feature_learner in pipeline.feature_learners:
        tuned_pipeline = _tune_feature_learner(
            feature_learner=feature_learner,
            pipeline=pipeline,
            container=container,
            train=train,
            validation=validation,
            n_iter=n_iter,
            score=score,
            num_threads=num_threads,
        )

        assert (
            len(tuned_pipeline.feature_learners) == 1
        ), "Expected exactly one feature learner!"

        tuned_feature_learners.append(tuned_pipeline.feature_learners[0])

    return _make_final_pipeline(
        pipeline,
        tuned_feature_learners,
        copy.deepcopy(pipeline.predictors),
        container,
        train,
        validation,
    )


# -----------------------------------------------------------------------------


def tune_predictors(
    pipeline,
    container,
    train="train",
    validation="validation",
    n_iter=0,
    score=None,
    num_threads=0,
):
    """
    A high-level interface for optimizing the predictors of a
    :class:`getml.Pipeline`.

    Efficiently optimizes the hyperparameters for the set of predictors (from
    :mod:`getml.predictors`) of a given pipeline by breaking each predictor's
    hyperparameter space down into :ref:`carefully curated
    subspaces<hyperopt_tuning_subspaces>` and optimizing the hyperparameters for
    each subspace in a sequential multi-step process.  For further details about
    the actual recipes behind the tuning routines refer to
    :ref:`tuning routines<hyperopt_tuning>`.

    Args:
        pipeline (:class:`~getml.Pipeline`):
            Base pipeline used to derive all models fitted and scored
            during the hyperparameter optimization. It defines the data
            schema and any hyperparameters that are not optimized.

        container (:class:`~getml.data.Container`):
            The data container used for the hyperparameter tuning.

        train (str, optional):
            The name of the subset in 'container' used for training.

        validation (str, optional):
            The name of the subset in 'container' used for validation.

        n_iter (int, optional):
            The number of iterations.

        score (str, optional):
            The score to optimize. Must be from
            :mod:`~getml.pipeline.metrics`.

        num_threads (int, optional):
            The number of parallel threads to use. If set to 0,
            the number of threads will be inferred.

    Example:
        We assume that you have already set up your
        :class:`~getml.Pipeline` and
        :class:`~getml.data.Container`.

        .. code-block:: python

            tuned_pipeline = getml.hyperopt.tune_predictors(
                pipeline=base_pipeline,
                container=container)

    Returns:
        A :class:`~getml.Pipeline` containing tuned
        predictors.
    """

    if not isinstance(pipeline, getml.pipeline.Pipeline):
        raise TypeError("'pipeline' must be a pipeline!")

    pipeline._validate()

    if not score:
        score = _infer_score(pipeline)

    tuned_predictors = []

    for predictor in pipeline.predictors:
        tuned_pipeline = _tune_predictor(
            predictor=predictor,
            pipeline=pipeline,
            container=container,
            train=train,
            validation=validation,
            n_iter=n_iter,
            score=score,
            num_threads=num_threads,
        )

        assert len(tuned_pipeline.predictors) == 1, "Expected exactly one predictor!"

        tuned_predictors.append(tuned_pipeline.predictors[0])

    return _make_final_pipeline(
        pipeline,
        copy.deepcopy(pipeline.feature_learners),
        tuned_predictors,
        container,
        train,
        validation,
    )
