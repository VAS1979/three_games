"""Модуль содержит класс игры Викторина, а также обьект класса,
который инициализируется из модуля bot.py.
"""

import random
import telebot
from telebot import types

from .questions import questions_list


class Quiz:
    '''
    Класс содержит атрибуты и методы
    используемые в игре Викторина
    '''
    total_score = 0  # суммарное количество очков
    games_total = 0  # суммарное количество сыгранных игр

    def __init__(self):
        self.current_question = 0   # номер текущего вопроса
        self.score = 0   # счет за текущий раунд
        self.check_list = []    # список использованных вопросов из словаря
        self.question = None    # текущий вопрос
        self.answers = None      # текущий ответ

    def random_question(self):
        '''
        Берет из словаря случайный вопрос, проверяет
        на уникальность и сохраняет в атрибут self.question
        '''
        # рандомно берет вопрос
        question = random.choice(list(questions_list.keys()))
        # если нет в списке self.check_list
        if question not in self.check_list:
            self.check_list.append(question)  # добавляет в список
            self.question = question    # сохраняет в self.question
        else:   # если вопрос присутствует в списке
            # обрабатывает цикл, до тех пор пока вопрос в списке
            while question in self.check_list:
                # рандомно берет вопрос
                question = random.choice(list(questions_list.keys()))
            # если вопроса нет  в списке - добавляет его
            self.check_list.append(question)
            self.question = question    # сохраняет в self.question

    def current_answers(self):
        '''
        Запрашивает ответы на текущий вопрос из словаря
        и сохраняет в атрибут self.answers
        '''
        # берет ответы на текущий вопрос по ключу
        answers = questions_list[self.question]
        self.answers = answers  # сохраняет в self.answers

    def controls(self):
        '''
        Вызывает методы random_question() и current_answers(),
        строит клавиатуру, рандомно меняет местами кнопки,
        возвращает клавиатуру с добавленными кнопками
        '''
        self.random_question()  # берет вопрос
        self.current_answers()  # берет ответы
        # создает инлайн  клавиатуру
        keyboard_quiz = telebot.types.InlineKeyboardMarkup(row_width=1)
        used_answer = []    # список ответов на текущий вопрос
        answer = None   # переменная для хранения ответа
        for _ in range(2):
            # если ответа нет в списке used_answer
            if answer not in used_answer:
                answer = random.choice(list(self.answers))  # сохраняет ответ
                # сохраняет значение ответа (True, False)
                value = (self.answers[str(answer)])
                used_answer.append(answer)  # добавляем ответ в список ответов
                button1 = types.InlineKeyboardButton(text=answer,
                                                     callback_data=str(value))
            else:   # если ответ есть в списке used_answer
                # до тех пор пока ответ в used_answer
                while answer in used_answer:
                    # сохраняет в переменную рандомный ответ
                    answer = random.choice(list(self.answers))
                    # сохраняет значение ответа (True, False)
                value = (self.answers[str(answer)])
                used_answer.append(answer)  # добавляем ответ в список ответов
            button2 = types.InlineKeyboardButton(text=answer,
                                                 callback_data=str(value))
        keyboard_quiz.add(button1, button2)
        return keyboard_quiz    # возврат клавиатуры

    @classmethod
    def save_game(cls, obj):
        '''
        Суммирует итоги игры и
        сохраняет в атрибуты класса
        '''
        cls.games_total += 1  # подсчет количества игр
        cls.total_score += obj.score  # подсчет суммарных очков по всем играм

    def finish_results(self):
        '''
        Возвращает итоги игры F-строкой.
        Обнуляет текущий счет и количество
        заданных вопросов.
        '''
        text = f"""Верный ответ\n
        Текущий счет: {self.score}
        Сыграно игр: {Quiz.games_total}
        Общий счет: {Quiz.total_score}"""
        self.score = 0
        self.current_question = 0
        return text


object_quiz = Quiz()    # создание экземпляра класса
