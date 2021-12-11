import requests, json, sys, re
from bot import PizzaBot
from os import path

# Проверка существует ли файл с пользовательскими данными
# Если файла нет, он создается и в него вносится токен
if not path.exists('./settings.json'):
    while True:
        token = input('Enter your bot token: ')
        if re.fullmatch(r'\d+:[A-Za-z0-9_-]{35}', token):
            break
    data = {
        'token': token,
        'offset': 0
    }
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

# Загрузка пользовательских данных (токен и информация о последнем обработанном сообщении)
with open('settings.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

headers = {'Content-Type': 'application/json'}
url = 'https://api.telegram.org/bot' + data['token'] + '/'
offset = data['offset']
clients = {}


def get_updates(offset:int = 0) -> list:
    """
    Возвращает список обновлений, полученных через GET запрос
    Принимает в качестве аргумента номер обновления, с которого необходимы данные
    """
    updates = requests.get(url + f'getUpdates?offset={offset}').json()['result']
    return updates


def send_message(chat_id:int, text:str) -> None:
    """
    Принимает в качестве аргументов ID чата и содержание сообщения для отправки
    Отправляет сообщение с указанными параметрами путем POST запроса
    Функция формирует Message объект, запрашивая варианты ответа для кастомной клавиатуры у основного тела бота
    """
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
    else:
        msg['reply_markup'] = {
            'remove_keyboard': True
        }

    requests.post(url=url + 'sendMessage', headers=headers, json=msg)


def save(offset:str) -> None:
    """Сохраняет текущий offset в файл. Выполняется при завершении программы"""
    data['offset'] = offset
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3)


"""
Цикл, постоянно выполняющий опрос сервера на наличие новых обновлений
При появлении таковых получает информацию из них и вызывает метод chat() основного тела бота
Для новых чатов создает отдельный экземпляр класса бота, при завершении общения ссылка на экземпляр удаляется
и он остается на растерзание уборщика мусора
"""
while True:
    try:
        updates = get_updates(offset)
        for update in updates:
            last_update_id = update['update_id']
            if last_update_id > offset:
                offset = last_update_id
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                if not chat_id in clients:
                    clients[chat_id] = PizzaBot()
                send_message(chat_id, clients[chat_id].chat(text))
                if clients[chat_id].state == 'idle':
                    clients.pop(chat_id)
    except KeyboardInterrupt:
        save(offset)
        sys.exit()
    except Exception as error:
        print(error)