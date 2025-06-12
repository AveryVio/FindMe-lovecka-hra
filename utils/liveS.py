from http.client import *
from random import *
from time import *

reqs = [
    '{"huntid":"53BA00"}',
    '{"huntid":"D0C111"}',
    '{"huntid":"017A00"}',
    '{"huntid":"A53B10"}',
    '{"huntid":"5BAC70"}',
    '{"huntid":"BA57A0"}',
    '{"huntid":"C141C1"}',
    '{"huntid":"C0CC11"}',
    '{"huntid":"51C801"}',
    '{"huntid":"800850"}',
]

while True:
    num = randrange(len(reqs))
    print("'" + reqs[num] + "'")
    conn = HTTPConnection(host='localhost', port=5000, timeout=10)
    conn.request("POST", "/add_hunt", headers={"Host": "localhost:5000", "Content-Length": str(len(reqs[num])), "Content-Type": "application/json"}, body=reqs[num])
    print("'" + conn.getresponse().read().decode("utf-8") + "'")
    sleep(uniform(3.3,6.1))