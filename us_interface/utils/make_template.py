import os
import jinja2
from us_interface.utils.file_operations import get_all_subdirectories, load_yaml, locate_file

# todo:base_api已修改，下次需要根据新方式修改模板
__PAGE_TEMPLATE__ = jinja2.Template(
    """#page template
from us_interface.base.base_api import BaseApi
from us_interface.utils.file_operations import load_yaml


class {{ classname }}(BaseApi):
    _file_path = "{{ file_path }}"
    _{{page_data_name}} = load_yaml(_file_path)
{% for methodname in method_list %}
    def {{ methodname }}(self, **kwargs):
        api_data = self._{{page_data_name}}["{{ methodname }}"]
        p_data = 
        api_data = self.template_data(api_data, p_data)
        return self.request_http(api_data)
{% endfor %}
    """
)


__CONFTEST_TEMPLATE__ = jinja2.Template(
    """#first conftest.py
    from us_interface.utils.load_file import load_ini, locate_file
    import os
    test_path_root = os.path.getcwd()
    test_path = locate_file(test_path_root, "config.ini")
    _instance_ini = load_ini(test_path)
    _config = _instance_ini.get("config")
    _corp_id = _instance_ini.get("wwork", "corp_id")
    _contact_secret = _instance_ini.get("wwork", "contact_secret")
    
    def get_token():
        pass
    """
)


def make_api_page(api_files_path):
    """
    自动生成api page文件
    :return:
    """
    api_files_abs = os.path.abspath(api_files_path)

    # 查找或创建api_page目录
    root_abs_path = locate_file(api_files_abs, "env_config.ini")
    page_files_abs = os.path.join(os.path.dirname(root_abs_path), "api_page")
    if not os.path.isdir(page_files_abs):
        os.makedirs(page_files_abs)

    api_files = get_all_subdirectories(api_files_abs)

    for api_file in api_files:
        # 获取api yml文件内容
        api_file_abs = os.path.join(api_files_abs, api_file)
        yml_data = load_yaml(api_file_abs)

        api_file_name = str(api_file).split('.')[0]
        # 类名：去除_ 每个单词首字母大写 清空空格
        classname = api_file_name.replace("_", " ").title().replace(" ","")
        # api数据名称
        page_data_name = api_file_name+"_data"
        # page文件路径
        api_page_file_abs = os.path.join(page_files_abs, api_file_name + ".py")

        # 获取template上下文
        data = {
            "classname": classname,
            "page_data_name": page_data_name,
            "file_path": api_file_abs,
            "method_list": [ methodname for methodname in yml_data.keys()]
        }
        content = __PAGE_TEMPLATE__.render(data)

        # 写入文件
        with open(api_page_file_abs, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    path = "../../examples/api"
    make_api_page(path)