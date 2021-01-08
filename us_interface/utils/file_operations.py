import os
import re

from loguru import logger
import yaml
from us_interface.plugin.myconfigparser import MyConfigParser


def load_yaml(file_path):
    try:
        with open(file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data
    except Exception as error:
        raise error


def load_ini(ini_file):
    instance_ini = MyConfigParser()
    try:
        instance_ini.read(ini_file, encoding='utf-8')
        return instance_ini
    except Exception as error:
        error = f"IniError:\nfile: {ini_file}\nerror: {error}"


def get_all_subdirectories(path, filter_name=None) -> list:
    # 获取目录下的文件名
    # 默认是当前目录
    # 根据filter_name指定所需文件，默认返回全部
    file = os.listdir(path)
    if filter_name:
        filter_file = []
        for file_name in file.copy():
            if filter_name in file_name:
                filter_file.append(file_name)

        if len(filter_file) == 0:
            logger.error("需要的文件或文件类型不存在：%s \n" % filter_name)
            raise ("需要的文件类型不存在")

        return filter_file

    else:
        return file


def locate_file(start_path, file_name):
    # 不断向前更新目录，直到查找到对应的filename 或者 到根目录抛出错误

    if os.path.isfile(start_path):
        start_path_dir = os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_path_dir = start_path
    else:
        raise FileNotFoundError(f"invalid path: {start_path}")

    file_path = os.path.join(start_path_dir, file_name)
    if os.path.isfile(file_path):
        return os.path.abspath(file_path)

    parent_dir = os.path.dirname(start_path_dir)
    if parent_dir == start_path_dir:
        raise FileNotFoundError(f"{file_name} not found in {start_path}")
    return locate_file(parent_dir, file_name)


"""
pytest 执行方式：
    描述     path1   +   path2
    在根目录：/ + 输入用例绝对路径
    在测试用例根目录： abspath(tester) + 输入用例相对路径
    在测试用例其中一个用例目录：/User/us_interface/examples/contact/department/ + ../../member/test_member.py
    在框架目录：/User/us_interface/us_interface/utils/ + 绝对路径 or ../../相对路径
    在其他目录：/opt + 绝对路径
    检测path2是否是绝对路径，是则直接引用
    否 则path1 + path2 转换成绝对路径
"""


def path_extract(original_path: str) -> str:
    """
    路径提取 返回绝对路径
    用于pytest特性：指定单个用例执行 例如：pytest test_case/main/test_home.py::TestHome::test_search
    提取出完整的文件路径：test_case/main/test_home.py
    :param original_path:
    :return:
    """
    is_path = re.search(r"::", original_path)
    if is_path:
        extract_path = original_path.split("::")[0]
        complete_path = os.path.abspath(extract_path)
        if not os.path.exists(complete_path):
            raise Exception(f"用例指定路径不存在：{original_path}")
        return complete_path
    else:
        if not os.path.isabs(original_path):
            original_path = os.path.abspath(original_path)

        if not os.path.exists(original_path):
            raise Exception(f"用例指定路径不存在：{original_path}")
        return original_path


if __name__ == '__main__':
    print(path_extract("../../examples/contact/department/test_department.py::TestDepartment::test_add_depart"))
    print(os.path.join("/Users", "/Users/yewenkai/PycharmProjects/us_interface"))
    print(path_extract("test_case/main/test_home.py::TestDepartment::test_add_depart"))
