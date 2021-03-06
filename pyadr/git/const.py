"""Package constants"""

GIT_ADR_DEFAULT_SETTINGS = {"adr-only-repo": "false"}

PROPOSAL_REQUEST = "propose"
DEPRECATION_REQUEST = "deprecate"
SUPERSEDING_REQUEST = "supersede"
VALID_REQUESTS = [
    PROPOSAL_REQUEST,
    DEPRECATION_REQUEST,
    SUPERSEDING_REQUEST,
]
