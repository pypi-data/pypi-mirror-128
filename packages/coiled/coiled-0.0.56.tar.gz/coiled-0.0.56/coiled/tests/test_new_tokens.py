"""
These are some tests for our new long-lived API tokens.

When the old tokens are deprecated, most/all tests will switch to these type of tokens, so this file will be
superfluous can be deleted.
"""
import coiled
import dask
from django.test import override_settings


@override_settings(LONG_LIVED_TOKENS_ENABLED=True)
def test_set_backend_options_new_token(sample_user, long_lived_token_for_sample_user):
    """Tests that config setting (which exercises the websocket code path) works with the new long-lived tokens."""
    config = dask.config.config
    with dask.config.set(
        dask.config.merge(
            config, {"coiled": {"token": long_lived_token_for_sample_user}}
        )
    ):
        coiled.set_backend_options(use_coiled_defaults=True)


@override_settings(LONG_LIVED_TOKENS_ENABLED=True)
def test_create_software_environment_new_token(
    sample_user, long_lived_token_for_sample_user
):
    config = dask.config.config
    with dask.config.set(
        dask.config.merge(
            config, {"coiled": {"token": long_lived_token_for_sample_user}}
        )
    ):
        coiled.create_software_environment(
            name=f"{sample_user.account.name}/test-env-with-new-token",
            container="daskdev/dask:latest",
        )
