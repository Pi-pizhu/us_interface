import json

from base.base_api import BaseApi


class Department(BaseApi):

    corpsecret = "OPwr_zzGZJJqtSDu3VtvkYdcL3_sK2SDrc-VIVUvP58"
    corpid = "wwa7cdc2cfba303c84"

    def __init__(self):
        case_data = self.get_case("./../examples/yml/token.yml")
        self.token = self.run(
            case_data, corpsecret=self.corpsecret, corpid=self.corpid
        )
        self.token = self.token['access_token']
        self.case_data = self.get_case("./../examples/yml/tag.all.yaml")

    def create(self, **data):
        data.update({"token": self.token})
        # 通过jsonpath获取对应name的请求信息
        request_msg = self.extract_variables(self.case_data,
                                             self.extract_test_case_format.replace("case_name", "create"))
        return self.run(request_msg["request"], **data)

    def delete(self, **data):
        data.update({"token": self.token})
        request_msg = self.extract_variables(self.case_data,
                                             self.extract_test_case_format.replace("case_name", "create"))
        return self.run(request_msg["request"], **data)

    def update(self, **data):
        data.update({"token": self.token})
        request_msg = self.extract_variables(self.case_data,
                                             self.extract_test_case_format.replace("case_name", "create"))
        return self.run(request_msg["request"], **data)

    def get_department(self, **data):
        data.update({"token": self.token})
        request_msg = self.extract_variables(self.case_data,
                                             self.extract_test_case_format.replace("case_name", "create"))
        return self.run(request_msg["request"], **data)


if __name__ == '__main__':
    dep = Department()
    dep.create()