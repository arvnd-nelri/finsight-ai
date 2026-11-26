"""Settings loaded from the environment or from files outside the repository.

Nothing personal or secret is stored in code. Each setting is read from an
environment variable first, then from a small KEY=VALUE file under
~/.config/finsight-ai/.
"""

import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "finsight-ai"
SEC_ENV_FILE = CONFIG_DIR / "sec.env"

# The placeholder written into sec.env; a real value must replace it.
SEC_USER_AGENT_PLACEHOLDER = "Your Name your.email@example.com"


class ConfigError(RuntimeError):
    """A required setting is missing or still holds its placeholder."""


def read_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE file. Blank lines and # comments are ignored."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_sec_user_agent(env_file: Path = SEC_ENV_FILE) -> str:
    """Return the User-Agent the SEC requires: a name and an email address.

    Looks in the SEC_USER_AGENT environment variable, then in `env_file`.
    """
    value = os.environ.get("SEC_USER_AGENT") or read_env_file(env_file).get(
        "SEC_USER_AGENT", ""
    )
    if not value or value == SEC_USER_AGENT_PLACEHOLDER:
        raise ConfigError(
            f"SEC_USER_AGENT is not set. Edit {env_file} and replace the "
            'placeholder with your name and email, e.g. "Jane Doe jane@example.com".'
        )
    if "@" not in value:
        raise ConfigError("SEC_USER_AGENT must include an email address.")
    return value
