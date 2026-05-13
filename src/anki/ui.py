from textwrap import dedent


class TextUI:
    STOP_WORD = 'СТОП'
    MENU = dedent("""
        ========================================
                    КАРТЫ ANKI
        ========================================
        Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        """).strip()

    def __init__(self, anki_game):
        """
        Инициализатор класса TextUI.

        Параметры:
            anki_game (Anki): экземпляр класса Anki.
        """
        if anki_game is None:
            raise ValueError('Аргумент anki_game обязателен')
        self._anki_game = anki_game

    def start_game(self):
        """
        Запускает обычную игру (тренировку) по словам.
        """
        # print(f'\nИгра началась! Для завершения введите "{self.STOP_WORD}".')
        print('Игра началась! Для завершения введите СТОП.')
        while True:
            try:
                word = self._anki_game.get_random_word()
            except ValueError:
                print('Словарь пуст. Добавьте слова через меню.')
                break

            print(f'\nСлово: {word}')
            user_answer = input('Введите перевод: ').lower().strip()

            if user_answer.upper() == self.STOP_WORD:
                print('Игра завершена.')
                break
            if self._anki_game.check_translation(word, user_answer):
                print('Верно!')
            else:
                print('Неверно. Правильный ответ: '
                      f'{self._anki_game.get_translation(word)}')

    def add_words(self):
        """
        Добавляет слова в словарь.
        """
        print('Для завершения ввода введите служебное слово — СТОП.')
        while True:
            word = input('Введите слово: ').lower().strip()
            if word.upper() == self.STOP_WORD:
                break
            translation = input('Введите перевод: ').lower().strip()
            self._anki_game.add_word(word, translation)

    def show_words(self):
        """
        Выводит все слова из словаря.
        """
        words = self._anki_game.get_words()
        if not words:
            print("\nСловарь пуст.")
            return

        print("\nСловарь:")
        for word, translation in words.items():
            print(f"{word} - {translation}")

    def main_loop(self):
        """
        Запускает главный цикл программы.
        """
        while True:
            print(self.MENU)
            menu_choice = input('Пункт меню: ')

            if menu_choice == '1':
                self.start_game()
            elif menu_choice == '2':
                self.add_words()
            elif menu_choice == '3':
                print('\nДанная функциональность ещё не реализована')
                # self.train_until_mistake()
            elif menu_choice == '4':
                self.show_words()
            elif menu_choice == '5':
                print('\nВыход')
                break
            else:
                print('Неизвестный пункт меню')        
