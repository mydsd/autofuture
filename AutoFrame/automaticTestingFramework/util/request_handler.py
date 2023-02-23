import json
import requests
from automaticTestingFramework.conf import env_conf
from automaticTestingFramework.util.operation_json import OperationJson


class RequestHandler:
    def post_request(self, url, data, header=None):
        res = None
        if header is not None:
            res = requests.post(url=url, json=data, headers=header, verify=False)
        else:

            res = requests.post(url=url, json=data, verify=False)
        if 'application/json' in res.headers.get('Content-Type'):
            # return res.json()
            return json.dumps(res.json(), sort_keys=True, ensure_ascii=False)
        else:
            return '<textarea>' + res.text + '</textarea>'

    def get_request(self, url, data=None, header=None):
        res = None
        if header is not None:
            res = requests.get(url=url, params=data, headers=header, verify=False)
        else:
            res = requests.get(url=url, params=data, verify=False)
        if 'application/json' in res.headers.get('Content-Type'):
            # return res.json()
            return json.dumps(res.json(), sort_keys=True, ensure_ascii=False)
        else:
            return '<textarea>' + res.text + '</textarea>'

    def send_request(self, method, url, data=None, header=None,envHost=None):
        res = None
        if method == 'post':
            res = self.post_request(envHost + url, data, header)
        else:
            res = self.get_request(envHost + url, data, header)
        return res
        # return json.dumps(res, sort_keys=True, ensure_ascii=False)

