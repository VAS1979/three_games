"""Модуль содержит класс игры крестики-нолики, а также обьект класса,
который инициализируется из модуля bot.py.
"""

import random
import telebot

from utils.messages import (YOU_WIN, YOU_LOST, DRAW, OCCUPIED, NEXT_MOVE)


class Tttoe:
    """ Класс содержит атрибуты и методы
    игры крестики-нолики"""

    total_win = 0   # суммарное количество выигрышей
    total_lost = 0  # суммарное количество проигрышей
    total_draw = 0  # суммарное количество ничей

    def __init__(self):
        self.map = ['*' for i in range(9)]   # игровое поле

    def create_keyboard(self):
        """
        Формирует игровое поле, добавляет
        его в клавиатуру и возвращает клавиатуру
        """
        map_button = telebot.types.InlineKeyboardButton  # создание кнопки
        tttoe_buttons = []  # список для строк кнопок (по 3 кнопки)
        for i in range(3):  # цикл по строкам
            row = []    # список строки
            for j in range(3):  # цикл по кнопкам в строке
                if self.map[i * 3 + j] == '*':  # если в поле пусто
                    # добавляет в список строки пустую кнопку
                    row.append(map_button(text=' ',
                                          callback_data=str(i * 3 + j)))
                elif self.map[i * 3 + j] == 'X':  # если стоит крестик
                    # добавляет в список строки кнопку с крестиком
                    row.append(map_button(text='❌', callback_data='no'))
                elif self.map[i * 3 + j] == 'O':  # если стоит нолик
                    # добавляет в список строки кнопку с ноликом
                    row.append(map_button(text='⭕', callback_data='no'))
                    # добавляет строку c клавиатурой в список строк
            tttoe_buttons.append(row)
        # создает клавиатуру
        tttoe_keyboard_map = telebot.types.InlineKeyboardMarkup(tttoe_buttons,
                                                                row_width=3)
        return tttoe_keyboard_map  # возвращает клавиатуру

    def who_win(self):
        """
        Определяет победителя игры крестики-нолики
        """
        if self.map[0] == self.map[1] == self.map[2] == 'X' or \
            self.map[3] == self.map[4] == self.map[5] == 'X' or \
            self.map[6] == self.map[7] == self.map[8] == 'X' or \
            self.map[0] == self.map[3] == self.map[6] == 'X' or \
            self.map[1] == self.map[4] == self.map[7] == 'X' or \
            self.map[2] == self.map[5] == self.map[8] == 'X' or \
            self.map[0] == self.map[4] == self.map[8] == 'X' or \
            self.map[2] == self.map[4] == self.map[6] == 'X':
            return YOU_WIN
        elif self.map[0] == self.map[1] == self.map[2] == 'O' or \
            self.map[3] == self.map[4] == self.map[5] == 'O' or \
            self.map[6] == self.map[7] == self.map[8] == 'O' or \
            self.map[0] == self.map[3] == self.map[6] == 'O' or \
            self.map[1] == self.map[4] == self.map[7] == 'O' or \
            self.map[2] == self.map[5] == self.map[8] == 'O' or \
            self.map[0] == self.map[4] == self.map[8] == 'O' or \
            self.map[2] == self.map[4] == self.map[6] == 'O':
            return YOU_LOST
        elif '*' not in self.map:
            return DRAW
        return None

    def bot_move(self):
        """
        Генерирует ходы ИИ
        """
        ans = random.randint(0, 8)    # выбирает случайную клетку
        while self.map[ans] != '*':    # пока сгенерированная клетка не пустая
            ans = random.randint(0, 8)    # генерирует клетку
        return ans

    @classmethod
    def save_game(cls, res):
        """
        Суммирует итоги
        """
        if res == 1:
            cls.total_win += 1  # подсчет количества выигрышей
        elif res == 2:
            cls.total_lost += 1  # подсчет количества проигрышей
        else:
            cls.total_draw += 1  # подсчет количества ничей

    def return_results(self, message):
        """
        Принимает на вход аргумент в виде
        сообщения, формирует строку статистики
        и возвращает результат
        """
        text = f"""{message}
        Побед: {self.total_win}
        Поражений: {self.total_lost}
        Ничьи: {self.total_draw}"""
        return text

    def game_messages(self, message):
        """
        Принимает на вход аргумент в виде сообщения,
        формирует сообщения игры и статус окончания
        """
        # если сообщения об окончании игры
        if message not in [OCCUPIED, NEXT_MOVE]:
            # формирет и сохранет строку итогов
            text = self.return_results(message)
        else:   # если сообщения не об окончании игры
            text = f"{message}"  # сообщение делай следующий ход
        return text


object_tttoe = Tttoe()   # создание экземпляра класса
