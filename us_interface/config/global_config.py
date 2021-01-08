# 入口->pytest.main或者pytest命令行
# 单例加载全局配置 -> 提供访问
import os

from us_interface.utils.file_operations import load_ini

"""
全局配置信息
全局数据替换场景

接口参数替换

url替换

局部变量：
    一般是有接口依赖时，从上一个接口提取，传入teststep进行接口参数替换
    这个不用管了
    
优先级：局部变量>全局配置
从$ 或 ${} 中提取变量名
匹配局部变量
    匹配局部变量 
    剩余的再匹配全局配置
    如果还有剩 则记录 警告 但不报错
"""


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
            self.config_var = self._get_config_var()
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

    def _get_config_options(self):
        # 获取全局配置的信息名称
        return self._ini_instance.options("config")

    def _get_config_var(self) -> dict:
        # 获取全局配置信息
        options = self._get_config_options()
        config_var = {}
        for option in options:
            config_var[option] = self.get_global_variable("config", option)
        return config_var