import os
from loguru import logger
import yaml
from ..plugin.myconfigparser import MyConfigParser


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