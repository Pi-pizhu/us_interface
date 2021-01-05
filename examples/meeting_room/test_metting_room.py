import allure
from ..api_page.meeting_room_api import MeetingRoomApi
from loguru import logger


class TestMeetingRoom():
    """
    会议室的测试类
    1.没有做参数化
    """

    # 初始化会议室对象
    meeting = MeetingRoomApi()

    @allure.story("增加会议室的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_metting_room_smoke(self, meeting_smoke, meeting_token):
        logger.info(f"meeting_token:{meeting_token}")
        logger.info("--------开始增加会议室的冒烟测试")
        res = self.meeting.add(meeting_token, "smoke1", 30, None, None, None, None)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("编辑会议室的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_metting_room_smoke(self, meeting_smoke, meeting_token):
        logger.info("--------开始编辑会议室的冒烟测试")
        res = self.meeting.edit(meeting_token, 2, "edit", None, None, None, None, None)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "updated" in res["errmsg"]

    @allure.story("删除会议室的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_metting_room_smoke(self, meeting_smoke, meeting_token):
        logger.info("--------开始删除会议室的冒烟测试")
        res = self.meeting.delete(meeting_token, 1)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "deleted" in res["errmsg"]

    @allure.story("获取会议室的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_metting_room_smoke(self, meeting_smoke, meeting_token):
        logger.info("--------开始获取会议室的冒烟测试")
        res = self.meeting.get(meeting_token, None, None, None, None)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]
