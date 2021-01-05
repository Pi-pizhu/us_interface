import allure
from ...api_page.calendar_api import CalendarApi
from loguru import logger


class TestCalendar():
    """
    日历的测试类
    1.没有做参数化
    """

    # 初始化日历对象
    calendar = CalendarApi()

    @allure.story("增加日历冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_calendar_smoke(self, schedule_token):
        logger.info("--------增加日历开始冒烟测试")
        res = self.calendar.add(schedule_token, "calendar", 1, 0, "test1", "0001FF", "hehedada")
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("编辑日历冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_calendar_smoke(self, schedule_token):
        logger.info("--------开始编辑日历冒烟测试")
        res = self.calendar.edit(schedule_token, 0, None, "gaigai", "1000FF", None)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("获取日历冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_calendar_smoke(self, schedule_token):
        logger.info("--------开始获取日历冒烟测试")
        res = self.calendar.get(schedule_token)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("删除日历冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_calendar_smoke(self, schedule_token):
        logger.info("--------开始删除日历冒烟测试")
        res = self.calendar.delete(schedule_token, 0)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]
