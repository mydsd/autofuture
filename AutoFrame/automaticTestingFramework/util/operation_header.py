import json
from automaticTestingFramework.util.operation_json import OperationJson
from automaticTestingFramework.conf import env_conf


class OperationHeader:

    def __init__(self, response):
        self.response = json.loads(response)
        self.op_json = OperationJson()
        self.op_header_json = OperationJson(env_conf.HEADER_DATA_PATH)

    def get_response_token(self):
        """
        获取生成的token
        """
        token = {"token": self.response["token"]}
        return token

    def write_token(self):
        self.op_json.write_data(self.get_response_token(), env_conf.Token_DATA_PATH)

    def write_header(self, key, value):
        self.op_header_json.write_to_header_json(key, value, env_conf.HEADER_DATA_PATH)

