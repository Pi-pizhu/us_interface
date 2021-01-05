#page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.load_file import load_yaml


class MeetingRoomApi(BaseApi):

    _file_path = "/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples/api/meeting_room_api.yml"
    _meeting_room_api_data = load_yaml(_file_path)
    

    def add(self, token, name, capacity, city, building, floor, equipment):
        api_data = self._meeting_room_api_data["add"]
        p_data = {"token": token, "name": name, "capacity": capacity, "city": city, "building": building,
                  "floor": floor, "equipment": equipment}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def get(self, token, city, building, floor, equipment):
        api_data = self._meeting_room_api_data["get"]
        p_data = {"token": token, "city": city, "building": building, "floor": floor,
                  "equipment": equipment}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def edit(self, token, meetingroom_id, name, capacity, city, building, floor, equipment):
        api_data = self._meeting_room_api_data["edit"]
        p_data = {"token": token, "meetingroom_id": meetingroom_id, "name": name, "capacity": capacity,
                  "city": city, "building": building, "floor": floor, "equipment": equipment}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    def delete(self, token, meetingroom_id):
        api_data = self._meeting_room_api_data["delete"]
        p_data = {"token": token, "meetingroom_id": meetingroom_id}
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)

    