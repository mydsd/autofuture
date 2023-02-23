import hashlib


def gen_token(sys_time):
    app_key = "96c0dd548137fceab40d776a8ddb9319"
    str_code = app_key + str(sys_time)
    m = hashlib.md5()
    str_encode = str_code.encode(encoding='utf-8')
    m.update(str_encode)
    token = m.hexdigest()
    print(token)
    return token


if __name__ == '__main__':
    import time
    gen_token('123')
