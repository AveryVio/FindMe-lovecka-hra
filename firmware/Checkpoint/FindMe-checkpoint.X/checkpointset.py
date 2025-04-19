import subprocess

text = open('checkpointid.txt', 'r').read()
#with open('checkpointid.txt') as f:
#    text = f.read()
#    f.close()

input = 's/uint8_t advData\\[\\]={.*}/uint8_t advData[]={' + text + '}/g'

subprocess.run(["sed", "-i -e", input, "..\\src\\app_ble\\app_ble.c"])