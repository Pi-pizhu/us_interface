# 入口->pytest.main或者pytest命令行
# 单例加载全局配置 -> 提供访问
import os

from us_interface.utils.load_file import load_ini


class GlobalConfig:

    _first_init = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, work_path=None):
        if not self._first_init:
            work_path = work_path or os.getcwd()
            self._config_path = os.path.join(work_path, "env_config.ini")
            self._get_ini_instance(self._config_path)
            self._global_config = {}
            self._first_init = True

    def _get_ini_instance(self, config_path):
        self._ini_instance = load_ini(config_path)

    def get_global_variable(self, section, option):
        if self._global_config.get(section, {}).get(option):
            return self._global_config.get(section).get(option)
        else:
            try:
                variable = self._ini_instance.get(section=section, option=option)
                self._global_config.update({section: {option: variable}})
                return variable
            except Exception as error:
                err_msg = f"faile load variable section:{section} option:{option}\n"
                err_msg += str(error)