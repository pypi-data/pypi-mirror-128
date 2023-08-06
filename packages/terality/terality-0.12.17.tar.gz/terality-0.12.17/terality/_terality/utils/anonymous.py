"""Implements support for anonymous users: temporary, short-lived accounts that can be used to quickly evaluate Terality.

For any regular usage, creating a full-fledged Terality account is required.
"""

import datetime as dt

from common_client_scheduler.requests_responses import CreateAnonymousUserResponse

from terality._terality.client import anonymous_client
from terality._terality.globals import load_global_client
from terality._terality.utils.account import (
    has_valid_terality_config_file,
    has_valid_terality_credentials_file,
)
from terality._terality.utils.config import TeralityConfig, TeralityCredentials


def create_anonymous_user():
    if has_valid_terality_config_file() or has_valid_terality_credentials_file():
        # Note that we don't detect if the previous configuration is for a quickstart account or not.
        # This means that a user that used the quickstart method on this laptop then created a real account
        # with `terality account create` will be greeted with a "configuration files already exist" warning.
        print("Terality is already configured on this machine, nothing to do.")
        return

    client = anonymous_client()
    res = client.poll_for_answer("anonymous_users", payload={})
    if not isinstance(res, CreateAnonymousUserResponse):
        raise ValueError(
            f"Unexpected server answer: expected type 'CreateAnonymousUserResponse', got '{type(res)}'"
        )
    user_id = res.user_id
    api_key = res.api_key
    expires_at = res.expires_at
    _write_terality_configuration(user_id, api_key)

    print(
        f"Terality is now initialized on this machine. This is a temporary demonstration account that will only remain valid for {_format_account_duration_in_minutes(expires_at)} minutes. To create a full account, please go to https://app.terality.com (it's free!)."
    )


def _write_terality_configuration(email: str, api_key: str):
    credentials = TeralityCredentials(user_id=email, user_password=api_key)
    credentials.save()
    config = TeralityConfig()
    config.save()

    load_global_client()


def _format_account_duration_in_minutes(expires_at: dt.datetime) -> str:
    return str(round(max((expires_at - dt.datetime.utcnow()).total_seconds() // 60, 0)))
