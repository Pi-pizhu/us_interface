import pytest
from us_interface.config.global_config import GlobalConfig
from ..api_page.get_token import GetToken
from ..api_page.meeting_room_api import MeetingRoomApi

# 初始化会议室对象
meeting = MeetingRoomApi()


# 获取token值
@pytest.fixture(scope="session")
def meeting_token():
    gl_config = GlobalConfig()
    corp_id = gl_config.get_global_variable("token", "corp_id")
    secret = gl_config.get_global_variable("token", "meeting_room_secret")
    token = GetToken().token(corp_id, secret)
    return token["access_token"]


# 会议室冒烟测试前后置步骤
@pytest.fixture(scope="session")
def meeting_smoke(token):
    # add的前置步骤
    meeting.delete(token, 1)
    # edit的前置步骤
    meeting.add(token, "tong", 11, None, None, None, None)
    # 删除的前置步骤
    meeting.add(token, "tong1", 12, None, None, None, None)
    yield
    # 后置步骤
    meeting.delete(token, 1)
    meeting.delete(token, 2)
    meeting.delete(token, 3)
    meeting.delete(token, 4)
    meeting.delete(token, 5)
    meeting.delete(token, 6)
    meeting.delete(token, 7)
