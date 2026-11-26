"""Tests for finsight.config: loading the SEC User-Agent safely."""

import pytest

from finsight.config import (
    SEC_USER_AGENT_PLACEHOLDER,
    ConfigError,
    get_sec_user_agent,
    read_env_file,
)


@pytest.fixture(autouse=True)
def no_env_var(monkeypatch):
    # Make tests independent of the developer's real environment.
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)


def test_read_env_file_parses_values_and_skips_comments(tmp_path):
    env = tmp_path / "sec.env"
    env.write_text('# comment\n\nSEC_USER_AGENT="Jane Doe jane@example.com"\n')
    assert read_env_file(env) == {"SEC_USER_AGENT": "Jane Doe jane@example.com"}


def test_read_env_file_missing_file_returns_empty(tmp_path):
    assert read_env_file(tmp_path / "missing.env") == {}


def test_user_agent_from_file(tmp_path):
    env = tmp_path / "sec.env"
    env.write_text('SEC_USER_AGENT="Jane Doe jane@example.com"\n')
    assert get_sec_user_agent(env) == "Jane Doe jane@example.com"


def test_env_var_takes_priority_over_file(tmp_path, monkeypatch):
    env = tmp_path / "sec.env"
    env.write_text('SEC_USER_AGENT="From File file@example.com"\n')
    monkeypatch.setenv("SEC_USER_AGENT", "From Env env@example.com")
    assert get_sec_user_agent(env) == "From Env env@example.com"


def test_placeholder_is_rejected(tmp_path):
    env = tmp_path / "sec.env"
    env.write_text(f'SEC_USER_AGENT="{SEC_USER_AGENT_PLACEHOLDER}"\n')
    with pytest.raises(ConfigError, match="not set"):
        get_sec_user_agent(env)


def test_missing_setting_is_rejected(tmp_path):
    with pytest.raises(ConfigError, match="not set"):
        get_sec_user_agent(tmp_path / "missing.env")


def test_value_without_email_is_rejected(tmp_path):
    env = tmp_path / "sec.env"
    env.write_text('SEC_USER_AGENT="Jane Doe"\n')
    with pytest.raises(ConfigError, match="email"):
        get_sec_user_agent(env)
