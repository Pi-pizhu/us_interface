#page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.load_file import load_yaml


class DepartmentApi(BaseApi):

    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/department_api.yml"
    _department_api_data = load_yaml(_file_path)

    def get(self, token, id):
        api_data = self._department_api_data["get"]
        p_data = {"token": token, "id": id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def add(self, token, parentid, name):
        api_data = self._department_api_data["add"]
        p_data = {"token": token, "parentid": parentid, "name": name}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete(self, token, id):
        api_data = self._department_api_data["delete"]
        p_data = {"token": token, "id": id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit(self, token, id, name):
        api_data = self._department_api_data["edit"]
        p_data = {"token": token, "id": id, "name": name}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    