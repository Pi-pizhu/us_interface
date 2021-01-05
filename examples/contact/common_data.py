from examples.api_page.get_token import GetToken
from us_interface.config.global_config import GlobalConfig


class Base:
    """
    用类的方式获取token，这样测试类就不用受到fixture中，只有test用例才能拿到token的困扰
    """

    # 获取token
    def get_token(self):
        gl_config = GlobalConfig()
        corp_id = gl_config.get_global_variable("token", "corp_id")
        secret = gl_config.get_global_variable("token", "corp_secret")
        token = GetToken().token(corp_id, secret)
        return token["access_token"]

# 单例模式获取到的token值
contact_token = Base().get_token()

if __name__ == "__main__":
    pass