#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated NIH CXR14-PadChest dataset"""

from ..configs.datasets.nih_cxr14_re_pc import idiap as nih_pc
from ..configs.datasets.nih_cxr14_re import default as nih
from ..configs.datasets.padchest import no_tb_idiap as pc
import pytest

@pytest.mark.skip_if_rc_var_not_set('bob.med.tb.padchest.datadir')
@pytest.mark.skip_if_rc_var_not_set('bob.med.tb.nih_cxr14_re.datadir')
def test_dataset_consistency():

    # Default protocol
    nih_pc_dataset = nih_pc.dataset
    assert isinstance(nih_pc_dataset, dict)

    nih_dataset = nih.dataset
    pc_dataset = pc.dataset

    assert "train" in nih_pc_dataset
    assert len(nih_pc_dataset["train"]) == len(nih_dataset["train"]) + len(pc_dataset["train"])

    assert "validation" in nih_pc_dataset
    assert len(nih_pc_dataset["validation"]) == len(nih_dataset["validation"]) + len(pc_dataset["validation"])
