"""
用于用例中的变量处理
"""
import json
from string import Template

from utils import codec


def template(test_case, data):
    try:
       return json.loads(Template(json.dumps(test_case)).substitute(data))
    except Exception as error:
        print(error)


def parser_string(raw_data, module, **kwargs):
    pass

def parse_data(raw_data, module=codec, **kwargs):
    if isinstance(raw_data, str):
        raw_data = raw_data.strip("\t")
        return parser_string(raw_data, module, **kwargs)
    elif isinstance(raw_data, list):
        pass
    elif isinstance(raw_data, dict):
        pass
    else:
        return raw_data