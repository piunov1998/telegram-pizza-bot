from brain import PizzaBot
import requests, json, sys, time


with open('settings.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

headers = {'Content-Type': 'application/json'}
url = data['https'] + data['token'] + '/'
offset = data['offset']
clients = {}


def get_updates(offset:int = 0):
    updates = requests.get(url + f'getUpdates?offset={offset}').json()['result']
    return updates

def send_message(chat_id:int, text:str, reply_markup:bool=False):
    
    msg = {
        'chat_id': chat_id,
        'text': text
    }

    if clients[chat_id].getAnswers():
        msg['reply_markup'] = {
            'keyboard':[
                [{'text': clients[chat_id].getAnswers()[0]}, {'text': clients[chat_id].getAnswers()[1]}]
            ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        }

    requests.post(url=url + 'sendMessage', headers=headers, json=msg)

def keyboard_builder(variants:list, chat_id: int):
    keyboard = []
    for i in range(0, variants // 2):
        keyboard.append([{'text': variants}, {}])

def save(offset:str):
    data['offset'] = offset
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3)


while True:
    #time.sleep(0.1)
    updates = get_updates(offset)
    for update in updates:
        last_update_id = update['update_id']
        if last_update_id > offset:
            offset = last_update_id
            chat_id = update['message']['chat']['id']
            text = update['message']['text']
            if not chat_id in clients:
                clients[chat_id] = PizzaBot()
            send_message(chat_id, clients[chat_id].chat(text), reply_markup=True)
            if clients[chat_id].state == 'idle':
                clients.pop(chat_id)