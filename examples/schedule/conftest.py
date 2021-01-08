import pytest
from examples.api_page.get_token import GetToken
from us_interface.config.global_config import GlobalConfig

gl_config = GlobalConfig()


# 获取token值
@pytest.fixture(scope="session")
def schedule_token():
    corp_id = gl_config.config_var("corp_id")
    secret = gl_config.config_var("schedule_secret")
    token = GetToken().token(corp_id, secret)
    return token["access_token"]
