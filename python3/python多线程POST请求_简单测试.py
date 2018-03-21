# coding = utf-8

import time
from urllib import request, parse
from urllib.error import URLError
import threading


class postRequest():
    def __init__(self, url, values, interfaceName):
        self.url = url
        self.values = values
        self.interfaceName = interfaceName

    def post(self):
        params = self.values
        queryString = parse.urlencode(params)
        try:
            u = request.urlopen(self.url, queryString.encode('ascii'))
            resp = u.read()
            print(u"接口名字为：", self.interfaceName)
            print(u"所传递的参数为：\n", params)
            print(u"服务器返回值为：\n", resp)
        except URLError as e:
            print(u"e ====== ", e)


def Login():
    # 实例化接口对象
    login = postRequest('http://xxxx.com/?' + str(time.time()), {}, "")
    return login.post()


try:
    i = 0
    tasks = []
    taskNumber = 300
    while i < taskNumber:
        t = threading.Thread(target=Login)
        tasks.append(t)
        t.start()
except Exception as e:
    print('while====error ', e)
