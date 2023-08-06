import os
import configparser
local_path = os.path.dirname(os.path.realpath(__file__))


class Config:
    def __init__(self):
        self.conf_file_path = os.path.join(local_path, 'config.ini')
        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_file_path, encoding='utf-8')

    def get_name(self, module, key):
        if not self.cf.has_option(module, key):
            print('未找到该数据')
            value = None
        else:
            value = self.cf.get(module, key)
        return value

    def set_name(self, module, key, value):
        if not self.cf.has_section(module):
            self.cf.add_section(module)
        self.cf.set(module, key, value)
        with open(self.conf_file_path, 'w') as f:
            self.cf.write(f)


# 初始化
conf = Config()

