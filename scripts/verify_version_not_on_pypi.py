# Uses the trick described in following link:
# https://stackoverflow.com/questions/4888027/python-and-pip-list-all-versions-of-a-package-thats-available/26664162#26664162  # noqa
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import toml

if len(sys.argv) < 2:
    print(f"ERROR: expected a version passed as argument.\n")
    sys.exit(1)

if len(sys.argv) > 2:
    print(f"ERROR: expected only one argument.\n")
    sys.exit(1)

root_dir = Path(__file__).resolve().parents[1]

with (root_dir / "pyproject.toml").open() as f:
    pyproject = toml.loads(f.read())

pip_cmd = "pip install"

try:
    url = os.environ["PYPI_REPOSITORY_URL"]
except KeyError:
    pass
else:
    if url:
        pip_cmd = " ".join([pip_cmd, "-i", url])
        print(pip_cmd)
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http":
            pip_cmd = " ".join([pip_cmd, "--trusted-host", parsed_url.hostname])

pip_cmd = " ".join([pip_cmd, f'{pyproject["tool"]["poetry"]["name"]}=='])
print(pip_cmd)

try:
    cmd_response = subprocess.run(
        pip_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
except subprocess.CalledProcessError as e:
    print(f'ERROR: The pip command did not succeed: {e.stderr.decode("utf-8")}')
    sys.exit(1)

cmd_error_string = cmd_response.stderr.decode("utf-8").strip()

if "NewConnectionError" in cmd_error_string:
    print(
        "ERROR: pip indicated that it has connection problems. "
        "Please check your network."
    )
    sys.exit(1)

from_versions_string = "(from versions: "
versions_start = cmd_error_string.find(from_versions_string) + len(from_versions_string)
versions_end = cmd_error_string.find(")", versions_start)
versions = cmd_error_string[versions_start:versions_end].split(", ")

if sys.argv[1] in versions:
    print(
        f"ERROR: The version you are trying to publish ({sys.argv[1]}) already exists "
        "in the pypi repository."
    )
    sys.exit(1)
