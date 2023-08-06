#!/usr/bin/env python
# coding=utf-8


"""Tests for Extended Shenzhen dataset"""

from ..data.shenzhen_RS import dataset


def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("default")
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == 422

    assert "validation" in subset
    assert len(subset["validation"]) == 107

    assert "test" in subset
    assert len(subset["test"]) == 133
    for s in subset["test"]:
        assert s.key.startswith("CXR_png/CHNCXR_0")

    # Check labels
    for s in subset["train"]:
        assert s.label in [0.0, 1.0]

    for s in subset["validation"]:
        assert s.label in [0.0, 1.0]

    for s in subset["test"]:
        assert s.label in [0.0, 1.0]

    # Cross-validation folds 0-1
    for f in range(2):
        subset = dataset.subsets("fold_" + str(f))
        assert len(subset) == 3

        assert "train" in subset
        assert len(subset["train"]) == 476
        for s in subset["train"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        assert "validation" in subset
        assert len(subset["validation"]) == 119
        for s in subset["validation"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        assert "test" in subset
        assert len(subset["test"]) == 67
        for s in subset["test"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]

        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]

        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

    # Cross-validation folds 2-9
    for f in range(2, 10):
        subset = dataset.subsets("fold_" + str(f))
        assert len(subset) == 3

        assert "train" in subset
        assert len(subset["train"]) == 476
        for s in subset["train"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        assert "validation" in subset
        assert len(subset["validation"]) == 120
        for s in subset["validation"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        assert "test" in subset
        assert len(subset["test"]) == 66
        for s in subset["test"]:
            assert s.key.startswith("CXR_png/CHNCXR_0")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]

        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]

        for s in subset["test"]:
            assert s.label in [0.0, 1.0]


def test_loading():
    def _check_sample(s):

        data = s.data

        assert isinstance(data, dict)
        assert len(data) == 2

        assert "data" in data
        assert len(data["data"]) == 14  # Check radiological signs

        assert "label" in data
        assert data["label"] in [0, 1]  # Check labels

    limit = 30  # use this to limit testing to first images only, else None

    subset = dataset.subsets("default")
    for s in subset["train"][:limit]:
        _check_sample(s)
