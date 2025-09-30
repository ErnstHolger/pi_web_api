import pytest


@pytest.mark.integration
def test_sandbox_placeholder(pi_web_api_client):
    l = pi_web_api_client.asset_server.list()

    asset_servers = l[0]
    assert True
