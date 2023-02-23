import hashlib
import requests
import json


def signedUtil(data, secretKey):
    key = data+secretKey
    print(key)
    hash = hashlib.md5()
    hash.update(key.encode("utf-8"))
    return hash.hexdigest()


def send_request():
    secretkey = "kG62V5xgvcKjpyzW5thhusDQtliWjyYF"
    # 创建签名
    print('请输入人群类型：')
    personType = int(input())

    print('请输入结案身份证号：')
    num1 = input()
    # 新增身份证号
    print('请输入新增身份证号：')
    num2 = input()
    params = {"type": personType, "closecase":[] if num1 =="" else [num1] , "added": [num2]}
    jsonData = json.dumps(params, ensure_ascii=False)
    print(jsonData)
    signed = signedUtil(jsonData, secretkey)
    print('-------------'+signed)
    header = {'content-type':'text/plain', 'signed': signed}
    url = "http://tt-poc-his.seenew.info/app-publichealth-data-service/healthRecord/childGravidaUpdateState"

    r = requests.post(url, data=jsonData, headers=header)
    print(r.text)


if __name__ == '__main__':
    send_request()