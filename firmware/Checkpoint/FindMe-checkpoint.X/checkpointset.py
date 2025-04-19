import subprocess
import random
import time

#! Data format for the ble advData string
#
# example: 0x02, 0x01, 0x05, 0x11, 0x09, 0x46, 0x69, 0x6E, 0x64, 0x4D, 0x65, 0x43, 0x68, 0x63, 0x68, 0x70, 0x6F, 0x69, 0x6E, 0x74
#
#* format: STX, SOH, ENQ, {length of data}, HT, {data}

# a set length for the id
leng = 0x10
# generate the id from call capital letters A-Z
checkpointid = ""
random.seed(time.time())
for i in range(0, leng):
    checkpointid = checkpointid + random.choice([', 0x41',', 0x42',', 0x43',', 0x44',', 0x45',', 0x46',', 0x47',', 0x48',', 0x49',', 0x4A',', 0x4B',', 0x4C',', 0x4D',', 0x4E',', 0x4F',', 0x50',', 0x51',', 0x52',', 0x53',', 0x54',', 0x55',', 0x56',', 0x57',', 0x58',', 0x59',', 0x5A'])

# put the id into the ble advertising data string
advData = "0x02, 0x01, 0x05, " + hex(leng).upper().replace('X', 'x') + ", 0x09" + checkpointid

# put advData into the regex string for sed
input = 's/uint8_t advData\\[\\]={.*}/uint8_t advData[]={' + advData + '}/g'

# run sed to edit the source file
subprocess.run(["sed", "-i ", input, "..\\src\\app_ble\\app_ble.c"])