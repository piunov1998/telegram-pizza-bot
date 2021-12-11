import sys
from bot import PizzaBot


test_mode = input('Choose testing mode:\n(1) Manual\n(2) Auto\n')
if not test_mode.isnumeric():
    print('Wrong input')
    sys.exit()

if int(test_mode) == 1:
    print('Manual testing has been started. Input chat messages to bot to interact with it')
    bot = PizzaBot()
    print('\nCreated bot example', bot)
    while True:
        try:
            print(bot.chat(input()))
        except KeyboardInterrupt:
            print('Finishing testing')
            sys.exit()

elif int(test_mode) == 2:
    i = 1
    print('Auto testing has been started.')
    test_case = [
        ['start', 'Большую', 'Наличкой', 'Да.'],
        ['start', 'маленькую', 'картой', 'нет', 'большую', 'картой', 'да'],
        ['strat', 'start', 'small', 'маленькую', 'by card', 'картой', 'yes', 'да']
        ]
    for case in test_case:
        bot = PizzaBot()
        print(f'\nTest case #{i}\nCreated bot example', bot)
        for input in case:
            print('-', input)
            print('-', bot.chat(input))
        i += 1
else:
    print('Wrong input')