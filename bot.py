from transitions import Machine

class PizzaBot:

    """
    Класс бота. Для взаимодействия с ботом достаточно вызвать метод chat() на экземпляре класса,
    что позволяет взаимодействовать с любыми платформами через разные интерфейсы
    """
    
    states = ['idle', 'pizza_size', 'payment_method', 'confirm']

    def __init__(self) -> None:
        self.pizza_size = ''
        self.payment_method = ''

        self.machine = Machine(model=self, states=self.states, initial='idle')

        self.machine.add_transition(trigger='start', source='*', dest='pizza_size')
        self.machine.add_transition(trigger='size_selected', source='pizza_size', dest='payment_method')
        self.machine.add_transition(trigger='payment_selected', source='payment_method', dest='confirm')
        self.machine.add_transition(trigger='idle', source='*', dest='idle')
        

    def chat(self, msg: str) -> str:
        """
        Основная функция бота, принимает в качестве аргумента сообщение и возвращает ответ
        В зависимости от полученных сообщений выполняет переключение состояний
        При завершении диалога вызывает функцию order()
        """
        choice = msg.lower().lstrip().removesuffix('.')
        match self.state:
            case 'idle':
                if choice == 'start':
                    self.start()
                    return 'Какую вы хотите пиццу? Большую или маленькую?'
                else:
                    return 'Отправте start для начала'

            case 'pizza_size':
                if choice in self.getAnswers():
                    self.pizza_size = choice
                    self.size_selected()
                    return 'Как вы будете платить?'
                else:
                    return 'Пожалуйста, выберете размер пиццы из предложенных вариантов'

            case 'payment_method':
                if choice in self.getAnswers():
                    self.payment_method = choice
                    self.payment_selected()
                    return f'Вы хотите {self.pizza_size} пиццу, оплата - {self.payment_method}?'
                else:
                    return 'Пожалуйста, выберете способ оплаты из предложенных (картой/наличкой)'

            case 'confirm':
                if choice in self.getAnswers():
                    if choice == 'да':
                        self.order()
                        return 'Спасибо за заказ'
                    elif choice == 'нет':
                        self.idle()
                        return self.chat('start')
                else:
                    return 'Пожалуйста выберете Да / Нет'


    def order(self, size: str='', payment: str=''):
        """
        Функция, вызывающаяся при подтверждении заказа
        Есть возможность вызова отдельно с указанием параметров заказа
        """
        if not size:
            size = self.pizza_size
        if not payment:
            payment = self.payment_method

        """
        
        Код выполнения заказа

        """

        self.idle()


    def getAnswers(self) -> list:
        """
        Возвращает список вариантов ответа в зависимости от состояния
        """
        match self.state:
            case 'idle':
                return []
            case 'pizza_size':
                return ['маленькую', 'большую']
            case 'payment_method':
                return ['картой', 'наличкой']
            case 'confirm':
                return ['да', 'нет']