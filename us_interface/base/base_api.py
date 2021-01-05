import json
import re
from urllib import parse
import requests
from string import Template
from us_interface.config.global_config import GlobalConfig
from loguru import logger
from jsonpath import jsonpath


_url_compile = re.compile(r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$")
_hosts_compile = re.compile(r"^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)")

class BaseApi:
    _gl_config = GlobalConfig("/Users/yewenkai/PycharmProjects/HogwartsSDET14/us_interface/examples")
    _request_way = "https" or _gl_config.get_global_variable("env", "request_way")
    _domain_name = _gl_config.get_global_variable("hosts", "domain_name")
    _url = _gl_config.get_global_variable("hosts", _gl_config.get_global_variable("hosts", "default"))

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
            if self._domain_name and re.search(self._domain_name, hosts):
                new_hosts = hosts.replace(self._domain_name, self._url)
                return new_hosts
        elif self._url:
            new_hosts = parse.urljoin(self._request_way + "://" + self._url, hosts)
            return new_hosts
        return hosts

    def jsonpath(self, data, expr):
        return jsonpath(data, expr)


if __name__ == '__main__':
    a = BaseApi()
    print(a.replace_hosts("https://qyapi.weixin.qq.com/cgi-bin/oa/schedule/add"))