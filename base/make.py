import json
import os
import sys
from json import JSONDecodeError
from urllib.parse import unquote
from loguru import logger
from urllib import parse

from base.loader import load_har_file, dump_yml


class HarParser:

    def __init__(self, har_file_path):
        self.har_file_path = har_file_path

    def _prepare_teststep(self, entry_json):
        """ extract info from entry dict and make teststep

        Args:
            entry_json (dict):
                {
                    "request": {
                        "method": "POST",
                        "url": "https://httprunner.top/api/v1/Account/Login",
                        "headers": [],
                        "queryString": [],
                        "postData": {},
                    },
                    "response": {
                        "status": 200,
                        "headers": [],
                        "content": {}
                    }
                }

        """
        teststep_dict = {"name": "", "request": {
            "method": "",
            "url": ""
        }}

        self.__make_request_url(teststep_dict, entry_json)
        self.__make_request_method(teststep_dict, entry_json)
        self.__make_request_cookies(teststep_dict, entry_json)
        self.__make_request_headers(teststep_dict, entry_json)
        self._make_request_data(teststep_dict, entry_json)
        return teststep_dict

    def __make_request_url(self, teststep_dict, entry_json):
        request_params = self._convert_list_to_dict(
            entry_json["request"].get("queryString", [])
        )

        url = entry_json["request"].get("url")
        if not url:
            logger.exception("url missed in request.")
            sys.exit(1)

        parsed_object = parse.urlparse(url)
        if request_params:
            parsed_object = parsed_object._replace(query="")
            teststep_dict["request"]["url"] = parsed_object.geturl()
            teststep_dict["request"]["params"] = request_params
        else:
            teststep_dict["request"]["url"] = url

        teststep_dict["name"] = parsed_object.path

    def __make_request_method(self, teststep_dict, entry_json):
        method = entry_json["request"].get("method")
        if not method:
            logger.exception("method missed in request.")
            sys.exit(1)

        teststep_dict["request"]["method"] = method

    def __make_request_cookies(self, teststep_dict, entry_json):
        cookies = {}
        for cookie in entry_json["request"].get("cookies", []):
            cookies[cookie["name"]] = cookie["value"]

        if cookies:
            teststep_dict["request"]["cookies"] = cookies

    def __make_request_headers(self, teststep_dict, entry_json):
        teststep_headers = {}
        for header in entry_json["request"].get("headers", []):
            if header["name"] == "cookie" or header["name"].startswith(":"):
                continue

            teststep_headers[header["name"]] = header["value"]

        if teststep_headers:
            teststep_dict["request"]["headers"] = teststep_headers

    def _make_request_data(self, teststep_dict, entry_json):
        method = entry_json["request"].get("method")
        if method in ["POST", "PUT", "PATCH"]:
            postData = entry_json["request"].get("postData", {})
            mimeType = postData.get("mimeType")

            # Note that text and params fields are mutually exclusive.
            if "text" in postData:
                post_data = postData.get("text")
            else:
                params = postData.get("params", [])
                post_data = self._convert_list_to_dict(params)

            request_data_key = "data"
            if not mimeType:
                pass
            elif mimeType.startswith("application/json"):
                try:
                    post_data = json.loads(post_data)
                    request_data_key = "json"
                except JSONDecodeError:
                    pass
            elif mimeType.startswith("application/x-www-form-urlencoded"):
                post_data = self._convert_x_www_form_urlencoded_to_dict(post_data)
            else:
                # TODO: make compatible with more mimeType
                pass

            teststep_dict["request"][request_data_key] = post_data

    def _convert_x_www_form_urlencoded_to_dict(self, post_data):
        """ convert x_www_form_urlencoded data to dict

        Args:
            post_data (str): a=1&b=2

        Returns:
            dict: {"a":1, "b":2}

        """
        if isinstance(post_data, str):
            converted_dict = {}
            for k_v in post_data.split("&"):
                try:
                    key, value = k_v.split("=")
                except ValueError:
                    raise Exception(
                        "Invalid x_www_form_urlencoded data format: {}".format(post_data)
                    )
                converted_dict[key] = unquote(value)
            return converted_dict
        else:
            return post_data

    def _convert_list_to_dict(self, convert_list):
        return {item["name"]: item.get("value") for item in convert_list}

    def _make_testcase(self):
        """
        testcase_dict = {
                name: "",
                "request": {
                    "method": "",
                    "url": "",
                    "params": {},
                    "json": {},
                    "data": {}
                }
        }
        testcase = [testcase_dict, testcase_dict]
        :return:
        """
        logs_entrys = load_har_file(self.har_file_path)
        testcase = []
        for entry_json in logs_entrys:
            teststeps_dict = self._prepare_teststep(entry_json)
            testcase.append(teststeps_dict)
        return testcase

    def gen_testcase(self, file_type="yml"):
        harfile = os.path.splitext(self.har_file_path)[0]

        try:
            test_case = self._make_testcase()
        except Exception as error:
            logger.error(f"生成测试用例yml文件失败：{error} \n")

        if file_type == "yml" or file_type == "yaml":
            output_testcase_file = f"{harfile}1.yml"
            dump_yml(test_case, output_testcase_file)


if __name__ == '__main__':
    harparser = HarParser("/Users/yewenkai/Documents/hogwarts_std/qiyeweixin_dep.har")
    harparser.gen_testcase()