import os
import sys

PYPI_REPOSITORY_NAME_ENV_VAR = "PYPI_REPOSITORY_NAME"
PYPI_REPOSITORY_URL_ENV_VAR_TEMPLATE = "POETRY_REPOSITORIES_{}_URL"
PYPI_REPOSITORY_USERNAME_ENV_VAR_TEMPLATE = "POETRY_HTTP_BASIC_{}_USERNAME"
PYPI_REPOSITORY_PASSWORD_ENV_VAR_TEMPLATE = "POETRY_HTTP_BASIC_{}_PASSWORD"
PYPI_REPOSITORY_API_TOKEN_ENV_VAR_TEMPLATE = "POETRY_PYPI_TOKEN_{}"

pypi_name = "pypi"
pypi_url = pypi_username = pypi_password = pypi_api_token = None

exit_code = 0

try:
    pypi_name = os.environ[PYPI_REPOSITORY_NAME_ENV_VAR]
except KeyError:
    pass

print(f"Target pypi repository: '{pypi_name}'")


def to_env_var_name(name):
    return name.replace(".", "_").replace("-", "_").upper()


pypi_repository_url_env_var = PYPI_REPOSITORY_URL_ENV_VAR_TEMPLATE.format(
    to_env_var_name(pypi_name)
)
pypi_repository_username_env_var = PYPI_REPOSITORY_USERNAME_ENV_VAR_TEMPLATE.format(
    to_env_var_name(pypi_name)
)
pypi_repository_password_env_var = PYPI_REPOSITORY_PASSWORD_ENV_VAR_TEMPLATE.format(
    to_env_var_name(pypi_name)
)
pypi_repository_api_token_env_var = PYPI_REPOSITORY_API_TOKEN_ENV_VAR_TEMPLATE.format(
    to_env_var_name(pypi_name)
)

# This line is only to avoid confusion in the code formatting error message by having
# all variables in lower case
pypi_repository_name_env_var = PYPI_REPOSITORY_NAME_ENV_VAR

try:
    pypi_url = os.environ[pypi_repository_url_env_var]
except KeyError:
    pass
try:
    pypi_username = os.environ[pypi_repository_username_env_var]
except KeyError:
    pass
try:
    pypi_password = os.environ[pypi_repository_password_env_var]
except KeyError:
    pass
try:
    pypi_api_token = os.environ[pypi_repository_api_token_env_var]
except KeyError:
    pass

print(pypi_url)
print(pypi_username)
print(pypi_password)
print(pypi_api_token)

if pypi_name == "pypi":
    if pypi_url:
        print(
            f"ERROR: ({pypi_repository_name_env_var} = '{pypi_name}', "
            f"{pypi_repository_url_env_var} = '{pypi_url}') "
            f"When the environment variable {PYPI_REPOSITORY_NAME_ENV_VAR} is 'pypi', "
            f"empty or not defined, you must NOT define the environment variable "
            f"{pypi_repository_url_env_var}."
        )
        exit_code = 1
else:
    if not pypi_url:
        print(
            f"ERROR: ({pypi_repository_name_env_var} = '{pypi_name}', "
            f"{pypi_repository_url_env_var} = '{pypi_url}') "
            f"When the environment variable {PYPI_REPOSITORY_NAME_ENV_VAR} "
            f"is NOT 'pypi', you must define the environment variable "
            f"{pypi_repository_url_env_var}."
        )
        exit_code = 1
if pypi_username is None and pypi_api_token is None:
    print(
        f"ERROR: Either {pypi_repository_username_env_var} or "
        f"{pypi_repository_api_token_env_var} environment variables "
        f"must be set."
    )
    exit_code = 1
if pypi_username and pypi_password is None:
    print(
        f"ERROR: No {pypi_repository_api_token_env_var} environment variable set "
        f"for {pypi_repository_username_env_var} = '{pypi_username}'."
    )
    exit_code = 1

if exit_code == 0:
    print("Pypi repository environment variables correctly configured for CI/CD.")

sys.exit(exit_code)
