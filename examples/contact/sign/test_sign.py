# @Author : TongTong

import os
import allure
import pytest

from us_interface.utils.load_file import load_yaml
from ..common_data import contact_token
from ...api_page.sign_api import SignApi
from loguru import logger


class TestSign():
    """
    标签的的测试类
    1.参数化存放在特定的yml文件中，用三级目录管理用例、参数数据和ids的数据
    2.token值是从上一级目录的类中获取的，因此可以放到类中使用
    3.对token的值做参数化
    5.critical的用例等级为完整测试，blocker等级为冒烟测试
    6.每个用例都配合fixture，完成了不同的前置和后置，实现了不同用例互不干扰的状态
    """

    # 初始化标签对象
    sign = SignApi()
    # 获取根路径
    # base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    # # 获取data的路径，但这样写有点蠢，因为template没有对路径进行好的优化
    # data_path = os.path.join(base_path, "data/sign/sign_para.yml")
    sign_para_data = load_yaml("../../api_parameter/sign_para.yml")
    # 参数化的数据
    sign_data = sign.template_data(sign_para_data, {"token": contact_token})

    add_data = sign_data["add"]["data"]
    add_ids = sign_data["add"]["ids"]

    edit_data = sign_data["edit"]["data"]
    edit_ids = sign_data["edit"]["ids"]

    get_data = sign_data["get"]["data"]
    get_ids = sign_data["get"]["ids"]

    get_all_sign_data = sign_data["get_all_sign"]["data"]
    get_all_sign_ids = sign_data["get_all_sign"]["ids"]

    add_sign_to_member_data = sign_data["add_sign_to_member"]["data"]
    add_sign_to_member_ids = sign_data["add_sign_to_member"]["ids"]

    delete_data = sign_data["delete"]["data"]
    delete_member_ids = sign_data["delete"]["ids"]

    delete_sign_to_member_data = sign_data["delete_sign_to_member"]["data"]
    delete_sign_to_member_ids = sign_data["delete_sign_to_member"]["ids"]

    @pytest.mark.parametrize(("token1,tagid,tagname,errcode,errmsg"), add_data, ids=add_ids)
    @allure.story("增加标签测试")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add(self, token1, tagid, tagname, errcode, errmsg, add_sign):
        logger.info("--------开始增加标签测试")
        res = self.sign.add_sign(token1, tagname, tagid)
        logger.info("--------结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]

    @pytest.mark.parametrize(("token1,errcode,errmsg"), get_all_sign_data, ids=get_all_sign_ids)
    @allure.story("查看所有的标签")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_sign(self, token1, errcode, errmsg):
        logger.info("--------开始测试冒烟")
        res = self.sign.get_all_sign(token1)
        logger.info("--------开始结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]

    @pytest.mark.parametrize(("token1,tagid,tagname,errcode,errmsg"), edit_data, ids=edit_ids)
    @allure.story("编辑标签")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit(self, token1, tagid, tagname, errcode, errmsg, edit_sign):
        logger.info("--------开始测试冒烟")
        res = self.sign.edit_sign(token1, tagname, tagid)
        logger.info("--------开始结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]

    @pytest.mark.parametrize(("token1,tagid,errcode,errmsg"), get_data, ids=get_ids)
    @allure.story("获取标签。通过tagid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get(self, token1, tagid, errcode, errmsg, get_sign):
        logger.info("--------开始测试冒烟")
        res = self.sign.get_member_sign(token1, tagid)
        logger.info("--------开始结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]

    @pytest.mark.parametrize(("token1,tagid,userlist,errcode,errmsg"), add_sign_to_member_data,
                             ids=add_sign_to_member_ids)
    @allure.story("把标签添加到用户上")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_sign_to_member(self, token1, tagid, userlist, errcode, errmsg, add_sign_to_member):
        logger.info("--------开始测试冒烟")
        res = self.sign.add_sign_to_member(token1, tagid, userlist)
        logger.info("--------开始结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]

    # @pytest.mark.parametrize(("token1,tagid,userlist,errcode,errmsg"),delete_sign_to_member_data,ids=delete_sign_to_member_ids)
    # @allure.story("删除用户的标签")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_delete_sign_to_member(self,token1,tagid,userlist,errcode,errmsg,delete_sign_to_member):
    #     logger.info("--------开始删除用户的标签测试")
    #     res= self.sign.delete_sign_to_member(token1,tagid,userlist)
    #     logger.info("--------开始结束测试")
    #     assert errcode ==res["errcode"]
    #     assert errmsg in res["errmsg"]

    @pytest.mark.parametrize(("token1,tagid,userlist,errcode,errmsg,invalidlist"), delete_sign_to_member_data,
                             ids=delete_sign_to_member_ids)
    @allure.story("删除用户的标签")
    @allure.severity(allure.severity_level.CRITICAL)
    def test(self, token1, tagid, userlist, errcode, errmsg, delete_sign_to_member, invalidlist):
        logger.info("--------开始删除用户的标签测试")
        res = self.sign.delete_sign_to_member(token1, tagid, userlist)
        logger.info("--------开始结束测试")
        assert errcode == res["errcode"]
        assert errmsg in res["errmsg"]
        if self.sign.jsonpath(res, "$.invalidlist"):
            assert invalidlist in self.sign.jsonpath(res, "$.invalidlist")

    #
    # @pytest.mark.parametrize(("token,errcode,errmsg"),,ids=)
    # @allure.story("")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test(self,):
    #     logger.info("--------开始测试冒烟")
    #     res= self.sign
    #     logger.info("--------开始结束测试")
    #     assert errcode ==res["errcode"]
    #     assert errmsg in res["errmsg"]

    @allure.story("增加标签的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_smoke(self, smoke):
        logger.info("--------开始增加标签的冒烟测试")
        res = self.sign.add_sign(contact_token, "add1", 13)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "created" in res["errmsg"]

    @allure.story("获取所有标签信息冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_all_sign_smoke(self):
        logger.info("--------开始测试冒烟获取所有标签信息")
        res = self.sign.get_all_sign(contact_token)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("编辑标签名字冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_smoke(self, smoke):
        logger.info("--------开始测试冒烟编辑标签名字")
        res = self.sign.edit_sign(contact_token, "add20", 10)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "updated" in res["errmsg"]

    @allure.story("删除标签冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_smoke(self):
        logger.info("--------开始测试冒烟删除标签")
        res = self.sign.delete_sign(contact_token, 11)
        logger.info("--------结束测试")
        assert 0 == res["errcode"]
        assert "deleted" in res["errmsg"]

    @allure.story("标签加入到用户上的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_sign_to_member_smoke(self, smoke):
        logger.info("--------开始标签加入到用户上的冒烟测试")
        res = self.sign.add_sign_to_member(contact_token, 10, ["sign"])
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]

    @allure.story("删除用户名的标签的冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_sign_to_smoke(self, smoke):
        logger.info("--------开始测试删除用户名的标签冒烟测试")
        res = self.sign.delete_sign_to_member(contact_token, 10, ["sign"])
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "deleted" in res["errmsg"]

    @allure.story("获取标签信息冒烟测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_smoke(self, smoke):
        logger.info("--------开始测试冒烟")
        res = self.sign.get_member_sign(contact_token, 10)
        logger.info("--------开始结束测试")
        assert 0 == res["errcode"]
        assert "ok" in res["errmsg"]
