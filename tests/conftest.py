from pathlib import Path

import pytest
from git import Repo

from pyadr.const import ADR_REPO_REL_PATH


@pytest.fixture()
def adr_tmp_path(tmp_path):
    path = tmp_path / ADR_REPO_REL_PATH
    path.mkdir(parents=True)
    return path


@pytest.fixture()
def tmp_repo(tmp_path):
    repo = Repo.init(tmp_path)

    file = Path(tmp_path / "foo")
    file.touch()

    repo.index.add([str(file)])
    repo.index.commit("initial commit")

    return repo
