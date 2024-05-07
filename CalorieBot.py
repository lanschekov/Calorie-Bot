import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class CalorieBot(VkBotLongPoll):
    """ Бот, предоставляющий информацию о суточной норме калорий. """

    # Состояния бота по ходу диалога:
    BEGINNING = 0
    GENDER = 1
    AGE = 2
    HEIGHT = 3
    WEIGHT = 4

    def __init__(self, vk_session: vk_api.VkApi) -> None:
        super(CalorieBot, self).__init__(vk=vk_session, group_id=225809166)

        self.state = None
        self.gender = None
        self.age = None
        self.height = None
        self.weight = None

    def start(self) -> None:
        """ Этот метод вызывается самым первым для того, чтобы начать работу бота. """

        self.state = self.BEGINNING
        for event in self.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                # Обработанное сообщение пользователя и его идентификатор
                msg_text = self.get_clean_message(event.obj.message['text'])
                user_id = event.obj.message['from_id']

                if not self.is_valid_message(msg_text):
                    # Отправляем сообщение о некорректности данных на данном этапе
                    self.send_message(user_id, 'Ожидание корректного сообщения...')
                    continue

                # Ответ пользователю в зависимости от этапа диалога
                response = ''

                if self.state == self.BEGINNING:
                    response = 'Введите ваш пол: (М / Ж)'
                    self.state = self.GENDER

                elif self.state == self.GENDER:
                    self.gender = msg_text
                    response = 'Сколько вам полных лет? (Например, 34)'
                    self.state = self.AGE

                elif self.state == self.AGE:
                    self.age = int(msg_text)
                    response = 'Введите ваш рост: (Например, 175.2)'
                    self.state = self.HEIGHT

                elif self.state == self.HEIGHT:
                    self.height = float(msg_text)
                    response = 'Введите ваш вес: (Например, 65.6)'
                    self.state = self.WEIGHT

                elif self.state == self.WEIGHT:
                    self.weight = float(msg_text)
                    # Вычисляем суточную норму калорий
                    calories = self.calculate_calories()
                    response = f'''Количество калорий для поддержания веса тела: {round(calories, 2)}.
                    Начать заново? (Да / Запуск)'''
                    self.state = self.BEGINNING

                # Отвечаем пользователю
                self.send_message(user_id, response)

    def is_valid_message(self, message) -> bool:
        """ Проверить корректность сообщения пользователя в зависимости от состояния бота. """

        if self.state == self.BEGINNING:
            return message in ('да', 'запуск')
        if self.state == self.GENDER:
            return message in ('м', 'ж')
        if self.state == self.AGE:
            return message.isdigit()
        if self.state in (self.HEIGHT, self.WEIGHT):
            return message.replace('.', '').isdigit()

        return False

    def get_clean_message(self, message: str) -> str:
        """ Вернуть обработанный вариант сообщения. """

        return message.lower().strip().replace(',', '.')

    def send_message(self, user_id, message: str) -> None:
        """ Отправить сообщение адресату. """

        self.vk.get_api().messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(0, 2 ** 64)
        )

    def calculate_calories(self) -> float:
        """ Вычислить по полученным данным суточную норму калорий для поддержания веса. """

        if self.gender == 'м':
            # Для мужчины
            return self.height * 5 - self.age * 6.8 + self.weight * 13.7 + 66
        else:
            # Для женщины
            return self.height * 1.8 - self.age * 4.7 + self.weight * 9.6 + 655
