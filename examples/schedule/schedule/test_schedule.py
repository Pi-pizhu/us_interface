import allure
from ...api_page.schedule_api import ScheduleApi
from loguru import logger


class TestSchedule():
    """
    日程的测试类
    1.没有做参数化
    """

    # 初始化日程对象
    schedule = ScheduleApi()

    @allure.story("增加日程冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_calendar_smoke(self, schedule_token):
        logger.info("--------开始增加日程冒烟测试")
        res = self.schedule.add(schedule_token, "schedule", "2020-10-01 00:00:00", "2020-10-02 00:00:00",
                                "calendar", "abc", None, None)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("编辑日程冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_calendar_smoke(self, schedule_token):
        logger.info("--------开始编辑日程冒烟测试")
        res = self.schedule.edit(schedule_token, "schedule", 1, "2020-10-01 00:00:00", "2020-10-02 00:00:00",
                                 "calendar", "abc", None, None)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("获取日程冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_calendar_smoke(self, schedule_token):
        logger.info("--------开始获取日程冒烟测试")
        res = self.schedule.get(schedule_token)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("删除日程冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_calendar_smoke(self, schedule_token):
        logger.info("--------开始删除日程冒烟测试")
        res = self.schedule.delete(schedule_token, 0)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]
