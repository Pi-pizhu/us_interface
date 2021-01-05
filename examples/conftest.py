# 首个conftest文件，进行初始化配置操作

# 获取token值
import os

import pytest

from examples.api_page.get_token import GetToken
from us_interface.config.global_config import GlobalConfig

gl_config  = GlobalConfig()


@pytest.fixture(scope="session")
def token():
    corp_id = gl_config.get_global_variable("token", "corp_id")
    secret = gl_config.get_global_variable("token", "corp_secret")
    token = GetToken().token(corp_id, secret)
    return token["access_token"]