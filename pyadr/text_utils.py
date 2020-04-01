import re
from datetime import datetime
from typing import TextIO

from slugify import slugify

from .const import STATUS_ACCEPTED, STATUS_REJECTED


def change_adr_text_to_status(text: str, status: str) -> str:
    today = datetime.today().strftime("%Y-%m-%d")
    result_text = text
    result_text = re.sub(
        r"^\* Status: .*$", f"* Status: {status}", result_text, 1, re.MULTILINE
    )
    result_text = re.sub(
        r"^\* Date: .*$", f"* Date: {today}", result_text, 1, re.MULTILINE
    )
    return result_text


def change_adr_text_to_accepted(text: str) -> str:
    return change_adr_text_to_status(text, STATUS_ACCEPTED)


def change_adr_text_to_rejected(text: str) -> str:
    return change_adr_text_to_status(text, STATUS_REJECTED)


def get_adr_title_slug_from_stream(stream: TextIO) -> str:
    title_line = ""
    while not title_line.startswith("# "):
        title_line = stream.readline()
    title_slug = slugify(title_line[1:])
    return title_slug
