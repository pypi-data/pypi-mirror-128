#!/usr/bin/env python
# coding=utf-8


"""Tests for NIH CXR14 dataset"""

from ..data.nih_cxr14_re import dataset
import pytest


def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("default")
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == 98637
    for s in subset["train"]:
        assert s.key.startswith("images/000")

    assert "validation" in subset
    assert len(subset["validation"]) == 6350
    for s in subset["validation"]:
        assert s.key.startswith("images/000")

    assert "test" in subset
    assert len(subset["test"]) == 4054
    for s in subset["test"]:
        assert s.key.startswith("images/000")

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["test"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    # Idiap protocol
    subset = dataset.subsets("idiap")
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == 98637
    for s in subset["train"]:
        assert s.key.startswith("images/000")

    assert "validation" in subset
    assert len(subset["validation"]) == 6350
    for s in subset["validation"]:
        assert s.key.startswith("images/000")

    assert "test" in subset
    assert len(subset["test"]) == 4054
    for s in subset["test"]:
        assert s.key.startswith("images/000")

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["test"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]


@pytest.mark.skip_if_rc_var_not_set("bob.med.tb.nih_cxr14_re.datadir")
def test_loading():
    def _check_size(size):
        if size == (1024, 1024):
            return True
        return False

    def _check_sample(s):

        data = s.data
        assert isinstance(data, dict)
        assert len(data) == 2

        assert "data" in data
        assert _check_size(data["data"].size)  # Check size
        assert data["data"].mode == "RGB"  # Check colors

        assert "label" in data
        assert len(data["label"]) == 14  # Check labels

    limit = 30  # use this to limit testing to first images only, else None

    subset = dataset.subsets("default")
    for s in subset["train"][:limit]:
        _check_sample(s)
