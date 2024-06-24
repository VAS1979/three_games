"""Модуль содержит класс игры RPG-квест, а также обьект класса,
который инициализируется из модуля bot.py.
"""

from copy import deepcopy
import telebot
from telebot import types

from game.location_dict import locations


class Game:
    '''
    Класс содержит атрибуты и методы
    используемые в игре RPG-квест
    '''
    def __init__(self) -> None:
        self.current_position = 'start'  # текущая позиция
        self.mark = 0  # переменная баллов
        self.items = []  # список умений и баллов
        self.location = deepcopy(locations)  # полная копию словаря locations
        self.state = None  # хранит полученные баллы, статус окончания игры

    def restart_init(self):
        """
        Метод инициализирует экземпляр класса.
        Он необходим для перезапуска игры
        """
        Game.__init__(self)

    def generate_story(self, position):
        '''
        Генерирует весь игровой процесс
        '''
        txt = locations[position]['text']   # текстовое описание локации
        keyboard = telebot.types.InlineKeyboardMarkup()  # создает клавиатуру
        # цикл создания кнопок с ответами
        for i in self.location[position]['next_move']:
            key_txt = i  # сохраняет текст направления в переменную
            # сохраняет название локации
            key_data = locations[position]['next_move'][i]
            # сохраняет в клавиатуру кнопку с текстом и значением callback
            keyboard.add(types.InlineKeyboardButton(text=key_txt,
                                                    callback_data=key_data))
        # цикл обходит items в текущей локации и добавляет значения в кнопки
        for i in self.location[position]['items']:
            key_txt = 'Пройти - ' + i  # добавляет название предмета
            key_data = 'item ' + i  # добавляет к item  предмет
            # сохраняет в клавиатуру кнопку с текстом и значением callback
            keyboard.add(types.InlineKeyboardButton(text=key_txt,
                                                    callback_data=key_data))
        # цикл обходит exchange в текущей локации и добавляет значения в кнопки
        for i in self.location[position]['exchange']:
            # проверяет, что нужное умение есть для обмена
            if i in self.items or (i.startswith('баллы: ') and self.mark
                                   >= int(i.replace('баллы: ', ''))):
                # переменная обьекта для обмена
                change_item = self.location[position]['exchange'][i]
                # генерирует текст обмена
                key_txt = 'Сдать ' + i + ' на ' + change_item
                key_data = 'exchange ' + i  # сохраняет exchange  предмет
                # сохраняет в клавиатуру кнопку с текстом и значением callback
                keyboard.add(types.InlineKeyboardButton(text=key_txt,
                                                        callback_data=key_data))
        return (txt, keyboard)  # возвращает описание локации и клавиатуру

    def handling_item(self, call):
        """
        Метод вызывается из функции item_callback_query
        обрабатывает изменение умений и баллов в item
        """
        # название предмета меняет на item
        item = call.data.replace('item ', '')
        # если предмет начинается на баллы
        if item.startswith('баллы: '):
            # меняет баллы на новое значение
            self.mark += int(item.replace('баллы: ', ''))
        else:   # если предмет начинается не на баллы:
            self.items.append(item)  # добавляет в список items
        # удалаляеn с карты локаций этот предмет (чтобы повторно не взять)
        self.location[self.current_position]['items'].remove(item)

    def handling_exhange(self, call):
        """
        Метод вызывается из функции exchange_callback_query,
        обрабатывает изменение обьектов обмена в exchange
        """
        current_loc = self.location[self.current_position]['exchange']
        item = call.data.replace('exchange ', '')
        self.state = current_loc[item]

        if item.startswith('баллы: '):  # Если item начинается с баллы
            # удаляет баллы
            self.mark -= int(item.replace('баллы: ', ''))
        else:   # Если item начинается не со слова баллы
            self.items.remove(item)    # удаляет item из списка items

        if self.state.startswith('баллы: '):  # если state начинается на баллы
            self.mark += int(self.state.replace('баллы: ', ''))
            # увеличивает баллы (self.mark)
            self.items.append(self.state)  # добавляет state в список items
        # удаляет из exchange item
        self.location[self.current_position]['exchange'].pop(item)


object_game = Game()    # создание экземпляра класса
