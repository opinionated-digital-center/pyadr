from pathlib import Path

from .const import ADR_REPO_ABS_PATH, ADR_REPO_REL_PATH
from .content_utils import retrieve_title_status_and_date_from_madr_content_stream


def generate_toc() -> Path:
    # Initialise variables
    adr_paths = sorted(ADR_REPO_ABS_PATH.glob("[0-9X][0-9X][0-9X][0-9X]-*"))

    adrs_by_status = _extract_adrs_by_status(adr_paths)

    toc_content = _build_toc_content_from_adrs_by_status(adrs_by_status)

    toc_path = ADR_REPO_ABS_PATH / "index.md"
    with toc_path.open("w") as f:
        f.writelines(toc_content)

    return toc_path


def _build_toc_content_from_adrs_by_status(adrs_by_status):
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


def _extract_adrs_by_status(adr_paths):
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
            ) = retrieve_title_status_and_date_from_madr_content_stream(f)
        try:
            status_supplement = ""
            if status_phrase:
                status_supplement = f": {status} {status_phrase}"
            adrs_by_status[status]["adrs"].append(
                f"* [{title}]({ADR_REPO_REL_PATH / adr.name}){status_supplement}\n"
            )
        except KeyError:
            if status not in adrs_by_status["non-standard"]["adrs-by-status"].keys():
                adrs_by_status["non-standard"]["adrs-by-status"][status] = {
                    "status-title": f"Status `{status}`",
                    "adrs": [],
                }
            adrs_by_status["non-standard"]["adrs-by-status"][status]["adrs"].append(
                f"* [{title}]({ADR_REPO_REL_PATH / adr.name}){status_supplement}\n"
            )
        # adr_list.append(f"* [{title}]({ADR_REPO_REL_PATH / adr.name})\n")
    return adrs_by_status
