from pathlib import Path

from pyadr.content_utils import (
    adr_title_slug_from_content_stream,
    update_adr_content_title_status,
)
from pyadr.exceptions import PyadrNoNumberedAdrError


def rename_reviewed_adr_file(file: Path, adr_repo_path) -> Path:
    next_id = calculate_next_id(adr_repo_path)
    with file.open() as f:
        title_slug = adr_title_slug_from_content_stream(f)

    renamed_file = file.with_name("-".join([next_id, title_slug]) + file.suffix)
    file.rename(renamed_file)
    return renamed_file


def update_adr_title_status(file: Path, title: str = None, status: str = None) -> None:
    with file.open() as f:
        updated_content = update_adr_content_title_status(
            f.read(), title=title, status=status
        )
    with file.open("w") as f:
        f.write(updated_content)


def calculate_next_id(adr_path):
    reviewed_adrs = sorted(adr_path.glob("[0-9][0-9][0-9][0-9]-*"))
    if not len(reviewed_adrs):
        raise PyadrNoNumberedAdrError()
    most_recent_adr = reviewed_adrs.pop()
    most_recent_id = most_recent_adr.stem.split("-")[0]
    next_id = f"{int(most_recent_id) + 1:04d}"
    return next_id
