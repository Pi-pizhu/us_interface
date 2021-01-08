# page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class GetToken(BaseApi):
    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/get_token.yml"
    _get_token_data = load_yaml(_file_path)

    def token(self, corp_id, secret):
        api_data = self._get_token_data["token"]
        p_data = {"corp_id": corp_id, "secret": secret}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
