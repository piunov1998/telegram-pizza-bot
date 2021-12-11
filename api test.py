import requests, json

headers = {'Content-Type': 'application/json'}


r = requests.get(url='https://api.telegram.org/bot5091246162:AAGmcQUi_lhpkvmE5GeiDC2bFUkuNb489-Q/getUpdates', headers=headers)
#r = requests.post(url='https://api.telegram.org/bot5091246162:AAGmcQUi_lhpkvmE5GeiDC2bFUkuNb489-Q/sendMessage?chat_id=323754099&text=иди%0нахуй', headers=headers)
print(r.json())