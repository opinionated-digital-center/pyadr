from pathlib import Path

from pyadr.content_utils import update_adr_content_title_and_status
from pyadr.exceptions import PyadrNoNumberedAdrError


def update_adr(file: Path, title: str = None, status: str = None) -> None:
    with file.open() as f:
        updated_content = update_adr_content_title_and_status(
            f.read(), title=title, status=status
        )
    with file.open("w") as f:
        f.write(updated_content)


def calculate_next_adr_id(adr_path: Path) -> str:
    numbered_adrs = sorted(adr_path.glob("[0-9][0-9][0-9][0-9]-*"))
    if not len(numbered_adrs):
        raise PyadrNoNumberedAdrError()
    most_recent_adr = numbered_adrs.pop()
    most_recent_id = most_recent_adr.stem.split("-")[0]
    next_id = f"{int(most_recent_id) + 1:04d}"
    return next_id
