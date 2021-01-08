# page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class Member(BaseApi):
    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/member.yml"
    _member_data = load_yaml(_file_path)

    def add_member(self, token, name, userid, mobile):
        api_data = self._member_data["add_member"]
        p_data = {"token": token, "name": name, "userid": userid, "mobile": mobile}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete_member(self, token, userid):
        api_data = self._member_data["delete_member"]
        p_data = {"token": token, "userid": userid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def multi_delete_member(self, token, uesrid_list):
        api_data = self._member_data["multi_delete_member"]
        p_data = {"token": token, "userid_list": uesrid_list}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit_member(self, token, name, userid, mobile):
        api_data = self._member_data["edit_member"]
        p_data = {"token": token, "name": name, "userid": userid, "mobile": mobile}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_member(self, token, userid):
        api_data = self._member_data["get_member"]
        p_data = {"token": token, "userid": userid}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_active_stat(self, token, date):
        api_data = self._member_data["get_active_stat"]
        p_data = {"token": token, "date": date}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_depart_member(self, token, department_id, fetch_child):
        api_data = self._member_data["get_depart_member"]
        p_data = {"token": token, "department_id": department_id, "fetch_child": fetch_child}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_depart_member_explicit(self, token, department_id, fetch_child):
        api_data = self._member_data["get_depart_member_explicit"]
        p_data = {"token": token, "department_id": department_id, "fetch_child": fetch_child}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get_invite_qr(self, token, size_type):
        api_data = self._member_data["get_invite_qr"]
        p_data = {"token": token, "size_type": size_type}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
