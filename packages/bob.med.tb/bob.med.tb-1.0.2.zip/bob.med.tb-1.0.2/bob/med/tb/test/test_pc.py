#!/usr/bin/env python
# coding=utf-8


"""Tests for Padchest dataset"""

from ..data.padchest import dataset
import pytest

def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("idiap")
    assert len(subset) == 1

    assert "train" in subset
    assert len(subset["train"]) == 96269

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    # Cross-validation 2
    subset = dataset.subsets("tb_idiap")
    assert len(subset) == 2

    assert "train" in subset
    assert len(subset["train"]) == 200

    # Check labels
    for s in subset["train"]:
        assert s.label in [0.0, 1.0]

    assert "test" in subset
    assert len(subset["test"]) == 50

    # Check labels
    for s in subset["test"]:
        assert s.label in [0.0, 1.0]

    # Cross-validation 3
    subset = dataset.subsets("no_tb_idiap")
    assert len(subset) == 2

    assert "train" in subset
    assert len(subset["train"]) == 54371

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    assert "validation" in subset
    assert len(subset["validation"]) == 4052

    # Check labels
    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

@pytest.mark.skip_if_rc_var_not_set('bob.med.tb.padchest.datadir')
def test_check():
    assert dataset.check() == 0
