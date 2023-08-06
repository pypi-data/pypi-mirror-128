#!/usr/bin/env python
# coding=utf-8


"""Tests for Montgomery dataset"""

import pytest
from ..data.montgomery import dataset

def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("default")
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == 88
    for s in subset["train"]:
        assert s.key.startswith("CXR_png/MCUCXR_0")

    assert "validation" in subset
    assert len(subset["validation"]) == 22
    for s in subset["validation"]:
        assert s.key.startswith("CXR_png/MCUCXR_0")

    assert "test" in subset
    assert len(subset["test"]) == 28
    for s in subset["test"]:
        assert s.key.startswith("CXR_png/MCUCXR_0")

    # Check labels
    for s in subset["train"]:
        assert s.label in [0.0, 1.0]

    for s in subset["validation"]:
        assert s.label in [0.0, 1.0]

    for s in subset["test"]:
        assert s.label in [0.0, 1.0]

    # Cross-validation fold 0-7
    for f in range(8):
        subset = dataset.subsets("fold_"+str(f))
        assert len(subset) == 3

        assert "train" in subset
        assert len(subset["train"]) == 99
        for s in subset["train"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        assert "validation" in subset
        assert len(subset["validation"]) == 25
        for s in subset["validation"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        assert "test" in subset
        assert len(subset["test"]) == 14
        for s in subset["test"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]

        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]

        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

    # Cross-validation fold 8-9
    for f in range(8, 10):
        subset = dataset.subsets("fold_"+str(f))
        assert len(subset) == 3

        assert "train" in subset
        assert len(subset["train"]) == 100
        for s in subset["train"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        assert "validation" in subset
        assert len(subset["validation"]) == 25
        for s in subset["validation"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        assert "test" in subset
        assert len(subset["test"]) == 13
        for s in subset["test"]:
            assert s.key.startswith("CXR_png/MCUCXR_0")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]

        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]

        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

@pytest.mark.skip_if_rc_var_not_set('bob.med.tb.montgomery.datadir')
def test_loading():

    image_size_portrait = (4020, 4892)
    image_size_landscape = (4892, 4020)

    def _check_size(size):
        if size == image_size_portrait:
            return True
        elif size == image_size_landscape:
            return True
        return False

    def _check_sample(s):

        data = s.data
        assert isinstance(data, dict)
        assert len(data) == 2

        assert "data" in data
        assert _check_size(data["data"].size) # Check size
        assert data["data"].mode == "L" # Check colors

        assert "label" in data
        assert data["label"] in [0, 1] # Check labels

    limit = 30  #use this to limit testing to first images only, else None

    subset = dataset.subsets("default")
    for s in subset["train"][:limit]:
        _check_sample(s)

@pytest.mark.skip_if_rc_var_not_set('bob.med.tb.montgomery.datadir')
def test_check():
    assert dataset.check() == 0
