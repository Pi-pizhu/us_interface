# page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class TagAll(BaseApi):
    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/tag_all.yml"
    _tag_all_data = load_yaml(_file_path)

    def add(self, token, name):
        api_data = self._tag_all_data["add"]
        p_data = {"token": token, "name": name}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete(self, token, tag_id):
        api_data = self._tag_all_data["delete"]
        p_data = {"token": token, "tag_id": tag_id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
