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
Conducts a cross validation.
"""

from copy import deepcopy

from getml.pipeline import Pipeline
from getml.data import DataFrame, View
from getml.data.split import random
from getml.pipeline.scores_container import Scores


def cross_validation(pipeline, population, peripheral, n_folds=10, seed=5849):
    """
    Conducts a cross validation.
    """

    if not isinstance(pipeline, Pipeline):
        raise TypeError("'pipeline' must be a pipeline.")

    if not isinstance(population, (DataFrame, View)):
        raise TypeError("'pipeline' must be a pipeline.")

    if not isinstance(n_folds, int):
        raise TypeError("'n_folds' must be an integer.")

    if n_folds < 2:
        raise ValueError("'n_folds' must be >= 2.")

    # peripheral will be typechecked by pipeline .fit(...).
    # No need to duplicate code.

    kwargs = {
        "fold " + str(i + 1).zfill(len(str(n_folds))): (1.0 / float(n_folds))
        for i in range(n_folds)
    }

    split = random(seed=seed, train=0.0, test=0.0, validation=0.0, **kwargs)

    scores_objects = []

    for fold in list(kwargs.keys()):
        print(fold + ":")
        print()
        train_set = population[split != fold].with_name(
            "cross validation: train - " + fold
        )
        validation_set = population[split == fold].with_name(
            "cross validation: validation - " + fold
        )
        pipe = deepcopy(pipeline)
        pipe.tags += ["cross validation", fold]
        pipe.fit(train_set, peripheral)
        scores_objects.append(pipe.score(validation_set, peripheral))
        print()

    scores_data = [d for obj in scores_objects for d in obj.data]

    return Scores(data=scores_data, latest=scores_objects[-1]._latest).sort(
        key=lambda score: score.set_used, descending=False
    )
