import os
import sys

ENV_VAR_PYPI_REPOSITORY_NAME = "PYPI_REPOSITORY_NAME"
ENV_VAR_PYPI_REPOSITORY_URL_TEMPLATE = "POETRY_REPOSITORIES_{}_URL"
ENV_VAR_PYPI_REPOSITORY_USERNAME_TEMPLATE = "POETRY_HTTP_BASIC_{}_USERNAME"
ENV_VAR_PYPI_REPOSITORY_PASSWORD_TEMPLATE = "POETRY_HTTP_BASIC_{}_PASSWORD"
ENV_VAR_PYPI_REPOSITORY_API_TOKEN_TEMPLATE = "POETRY_PYPI_TOKEN_{}"

pypi_name = "pypi"
pypi_url = pypi_usename = pypi_password = pypi_api_token = None

exit_code = 0

try:
    pypi_name = os.environ[ENV_VAR_PYPI_REPOSITORY_NAME]
except KeyError:
    pass

print(f"Target pypi repository: '{pypi_name}'")


def format_pypi_name(name):
    return name.replace(".", "_").replace("-", "_").upper()


env_var_pypi_repository_url = ENV_VAR_PYPI_REPOSITORY_URL_TEMPLATE.format(
    format_pypi_name(pypi_name)
)
env_var_pypi_repository_username = ENV_VAR_PYPI_REPOSITORY_USERNAME_TEMPLATE.format(
    format_pypi_name(pypi_name)
)
env_var_pypi_repository_password = ENV_VAR_PYPI_REPOSITORY_PASSWORD_TEMPLATE.format(
    format_pypi_name(pypi_name)
)
env_var_pypi_repository_api_token = ENV_VAR_PYPI_REPOSITORY_API_TOKEN_TEMPLATE.format(
    format_pypi_name(pypi_name)
)
try:
    pypi_url = os.environ[env_var_pypi_repository_url]
except KeyError:
    pass
try:
    pypi_usename = os.environ[env_var_pypi_repository_username]
except KeyError:
    pass
try:
    pypi_password = os.environ[env_var_pypi_repository_password]
except KeyError:
    pass
try:
    pypi_api_token = os.environ[env_var_pypi_repository_api_token]
except KeyError:
    pass

print(pypi_url)
print(pypi_usename)
print(pypi_password)
print(pypi_api_token)

if pypi_name == "pypi":
    if pypi_url:
        print(
            f"ERROR: ({ENV_VAR_PYPI_REPOSITORY_NAME} = '{pypi_name}', "
            f"{env_var_pypi_repository_url} = '{pypi_url}') "
            f"When the environment variable {ENV_VAR_PYPI_REPOSITORY_NAME} is 'pypi', "
            f"empty or not defined, you must NOT define the environment variable "
            f"{env_var_pypi_repository_url}."
        )
        exit_code = 1
else:
    if not pypi_url:
        print(
            f"ERROR: ({ENV_VAR_PYPI_REPOSITORY_NAME} = '{pypi_name}', "
            f"{env_var_pypi_repository_url} = '{pypi_url}') "
            f"When the environment variable {ENV_VAR_PYPI_REPOSITORY_NAME} "
            f"is NOT 'pypi', you must define the environment variable "
            f"{env_var_pypi_repository_url}."
        )
        exit_code = 1
if pypi_usename is None and pypi_api_token is None:
    print(
        f"ERROR: Either {env_var_pypi_repository_username} or "
        f"{env_var_pypi_repository_api_token} environment variables "
        f"must be set."
    )
    exit_code = 1
if pypi_usename and pypi_password is None:
    print(
        f"ERROR: No {env_var_pypi_repository_api_token} environment variable set "
        f"for {env_var_pypi_repository_username} = '{pypi_usename}'."
    )
    exit_code = 1

if exit_code == 0:
    print("Pypi repository environment variables correctly configured for CI/CD.")

sys.exit(exit_code)
