"""Модуль бота для Telegram
Этот модуль содержит реализацию Telegram-бота с использованием pyTelegramBotAPI
и обрабатывает все события и обратные вызовы."""

import telebot
from telebot import types

from tokens import TOKEN_BOT

from utils.markups import (keyboard_exit, keyboard_start)
from utils.messages import (START_MESSAGE, HELP_MESSAGE, GO_FIRST, YOU_WIN,
                            YOU_LOST, DRAW, OCCUPIED, COMPLETED, NEXT_MOVE)

from quiz.quiz_game import object_quiz
from tic_tac_toe.tttoe_game import object_tttoe

from game.rpg_game import object_game
from game.location_dict import locations


bot = telebot.TeleBot(TOKEN_BOT)    # создание экземпляра класса


# Главное меню #
################
@bot.message_handler(commands=["start"])
def start_message(message: types.Message):
    """
    Функция стартового меню. Выводит сообщение
    и клавиатуру. Вызывает функцию conversion_start
    """
    print(f"user: {message.chat.id}")   # тестовое сообщение
    bot.send_message(message.chat.id, START_MESSAGE,
                     reply_markup=keyboard_start)


# Раздел помощи #
#################
@bot.message_handler(func=lambda message: message.text == "Помощь" or
                     message.text.startswith("/help"))
def help_message(message):
    """
    Функция убирает клавиатуру главного
    меню и выводит сообщение пользователю
    """
    bot.send_message(message.chat.id, HELP_MESSAGE)


# Игра Викторина #
##################
def quiz_exit(call):
    """
    Функция выхода из игры Викторина. Отправляет сообщение
    с клавиатурой и вызывает функцию command_conversion_quiz
    """
    bot.send_message(call.chat.id, "Выберите действие:",
                     reply_markup=keyboard_exit)
    bot.register_next_step_handler(call, command_conversion_quiz)


def quiz_dialogue(call):
    """
    Функция диалога с пользователем, выводит
    вопрос, клавиатуру с вариантами ответа
    """
    # вызывает метод класса, сохраняет в клавиатуру
    keyb_quiz_dialogue = object_quiz.controls()
    # отправляет текст вопроса и клавиатуру
    bot.send_message(call, object_quiz.question,
                     reply_markup=keyb_quiz_dialogue)


@bot.message_handler(func=lambda message: message.text == "Викторина" or
                     message.text.startswith("/quiz"))
def start_quiz(message):
    """
    Функция запускает игру Викторина, выводит
    вопрос, и клавиатуру с вариантами ответа
    """
    # вызывает метод класса, сохраняет в клавиатуру
    keyb_quiz_dialogue = object_quiz.controls()
    # отправляет текст вопроса и клавиатуру
    bot.send_message(message.chat.id, object_quiz.question,
                     reply_markup=keyb_quiz_dialogue)


@bot.callback_query_handler(func=lambda call: call.data in ['True', 'False'])
def callback_query_quiz(call):
    """
    Функция обрабатывает кнопки InlineKeyboardMarkup.
    Обрабатывает основной цикл игры Викторина.
    """
    if call.data == 'True':  # если ответ правильный
        object_quiz.score += 1  # увеличить текущий счет
    if object_quiz.current_question >= 4:  # если вопрос пятый
        object_quiz.save_game(object_quiz)  # суммируем итоги с прошлыми
        text = object_quiz.finish_results()  # строка итогов
        bot.send_message(call.message.chat.id, text)  # отправка строки итогов
        quiz_exit(call.message)  # вызов клавиатуры окончания игры
    else:  # если номер вопроса меньше пяти
        object_quiz.current_question += 1  # номер текущего вопроса плюс один
        if call.data == 'True':  # если ответ правильный
            # выводит сообщение верный ответ
            bot.send_message(call.message.chat.id, 'Верный ответ')
            # вызов клавиатуры с вопросом и вариантами ответов
            quiz_dialogue(call.message.chat.id)
        else:  # если ответ неверный
            # сообщение неверный ответ
            bot.send_message(call.message.chat.id, 'Неверный ответ')
            # вызов клавиатуры с вопросом и вариантами ответов
            quiz_dialogue(call.message.chat.id)


def command_conversion_quiz(message: types.Message):
    """
    Отлавливает нажатые кнопки Reply клавиатуры
    и вызывает функции по условию
    """
    if message.text == 'Начать заново':
        start_quiz(message)  # вызов начального меню викторины
    elif message.text == 'Выйти в главное меню':
        start_message(message)  # вызов стартового меню


# Игра крестики-нолики #
########################
@bot.message_handler(func=lambda message: message.text == "Крестики-Нолики" or
                     message.text.startswith("/tic_tac_toe"))
def start_tic_tac_toe(message):
    """
    Функция запускает игру крестики-нолики,
    начальная отрисовка поля, первый ход пользователя
    """
    object_tttoe.map = ['*' for i in range(9)]   # инициализация игрового поля
    ttoe_keyboard = object_tttoe.create_keyboard()
    bot.send_message(message.chat.id, GO_FIRST, reply_markup=ttoe_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'no' or call.data in
                            [str(i) for i in range(9)])
def callback_query(call):
    """
    Функция обрабатывает кнопки InlineKeyboardMarkup.
    Обрабатывает основной цикл игры крестики-нолики.
    """
    def edit_message(value):
        """
        Вызывает метод создания клавиатуры игры, изменяет
        отрисовку клеток поля исходя из совершенных ходов
        """
        # формирует сообщения игры и статус окончания
        text = object_tttoe.game_messages(value)
        ttoe_keyboard = object_tttoe.create_keyboard()
        bot.edit_message_text(text, reply_markup=ttoe_keyboard,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    # фильтрует финишные call
    if call.message.text not in [YOU_WIN, YOU_LOST, DRAW]:
        # условие срабатывает, если клетка поля занята
        if (call.data == 'no' and call.message.text != OCCUPIED and
                '*' in object_tttoe.map):
            edit_message(OCCUPIED)   # вызов функции с передачей аргумента
        elif call.data != 'no':  # если клетка свободная
            object_tttoe.map[int(call.data)] = 'X'
            win = object_tttoe.who_win()
            if win:  # если победил игрок или ничья
                if win == YOU_WIN:  # если победил игрок
                    object_tttoe.save_game(1)    # счетчик игрока +1
                elif win == DRAW:  # если ничья
                    object_tttoe.save_game(0)  # счетчик ничьи +1
                edit_message(win)   # вызов функции с передачей аргумента
                # вызов функции с передачей аргумента
                tttoe_exit(call.message)
            else:   # если нет победы игрока или ничьи
                hod_b = object_tttoe.bot_move()
                object_tttoe.map[hod_b] = 'O'
                win = object_tttoe.who_win()
                if win:  # если выиграл ИИ
                    object_tttoe.save_game(2)  # счетчик ИИ +1
                    edit_message(win)   # вызов функции с передачей аргумента
                    # вызов функции с передачей аргумента
                    tttoe_exit(call.message)
                else:   # иначе следующий ход
                    edit_message(NEXT_MOVE)


def tttoe_exit(call):
    """
    Функция выхода из игры крестики-нолики. Отправляет сообщение
    с клавиатурой и вызывает функцию command_conversion_tttoe
    """
    bot.send_message(call.chat.id, "Выберите действие:",
                     reply_markup=keyboard_exit)
    bot.register_next_step_handler(call, command_conversion_tttoe)


def command_conversion_tttoe(message: types.Message):
    """
    Отлавливает нажатые кнопки Reply клавиатуры
    и вызывает функции по условию
    """
    if message.text == 'Начать заново':
        start_tic_tac_toe(message)  # вызов начального меню викторины
    elif message.text == 'Выйти в главное меню':
        start_message(message)  # вызов стартового меню


# Игра квест-рпг #
##################
@bot.message_handler(func=lambda message: message.text == "RPG игра" or
                     message.text.startswith("/game"))
def start_game(message):
    """
    Функция запускает игру 'RPG игра', генерирует
    начальный текст, клавиатуру, и отправляет сообщение
    с клавиатурой
    """
    object_game.restart_init()  # инициализация экземпляра класса object_game
    # генерация начального текста, клавиатуры и сохранение их переменные
    txt, keyboard = object_game.generate_story(object_game.current_position)
    bot.send_message(message.chat.id, txt, reply_markup=keyboard)


# Обрабатывает новый callback, если call.data начинается с locations
@bot.callback_query_handler(func=lambda call: call.data in locations)
def locations_callback_query(call):
    """
    Функция вызывается при смене локации игрока, обрабатывает
    кнопки InlineKeyboardMarkup, генерирует текст, клавиатуру,
    и отправляет сообщение с клавиатурой
    """
    object_game.current_position = call.data    # меняет текущую позицию игрока
    # генерация начального текста, клавиатуры и сохранение их переменные
    txt, keyboard = object_game.generate_story(object_game.current_position)
    if object_game.current_position == 'loss':  # если игрок проиграл
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)
        game_exit(call.message)  # вызов меню
    else:   # если игра не проиграна
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)


# Обрабатывает новый callback, если call.data начинается с 'item'
@bot.callback_query_handler(func=lambda call: call.data.startswith('item '))
def item_callback_query(call):
    """
    Функция вызывается при изменении параметра item, обрабатывает
    кнопки InlineKeyboardMarkup, генерирует текст, клавиатуру,
    и отправляет сообщение с клавиатурой
    """
    #  вызов метода класса с передачей аргумента call
    object_game.handling_item(call)
    # сообщение об удачном действии
    bot.send_message(call.message.chat.id, 'Готово✔')
    txt, keyboard = object_game.generate_story(object_game.current_position)
    bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)


# Обрабатывает новый callback, если call.data начинается с 'exchange'
@bot.callback_query_handler(func=lambda call:
                            call.data.startswith('exchange '))
def exchange_callback_query(call):
    """
    Функция вызывается при изменении параметра exchange, обрабатывает
    кнопки InlineKeyboardMarkup, генерирует текст, клавиатуру,
    и отправляет сообщение с клавиатурой
    """
    #  вызов метода класса с передачей аргумента call
    object_game.handling_exhange(call)
    if object_game.state == 'закрытие модуля':    # если обменялись на выход
        # выводит сообщение о победе
        bot.send_message(call.message.chat.id, COMPLETED)
        game_exit(call.message)  # вызов меню
    else:  # иначе генерирует следующий ход
        txt, keyboard = object_game.generate_story(object_game.current_position)
        bot.send_message(call.message.chat.id, txt, reply_markup=keyboard)


def game_exit(call):
    """
    Функция выхода из игры крестики-нолики. Отправляет сообщение
    с клавиатурой и вызывает функцию command_conversion_game
    """
    bot.send_message(call.chat.id, "Выберите действие:",
                     reply_markup=keyboard_exit)
    bot.register_next_step_handler(call, command_conversion_game)


def command_conversion_game(message: types.Message):
    """
    Отлавливает нажатые кнопки Reply клавиатуры
    и вызывает функции по условию
    """
    if message.text == 'Начать заново':
        start_game(message)  # вызов начального меню викторины
    elif message.text == 'Выйти в главное меню':
        start_message(message)  # вызов стартового меню


if __name__ == '__main__':
    print('bot starting...')    # Тестовое сообщение
    bot.polling(none_stop=True)  # Запуск бесконечного цикла опроса сервера
