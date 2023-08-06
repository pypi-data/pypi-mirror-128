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
Collection of functions for simulating the effects of staging,
not meant to be used by the end user.
"""

from .relationship import many_to_one, one_to_one, _all_relationships

# ------------------------------------------------------------------


def _compare_join(join1, join2):
    return (
        (join1.right.name == join2.right.name)
        and (join1.on == join2.on)
        and (join1.time_stamps == join2.time_stamps)
        and (join1.upper_time_stamp == join2.upper_time_stamp)
        and (join1.relationship == join2.relationship)
        and (join1.memory == join2.memory)
        and (join1.horizon == join2.horizon)
        and (join1.lagged_targets == join2.lagged_targets)
    )


# ------------------------------------------------------------------


def _compare_joins(pair1, pair2):
    return all([_compare_join(j1, j2) for (j1, j2) in zip(pair1[1], pair2[1])])


# ------------------------------------------------------------------


def _is_same(pair1, pair2):
    if pair1[0] != pair2[0]:
        return False

    if not _compare_joins(pair1, pair2):
        return False

    return True


# ------------------------------------------------------------------


def _is_to_one(relationship):
    if relationship not in _all_relationships:
        raise ValueError(
            "'relationship' must be from getml.data.relationship, "
            + "meaning it must be one of the following: "
            + str(_all_relationships)
            + "."
        )
    return relationship in [many_to_one, one_to_one]


# ------------------------------------------------------------------


def _make_names(placeholder):
    return [placeholder.name] + [
        name
        for j in placeholder.joins
        if _is_to_one(j.relationship)
        for name in _make_names(j.right)
    ]


# ------------------------------------------------------------------


def _make_joins(placeholder):
    return [join for join in placeholder.joins if _is_to_one(join.relationship)] + [
        subjoin
        for join in placeholder.joins
        if _is_to_one(join.relationship)
        for subjoin in _make_joins(join.right)
    ]


# ------------------------------------------------------------------


def _make_pair(placeholder):
    names = _make_names(placeholder)
    joins = _make_joins(placeholder)
    assert len(names) == len(joins) + 1, "Lengths don't match"
    return (names, joins)


# ------------------------------------------------------------------


def _make_list_of_pairs(placeholder, include_head=True):
    head = [_make_pair(placeholder)] if include_head else []
    return head + [
        lis
        for j in placeholder.joins
        for lis in _make_list_of_pairs(j.right, not _is_to_one(j.relationship))
    ]


# ------------------------------------------------------------------


def _make_staging_overview(placeholder):
    list_of_pairs = _make_list_of_pairs(placeholder)
    peripheral = list_of_pairs[1:]
    peripheral.sort(key=lambda l: l[0][0])
    peripheral = _remove_duplicates(peripheral)
    list_of_names = [list_of_pairs[0][0]] + [p[0] for p in peripheral]
    return [
        [", ".join(lis), lis[0].upper() + "__STAGING_TABLE_" + str(i + 1)]
        for (i, lis) in enumerate(list_of_names)
    ]


# ------------------------------------------------------------------


def _remove_duplicates(sorted_list_of_pairs):
    if not sorted_list_of_pairs:
        return []

    if len(sorted_list_of_pairs) == 1:
        return sorted_list_of_pairs

    head = sorted_list_of_pairs[0]

    tail = sorted_list_of_pairs[1:]

    if _is_same(head, tail[0]):
        return _remove_duplicates(tail)

    return [head] + _remove_duplicates(tail)


# ------------------------------------------------------------------
