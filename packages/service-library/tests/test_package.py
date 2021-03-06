# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

import os
import re
from pathlib import Path

import pytest
from servicelib.utils import is_osparc_repo_dir, search_osparc_repo_dir
from pytest_simcore.helpers.utils_pylint import assert_pylint_is_passing


@pytest.fixture
def pylintrc(osparc_simcore_root_dir):
    pylintrc = osparc_simcore_root_dir / ".pylintrc"
    assert pylintrc.exists()
    return pylintrc


def test_run_pylint(pylintrc, package_dir):
    assert_pylint_is_passing(pylintrc=pylintrc, package_dir=package_dir)


def test_no_pdbs_in_place(package_dir):
    # TODO: add also test_dir excluding this function!?
    # TODO: it can be commented!
    # TODO: add check on other undesired code strings?!
    MATCH = re.compile(r"pdb.set_trace()")
    EXCLUDE = ["__pycache__", ".git"]
    for root, dirs, files in os.walk(package_dir):
        for name in files:
            if name.endswith(".py"):
                pypth = Path(root) / name
                code = pypth.read_text()
                found = MATCH.findall(code)
                # TODO: should return line number
                assert not found, "pbd.set_trace found in %s" % pypth
        dirs[:] = [d for d in dirs if d not in EXCLUDE]


def test_utils(osparc_simcore_root_dir, package_dir):
    assert is_osparc_repo_dir(osparc_simcore_root_dir)

    assert search_osparc_repo_dir(osparc_simcore_root_dir) == osparc_simcore_root_dir

    # assert not search_osparc_repo_dir(package_dir), "package is installed, should not be in osparc-repo"
    # assert search_osparc_repo_dir(package_dir) == osparc_simcore_root_dir, "in develop mode"

    assert not search_osparc_repo_dir(osparc_simcore_root_dir.parent)
