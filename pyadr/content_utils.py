import re
from datetime import datetime
from typing import Optional, TextIO, Tuple

from slugify import slugify

from pyadr.exceptions import PyadrNoLineWithSuffixError


def update_adr_content_title_status(
    content: str, title: str = None, status: str = None
) -> str:
    if not title and not status:
        raise TypeError("argument 'title' of 'status' has to be given")

    today = datetime.today().strftime("%Y-%m-%d")
    updated_content = content
    if title:
        updated_content = re.sub(
            r"^# .*$", f"# {title}", updated_content, 1, re.MULTILINE
        )
    if status:
        updated_content = re.sub(
            r"^\* Status: .*$", f"* Status: {status}", updated_content, 1, re.MULTILINE
        )
    updated_content = re.sub(
        r"^\* Date: .*$", f"* Date: {today}", updated_content, 1, re.MULTILINE
    )
    return updated_content


def build_adr_title_slug_from_content_stream(stream: TextIO) -> str:
    title, _, _ = retrieve_title_status_and_date_from_madr_content_stream(stream)
    title_slug = slugify(title)
    return title_slug


def retrieve_title_status_and_date_from_madr_content_stream(
    stream: TextIO,
) -> Tuple[str, Tuple[str, Optional[str]], str]:
    title = extract_next_line_with_suffix_from_content_stream(stream, "# ")

    full_status = extract_next_line_with_suffix_from_content_stream(stream, "* Status:")

    status_phrase: Optional[str]
    try:
        status, status_phrase = full_status.split(" ", 1)
    except ValueError:
        status = full_status
        status_phrase = None
    else:
        status_phrase = status_phrase.strip()

    date = extract_next_line_with_suffix_from_content_stream(stream, "* Date:")

    return title, (status, status_phrase), date


def extract_next_line_with_suffix_from_content_stream(
    stream: TextIO, suffix: str
) -> str:
    line = "bootstrap string"
    while not line.startswith(suffix) and len(line) != 0:
        line = stream.readline()
    if len(line) == 0:
        raise PyadrNoLineWithSuffixError(f"No line found with suffix '{suffix}'")
    title = line[len(suffix) :].strip()
    return title
