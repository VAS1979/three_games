""" Модуль содержит словарь, используемый для игры RPG игра"""

locations = {
    'start': {'text': 'Вы на третьем модуле Кода будущего от института \
  "Синергия", ваша задача - успешно закрыть модуль',
              'items': [],
              'next_move': {'Запустить браузер': 'browser'},
              'exchange': {}},

    'browser': {'text': 'Вам поступило письмо от компании SuperPuperPro с \
  предложением бросить учебу в Синергии и перейти к ним, за это\
  вам обещают трудоустройство сразу после окончания курса. Вы \
  стоите перед выбором, продолжить учебу, или перейти к \
  конкурентам',
                'items': [],
                'next_move': {'Уйти к конкурентам': 'loss',
                              'Пройти итоговый тест': 'testing',
                              'Пройти обучение в модуле': 'education'},
                'exchange': {}},

    'loss': {'text': 'SuperPuperPro оказались инфоцыганями, без аккредитации \
  и официальной регистрации, к тому же вы оплатили начальный \
  взнос, деньги вам не вернули. Вы кусаете локти, но назад пути \
  нет, приходит осознание что это провал...',
             'items': [],
             'next_move': {},
             'exchange': {}},

    'testing': {'text': 'Вы перешли в раздел итогового тестирования, \
  готовы-ли вы, вот в чем вопрос🤔...',
                'items': [],
                'next_move': {'Вернуться назад': 'browser'},
                'exchange': {'теорию': 'баллы: 75'}},

    'education': {'text': 'Вы в разделе учебные материалы. Блин, как много \
  всего нужно выучить, с тоской подумали вы, и чего я \
  отказался от обучения в SuperPuperPro? 😞',
                  'items': [],
                  'next_move': {'Вернуться назад': 'browser',
                                'Перейти к практике': 'practice',
                                'Почитать конспекты модуля': 'explore'},
                  'exchange': {}},

    'explore': {'text': 'Перед вами конспекты тем модуля, как много тут \
  информации, учить или забить на это, вот в чем вопрос...',
                'items': ['теорию'],
                'next_move': {'Вернуться в модуль обучения': 'education'},
                'exchange': {}},

    'practice': {'text': 'Практические задания интересные, но легкими их не \
  назовешь.',
                 'items': ['баллы: 25'],
                 'next_move': {'Продолжить выполнять ДЗ': 'learning',
                               'Вернуться в модуль обучения': 'education'},
                 'exchange': {}},

    'learning': {'text': 'Ты продолжаешь тупить за экраном и жмакать кнопки, \
  периодически возникает мысль, все-ли я выучил? Может стоит \
  вернуться и повторить метериал?',
                 'items': [],
                 'next_move': {'Завершить модуль': 'finish',
                               'Продолжить зубрить': 'practice'},
                 'exchange': {}},

    'finish': {'text': 'Ты знаешь что готов, но иногда проскакивают сомнения. \
  Не повторить - ли конспекты модуля?',
               'items': [],
               'next_move': {'Вернуться к повторению темы': 'learning'},
               'exchange': {'баллы: 100': 'закрытие модуля'}}
}
