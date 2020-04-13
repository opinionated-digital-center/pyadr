from hamcrest import assert_that, equal_to

from pyadr.content_utils import build_toc_content_from_adrs_by_status


def test_build_toc_content_from_adrs_by_status():
    # Given
    adrs_by_status = {
        "accepted": {
            "status-title": "Accepted Records",
            "adrs": [
                f"* [ADR Title](docs/adr/adr.md)\n",
                f"* [ADR Title](docs/adr/adr.md)\n",
            ],
        },
        "rejected": {
            "status-title": "Rejected Records",
            "adrs": [f"* [ADR Title](docs/adr/adr.md)\n"],
        },
        "superseded": {
            "status-title": "Superseded Records",
            "adrs": [f"* [ADR Title](docs/adr/adr.md)\n"],
        },
        "deprecated": {
            "status-title": "Deprecated Records",
            "adrs": [f"* [ADR Title](docs/adr/adr.md)\n"],
        },
        "non-standard": {
            "status-title": "Records with non-standard statuses",
            "adrs-by-status": {
                "foo": {
                    "status-title": "Status `foo`",
                    "adrs": [f"* [ADR Title](docs/adr/adr.md)\n"],
                },
                "bar": {
                    "status-title": "Status `bar`",
                    "adrs": [f"* [ADR Title](docs/adr/adr.md)\n"],
                },
            },
        },
    }

    # When
    toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

    # Then
    expected = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be erased "
        "at next generation. -->\n",
        "# Architecture Decision Records\n",
        "\n",
        "## Accepted Records\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "\n",
        "## Rejected Records\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "\n",
        "## Superseded Records\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "\n",
        "## Deprecated Records\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "\n",
        "## Records with non-standard statuses\n",
        "\n",
        "### Status `foo`\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
        "\n",
        "### Status `bar`\n",
        "\n",
        "* [ADR Title](docs/adr/adr.md)\n",
    ]
    assert_that(toc_content, equal_to(expected))


def test_build_toc_content_from_adrs_by_status_no_adr():
    # Given
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

    # When
    toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

    # Then
    expected = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be erased "
        "at next generation. -->\n",
        "# Architecture Decision Records\n",
        "\n",
        "## Accepted Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Rejected Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Superseded Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Deprecated Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Records with non-standard statuses\n",
        "\n",
        "* None\n",
    ]
    assert_that(toc_content, equal_to(expected))
