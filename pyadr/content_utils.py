import re
from datetime import datetime
from typing import Optional, TextIO, Tuple

from slugify import slugify

from pyadr.exceptions import (
    PyadrAdrDateNotFoundError,
    PyadrAdrStatusNotFoundError,
    PyadrAdrTitleNotFoundError,
    PyadrNoLineWithSuffixError,
)


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


def adr_title_slug_from_content_stream(
    stream: TextIO, stream_source: str = "Not provided"
) -> str:
    title, _, _ = retrieve_title_status_and_date_from_madr_content_stream(
        stream, stream_source
    )
    return adr_title_slug(title)


def adr_title_slug(title: str) -> str:
    return slugify(title)


def retrieve_title_status_and_date_from_madr_content_stream(
    stream: TextIO, stream_source: str = "Not provided",
) -> Tuple[str, Tuple[str, Optional[str]], str]:
    try:
        title = extract_next_line_with_suffix_from_content_stream(
            stream, "# ", stream_source=stream_source
        )
    except PyadrNoLineWithSuffixError:
        raise PyadrAdrTitleNotFoundError(source=stream_source)

    try:
        full_status = extract_next_line_with_suffix_from_content_stream(
            stream, "* Status:", stream_source=stream_source
        )
    except PyadrNoLineWithSuffixError:
        raise PyadrAdrStatusNotFoundError(source=stream_source)

    status_phrase: Optional[str]
    try:
        status, status_phrase = full_status.split(" ", 1)
    except ValueError:
        status = full_status
        status_phrase = None
    else:
        status_phrase = status_phrase.strip()

    try:
        date = extract_next_line_with_suffix_from_content_stream(
            stream, "* Date:", stream_source=stream_source
        )
    except PyadrNoLineWithSuffixError:
        raise PyadrAdrDateNotFoundError(source=stream_source)

    return title, (status, status_phrase), date


def extract_next_line_with_suffix_from_content_stream(
    stream: TextIO, suffix: str, stream_source: str = "Not provided",
) -> str:
    line = "bootstrap string"
    while not line.startswith(suffix) and len(line) != 0:
        line = stream.readline()
    if len(line) == 0:
        raise PyadrNoLineWithSuffixError(
            f"No line found with suffix '{suffix}' "
            f"in content from source '{stream_source}'"
        )
    title = line[len(suffix) :].strip()
    return title


def build_toc_content_from_adrs_by_status(adrs_by_status):
    toc_content = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be "
        "erased at next generation. -->\n",
        "# Architecture Decision Records\n",
    ]
    for status in ["accepted", "rejected", "superseded", "deprecated", "non-standard"]:
        if status != "non-standard":
            toc_content.append("\n")
            toc_content.append(f"## {adrs_by_status[status]['status-title']}\n")
            toc_content.append("\n")
            if adrs_by_status[status]["adrs"]:
                toc_content.extend(adrs_by_status[status]["adrs"])
            else:
                toc_content.append("* None\n")
        else:
            toc_content.append("\n")
            toc_content.append(f"## {adrs_by_status[status]['status-title']}\n")
            if adrs_by_status[status]["adrs-by-status"]:
                for value in adrs_by_status[status]["adrs-by-status"].values():
                    toc_content.append("\n")
                    toc_content.append(f"### {value['status-title']}\n")
                    toc_content.append("\n")
                    toc_content.extend(value["adrs"])
            else:
                toc_content.append("\n")
                toc_content.append("* None\n")
    return toc_content


def extract_adrs_by_status(records_path, adr_paths):
    adrs_by_status = {
        "accepted": {"status-title": "Accepted Records", "adrs": []},
        "rejected": {"status-title": "Rejected Records", "adrs": []},
        "superseded": {"status-title": "Superseded Records", "adrs": []},
        "deprecated": {"status-title": "Deprecated Records", "adrs": []},
        "non-standard": {
            "status-title": "Records with non-standard statuses",
            "adrs-by-status": {},
        },
    }
    for adr in adr_paths:
        with adr.open() as f:
            (
                title,
                (status, status_phrase),
                date,
            ) = retrieve_title_status_and_date_from_madr_content_stream(
                f, stream_source=str(adr)
            )
        try:
            status_supplement = ""
            if status_phrase:
                status_supplement = f": {status} {status_phrase}"
            adrs_by_status[status]["adrs"].append(
                f"* [{title}]({records_path / adr.name})" f"{status_supplement}\n"
            )
        except KeyError:
            if status not in adrs_by_status["non-standard"]["adrs-by-status"].keys():
                adrs_by_status["non-standard"]["adrs-by-status"][status] = {
                    "status-title": f"Status `{status}`",
                    "adrs": [],
                }
            adrs_by_status["non-standard"]["adrs-by-status"][status]["adrs"].append(
                f"* [{title}]({records_path / adr.name})" f"{status_supplement}\n"
            )
    return adrs_by_status
