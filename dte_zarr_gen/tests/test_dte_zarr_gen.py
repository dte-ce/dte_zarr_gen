#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dte_zarr_gen` package."""

__author__ = """Philip Kershaw"""
__contact__ = 'philip.kershaw@stfc.ac.uk'
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "y"
import os

import pytest
from click.testing import CliRunner

from dte_zarr_gen import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert 'Usage: ' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Usage: ' in help_result.output

    test_data_dir = os.path.join(cli.THIS_DIR, 'tests', 'data')

    cl_args = [
        "-f", os.path.join(test_data_dir,
            "tasmax_day_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_19500101-19991230.nc"),
        "-n", "tasmax",
        "-u", "http://esa-dte-o.s3.jc.rl.ac.uk/",
        "-b", "pjk_test2",
        "-o", "tasmax_day_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_19500101-19991230.zarr",
        "-c", os.path.join(test_data_dir, "creds.json")
    ]
    run_result = runner.invoke(cli.main, cl_args)
    assert run_result.exit_code == 0


if __name__ == '__main__':
    pytest.main()