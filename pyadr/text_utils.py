import re
from datetime import datetime
from typing import Optional, TextIO, Tuple

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
    title, _, _ = find_title_status_and_date_in_madr_content(stream)
    title_slug = slugify(title)
    return title_slug


def find_title_status_and_date_in_madr_content(
    stream: TextIO,
) -> Tuple[str, Tuple[str, Optional[str]], str]:
    """
    Extracts the title, the status (and phrase following status if exists) and date
    out of and MADR content. The content is expected to be well formed.

    Args:
        stream: TextIO

    Returns:
        Tuple[str, Tuple[str, Optional[str]]]: (title, (status, status phrase),
        date)
    """
    title = extract_next_line_content_starting_with_suffix(stream, "# ")

    full_status = extract_next_line_content_starting_with_suffix(stream, "* Status:")
    try:
        status_phrase: Optional[str]
        status, status_phrase = full_status.split(" ", 1)
    except ValueError:
        status = full_status
        status_phrase = None
    else:
        status_phrase = status_phrase.strip()

    date = extract_next_line_content_starting_with_suffix(stream, "* Date:")

    return title, (status, status_phrase), date


def extract_next_line_content_starting_with_suffix(stream: TextIO, suffix: str) -> str:
    """
    Looks for the next line starting with suffix in a text stream and returns the line
    content without the suffix

    Args:
        stream (TextIO): content stream to extract from
        suffix (str): suffix to look for

    Returns:
        str: line content without the suffix

    """
    line = ""
    while not line.startswith(suffix):
        line = stream.readline()
    title = line[len(suffix) :].strip()
    return title
