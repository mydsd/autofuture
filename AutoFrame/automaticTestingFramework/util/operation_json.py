import json
from automaticTestingFramework.conf import env_conf


def init_json_data(json_file):
    with open(json_file, 'w') as fp:
        fp.write(json.dumps({}))


class OperationJson:
    """操作json文件"""

    def __init__(self, file_path=None):
        if file_path == None:
            self.file_path = env_conf.Token_DATA_PATH
        else:
            self.file_path = file_path
        self.data = self.read_data()

    def read_data(self):
        """
        读取json文件
        :param file_name:文件路径
        :return:
        """
        with open(self.file_path) as fp:
            data = json.load(fp)
            return data

    def get_data(self, key):
        """根据关键字获取对应数据"""
        newest_data = self.read_data()
        if key in newest_data:
            return newest_data[key]
        else:
            return None

    # 写入json
    def write_data(self, data, json_file):
        with open(json_file, 'w') as fp:
            fp.write(json.dumps(data))

    # 写入全局变量json
    def write_to_global_vars(self, prefix='@', key='', value=''):
        newest_data = self.read_data()
        newest_data[key] = value
        with open(env_conf.GLOBAL_DATA_PATH, 'w') as fp:
            fp.write(json.dumps(newest_data))

    # 写入全局变量json
    def write_to_header_json(self, key='', value='', file_path=env_conf.HEADER_DATA_PATH):
        newest_data = self.read_data()
        newest_data[key] = value
        with open(file_path, 'w') as fp:
            fp.write(json.dumps(newest_data))


if __name__ == '__main__':
    op_json = OperationJson()
    print(op_json.read_data())
    print(op_json.get_data('token'))
