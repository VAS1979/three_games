""" Модуль содержит клавиатуры и кнопки, используемые в боте"""

from telebot import types


# кнопки стартового меню
button_quiz = types.KeyboardButton(text='Викторина')
button_tic_tac_toe = types.KeyboardButton(text='Крестики-Нолики')
button_rpg = types.KeyboardButton(text='RPG игра')
button_help = types.KeyboardButton(text='Помощь')

# кнопки меню выхода из игры
button_restart = types.KeyboardButton(text='Начать заново')
button_exit = types.KeyboardButton(text='Выйти в главное меню')

'''клавиатуры'''
# клавитура стартового меню
keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4,
                                           one_time_keyboard=True)
keyboard_start.add(button_quiz, button_tic_tac_toe,
                   button_rpg).row(button_help)

# клавиатура меню выхода из игры или перезапуска игры
keyboard_exit = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                          one_time_keyboard=True)
keyboard_exit.add(button_restart, button_exit)
