# page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class CalendarApi(BaseApi):
    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/calendar_api.yml"
    _calendar_api_data = load_yaml(_file_path)

    def add(self, token, organizer, readonly, set_as_default, summary, color, description):
        api_data = self._calendar_api_data["add"]
        p_data = {"token": token, "organizer": organizer, "readonly": readonly,
                  "set_as_default": set_as_default, "summary": summary, "color": color, "description": description}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get(self, token, cal_id_list):
        api_data = self._calendar_api_data["get"]
        p_data = {"token": token, "cal_id_list": cal_id_list}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit(self, token, cal_id, readonly, summary, color, description):
        api_data = self._calendar_api_data["edit"]
        p_data = {"token": token, "cal_id": cal_id, "readonly": readonly, "summary": summary,
                  "color": color, "description": description}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete(self, token, cal_id):
        api_data = self._calendar_api_data["delete"]
        p_data = {"token": token, "cal_id": cal_id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
