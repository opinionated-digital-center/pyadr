import pytest

from pyadr.const import ADR_REPO_REL_PATH


@pytest.fixture()
def adr_tmp_path(tmp_path):
    path = tmp_path / ADR_REPO_REL_PATH
    path.mkdir(parents=True)
    return path
