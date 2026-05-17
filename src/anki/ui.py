import textwrap


class TextUI:
    """пользовательский интерфейс"""
    MENU = textwrap.dedent("""\
        Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        """).strip()

    def __init__(self):
        pass
