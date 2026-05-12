from textwrap import dedent


class TextUI:
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
