$text = cat ./checkpointid.txt
$input = 's/uint8_t advData\[\]={.*}/uint8_t advData[]={' + $text + '}/g'

#"%LOCALAPPDATA%\Microsoft\WinGet\Links\sed.exe -i -e 's/uint8_t advData\[\]={.*}/uint8_t advData[]={$(cat checkpointid.txt)}/g' ../hell.txt"

sed -i -e $input ..\src\app_ble\app_ble.c