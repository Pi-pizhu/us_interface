import json, os, re, sys, requests
from urllib import parse
from string import Template
from us_interface.config.global_config import GlobalConfig
from loguru import logger
from jsonpath import jsonpath
from us_interface.utils.file_operations import path_extract, locate_file

_url_compile = re.compile(r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$")
_hosts_compile = re.compile(
    r"^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)")


class BaseApi:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._test_root_path = self._get_test_root_path()
        self._get_global_config(self._test_root_path)
        self._get_url_config()

    def _get_test_root_path(self):
        # 获取用例的根目录
        work_path = os.getcwd()
        test_paht = sys.argv[1]
        original_path = os.path.join(work_path, test_paht)
        # 用例的绝对路径
        work_path = path_extract(original_path)
        # test用例根目录
        test_root_dir = locate_file(work_path, "env_config.ini")
        return test_root_dir

    def _get_global_config(self, test_root_dir):
        # 获取全局配置信息config
        self._gl_config = GlobalConfig(test_root_dir)
        self._gl_config_data = self._gl_config.config_var

    def _get_url_config(self):
        self._url_config = {}
        self._url_config["request_way"] = self._gl_config.get_global_variable("hosts", "request_way")
        self._url_config["domain_name"] = self._gl_config.get_global_variable("hosts", "domain_name")
        self._url_config["url"] = self._gl_config.get_global_variable(
            "hosts",
            self._gl_config.get_global_variable("hosts", "default")
        )

    def request_main(self, test_api, test_params=None, req_type="tcp", test_describe=None):
        """
        对api接口信息进行变量替换
        对url进行检查替换
        分别进入各种协议请求方法
        :param args:
        :param kwargs:
        :return:
        """
        # 先合并局部+全局配置
        params = self._gl_config_data
        if test_params:
            params.update(test_params)

        # 进行test_api替换
        test_api = self.template_data(test_api, params)
        # 检查url
        test_step = json.loads(test_api)
        test_step = self.replace_hosts(test_step.get("url"))
        # 发送请求
        if req_type == "tcp":
            response = self.request_http(test_step)
        elif req_type == "udp":
            pass

        # todo:是否需要提取数据 -> 要不要放在这里呢
        return response

    def request_http(self, req_data):
        req_data = json.loads(req_data)
        req_data["url"] = self.replace_hosts(req_data.get("url"))
        log_msg = f"{req_data}\n"
        try:
            resp_data = requests.Session().request(**req_data)
            log_msg += f"response msg: \n" \
                       f"response status code: {resp_data.status_code}\n" \
                       f"response text: {resp_data.text}\n"
            logger.info(log_msg)
            return resp_data.json()
        except Exception as error:
            err_msg = f"request faile: {error}\n"
            logger.error(err_msg)
            raise error

    def template_data(self, data, temp_kwargs: dict):
        if not isinstance(data, str):
            try:
                data = json.dumps(data)
            except Exception as error:
                raise error
        try:
            data = Template(data).substitute(temp_kwargs)
            return data
        except Exception as error:
            err_msg = f"替换失败: {error}\n"
            logger.error(err_msg)

    def replace_hosts(self, hosts: str):
        # 替换域名，或是 拼接url
        # 判断url是否完整
        # 检查请求协议、域名 or ip
        # 检查是否需要替换/添加 域名 ip

        if re.search(_url_compile, hosts) or re.search(_hosts_compile, hosts):
            if self._url_config["domain_name"] and re.search(self._url_config["domain_name"], hosts):
                new_hosts = hosts.replace(self._url_config["domain_name"], self._url_config["url"])
                return new_hosts
        elif self._url_config["url"]:
            new_hosts = parse.urljoin(self._url_config["request_way"] + "://" + self._url_config["url"], hosts)
            return new_hosts
        return hosts

    def jsonpath(self, data, expr):
        return jsonpath(data, expr)
