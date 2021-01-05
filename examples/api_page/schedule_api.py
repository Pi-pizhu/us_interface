#page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.load_file import load_yaml


class ScheduleApi(BaseApi):

    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/schedule_api.yml"
    _schedule_api_data = load_yaml(_file_path)
    

    def add(self, token, organizer, start_time, end_time, userid, summary, description, location):
        api_data = self._schedule_api_data["add"]
        p_data = {"token": token, "organizer": organizer, "start_time": start_time, "end_time": end_time,
                  "userid": userid, "summary": summary, "description": description, "location": location}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get(self, token, schedule_id_list):
        api_data = self._schedule_api_data["get"]
        p_data = {"token": token, "schedule_id_list": schedule_id_list}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit(self, token, organizer, schedule_id, start_time, end_time, userid, summary, description, location):
        api_data = self._schedule_api_data["edit"]
        p_data = {"token": token, "organizer": organizer, "schedule_id": schedule_id,
                  "start_time": start_time, "end_time": end_time,
                  "userid": userid, "summary": summary, "description": description, "location": location}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete(self, token, schedule_id):
        api_data = self._schedule_api_data["delete"]
        p_data = {"token": token, "schedule_id": schedule_id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    