from pathlib import Path

import pytest
from git import Repo

import pyadr
from pyadr.config import config
from pyadr.const import DEFAULT_ADR_PATH, DEFAULT_CONFIG_FILE_PATH


@pytest.fixture()
def adr_tmp_path(tmp_path):
    path = tmp_path / DEFAULT_ADR_PATH
    path.mkdir(parents=True)
    yield path


@pytest.fixture()
def tmp_repo(tmp_path):
    repo = Repo.init(tmp_path)

    file = Path(tmp_path / "foo")
    file.touch()

    repo.index.add([str(file)])
    repo.index.commit("initial commit")

    yield repo


@pytest.fixture(autouse=True)
def initialise_config(monkeypatch, tmp_path):
    monkeypatch.setattr(
        pyadr.config.config.parser,
        "config_file_path",
        tmp_path / DEFAULT_CONFIG_FILE_PATH,
    )
    assert (
        pyadr.config.config.parser.config_file_path
        == tmp_path / DEFAULT_CONFIG_FILE_PATH
    )
    config.parser["adr"] = {}
