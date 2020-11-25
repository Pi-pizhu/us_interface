import json

import requests
from string import Template
from base.loader import load_files
from base.variables import template
from jsonpath import jsonpath
from loguru import logger


class BaseApi:

    extract_test_case_format = "$..[?(@.name=='case_name')]."

    def http_request(self, **kwargs):
        try:
            logger.info("---------请求内容---------\n")
            logger.info(json.dumps(kwargs) + "\n")
            resp_data = requests.Session().request(**kwargs)
            logger.info("---------响应结果---------")
            logger.info(resp_data.text + "\n")
            return resp_data.json()
        except Exception as error:
            print(error)

    def get_case(self, case_file, load_type="yml", sub=None):
        test_case = load_files(case_file, load_type=load_type)
        return test_case if not sub else test_case[sub]

    def run(self, test_case_data, **data):
        # 解析用例 替换变量
        if data:
            test_case_data = template(test_case_data, data=data)
        # todo：是否进行编码，先放弃

        # 进行请求
        resp_json = self.http_request(**test_case_data)
        return resp_json

    @classmethod
    def extract_variables(self, data, expr):
        return jsonpath(data, expr)