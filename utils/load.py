from http.client import *
from random import *

test_inputs = [
    ['{"huntid":"53BA00"}'],
    ['{"huntid":"53BA00"}','{"huntid":"53BA00"}','{"huntid":"53BA00"}','{"huntid":"53BA00"}','{"huntid":"D0C111"}'],
    ['{"huntid":"A53B10"}','{"huntid":"53BA00"}','{"huntid":"017A00"}','{"huntid":"D0C111"}','{"huntid":"D0C111"}','{"huntid":"D0C111"}','{"huntid":"D0C111"}','{"huntid":"A53B10"}','{"huntid":"D0C111"}','{"huntid":"53BA00"}'],
    ['{"huntid":"53BA00"}','{"huntid":"D0C111"}','{"huntid":"A53B10"}'],
    ['{"huntid":"5BAC70"}','{"huntid":"53BA00"}','{"huntid":"53BA00"}','{"huntid":"BA57A0"}','{"huntid":"5BAC70"}']
]

group = test_inputs[randrange(len(test_inputs))]

for req in group:
    print("'" + req + "'")
    conn = HTTPConnection(host='localhost', port=5000, timeout=10)
    conn.request("POST", "/add_hunt", headers={"Host": "localhost:5000", "Content-Length": str(len(req)), "Content-Type": "application/json"}, body=req)
    print("'" + conn.getresponse().read().decode("utf-8") + "'")