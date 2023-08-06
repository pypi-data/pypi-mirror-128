#!/usr/bin/env python
# coding=utf-8


"""Tests for Extended Padchest dataset"""

from ..data.padchest_RS import dataset


def test_protocol_consistency():

    # tb_idiap protocol
    subset = dataset.subsets("tb_idiap")
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == 160

    assert "validation" in subset
    assert len(subset["validation"]) == 40

    assert "test" in subset
    assert len(subset["test"]) == 50

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
        assert data["label"] in [0.0, 1.0]  # Check labels

    limit = 30  # use this to limit testing to first images only, else None

    subset = dataset.subsets("tb_idiap")
    for s in subset["train"][:limit]:
        _check_sample(s)
