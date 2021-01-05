import json, os, yaml
from loguru import logger


def get_current_path() -> str:
    # 获取当前工作目录绝对路径
    return os.getcwd()


def _load_json_file(json_file):
    """
    获取json文件内容
    :param json_file:
    :return:
    """
    with open(json_file, encoding="utf-8") as data_path:
        try:
            json_content = json.load(data_path)
            print(json_content)
        except json.JSONDecodeError as error:
            err_msg = f"JsonError:\nfile: {json_file}\nerror: {error}"
            raise err_msg
        return json_content


def _load_yaml_file(yaml_file):
    """
    根据路径获取yaml文件内容
    :param path:
    :return:
    """
    with open(yaml_file, encoding='utf-8') as casepath:
        try:
            yaml_content = yaml.safe_load(casepath)
        except yaml.YAMLError as error:
            err_msg = f"YamlError:\nfile: {yaml_file}\nerror: {error}"
            raise err_msg

    return yaml_content


def load_files(load_file, load_type='yml'):
    # 传入路径与模式，加载文件内容
    if not os.path.isfile(load_file):
        raise FileNotFoundError(f"load_file not exists: {load_file}")

    if load_type == "yaml" or load_type == "yml":
        file_content = _load_yaml_file(load_file)
    elif load_type == "json":
        file_content = _load_json_file(load_file)
    else:
        raise("Load File Type should be 'option'、'test' or 'json' ")
    return file_content


def get_all_subdirectories(path=get_current_path(), filter_name=None) -> list:
    # 获取目录下的文件名
    # 默认是当前目录
    # 根据filter_name指定所需文件，默认返回全部
    file = os.listdir(path)
    if filter_name:
        if filter_name in file:
            filter_file = []
            for file_name in file.copy():
                if filter_name in file_name:
                    filter_file.append(file_name)
            return filter_file
        else:
            logger.error("需要的文件或文件类型不存在：%s \n" % filter_name)
            raise("需要的文件类型不存在")
    else:
        return file


def mkdir_file(file_path, file_name):
    # 创建一个目录
    if not os.path.isdir(file_path):
        raise("不是一个目录")

    new_file_name = os.path.join(file_path, file_name)
    if os.path.exists(new_file_name):
        return new_file_name
    os.mkdir(new_file_name)
    return new_file_name


def locate_file(start_path, file_name):
    """ locate filename and return absolute file path.
        searching will be recursive upward until system root dir.

    Args:
        file_name (str): target locate file name
        start_path (str): start locating path, maybe file path or directory path

    Returns:
        str: located file path. None if file not found.

    Raises:
        exceptions.FileNotFound: If failed to locate file.

    """
    if os.path.isfile(start_path):
        start_dir_path = os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_dir_path = start_path
    else:
        raise (f"invalid path: {start_path}")

    file_path = os.path.join(start_dir_path, file_name)
    if os.path.isfile(file_path):
        # ensure absolute
        return os.path.abspath(file_path)

    # system root dir
    # Windows, e.g. 'E:\\'
    # Linux/Darwin, '/'
    parent_dir = os.path.dirname(start_dir_path)
    if parent_dir == start_dir_path:
        raise (f"{file_name} not found in {start_path}")

    # locate recursive upward
    return locate_file(parent_dir, file_name)


def load_har_file(har_file):
    with open(har_file, "rb") as f:
        try:
            test_content = json.load(f)
            return test_content["log"]["entries"]
        except Exception as error:
            logger.error(f"failed to load HAR file {har_file}: {error}")


def dump_yml(data, file_path):
    logger.info("生成yaml文件 \n")
    with open(file_path, "w") as out_file:
        yaml.dump(data, out_file, allow_unicode=True, default_flow_style=False, indent=4)
    logger.info("yaml用例文件生成成功 \n")
