# page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class SignApi(BaseApi):
    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/sign_api.yml"
    _sign_api_data = load_yaml(_file_path)

    def add_sign(self, token, tagname, tagid):
        api_data = self._sign_api_data["add_sign"]
        p_data = {"token": token, "tagname": tagname, "tagid": tagid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit_sign(self, token, tagname, tagid):
        api_data = self._sign_api_data["edit_sign"]
        p_data = {"token": token, "tagname": tagname, "tagid": tagid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete_sign(self, token, tagid):
        api_data = self._sign_api_data["delete_sign"]
        p_data = {"token": token, "tagid": tagid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_member_sign(self, token, tagid):
        api_data = self._sign_api_data["get_member_sign"]
        p_data = {"token": token, "tagid": tagid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def add_sign_to_member(self, token, tagid, userlist):
        api_data = self._sign_api_data["add_sign_to_member"]
        p_data = {"token": token, "tagid": tagid, "userlist": userlist}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete_sign_to_member(self, token, tagid, userlist):
        api_data = self._sign_api_data["delete_sign_to_member"]
        p_data = {"token": token, "tagid": tagid, "userlist": userlist}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_all_sign(self, token):
        api_data = self._sign_api_data["get_all_sign"]
        p_data = {"token": token}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
