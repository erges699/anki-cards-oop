from __future__ import annotations

import textwrap
from typing import Optional
from anki.anki import Anki


class TextUI:
    """
    Текстовый пользовательский интерфейс для взаимодействия с игрой Anki.

    Класс предоставляет меню для выполнения основных операций: начало игры,
    добавление слов, вывод всех слов и выход. Взаимодействие происходит через
    консоль.

    Parameters
    ----------
    anki : Anki
        Экземпляр класса Anki, с которым будет работать интерфейс.

    Raises
    ------
    ValueError
        Если переданный аргумент `anki` равен None.

    Attributes
    ----------
    STOP_WORD : str
        Ключевое слово для завершения ввода в интерактивных режимах.
    MENU : str
        Текст главного меню с доступными опциями.

    Examples
    --------
    >>> from anki import Anki
    >>> anki = Anki()
    >>> ui = TextUI(anki)
    >>> # Запуск основного цикла
    >>> # ui.main_loop()
    """
    STOP_WORD = "стоп"

    MENU = textwrap.dedent("""\
        Меню:
        1. Начать игру
        2. Добавить слова
        3. Вывод всех слов
        4. Тренировка до первой ошибки
        5. Выход
        """).strip()

    def __init__(self, anki: 'Anki') -> None:
        """
        Инициализирует текстовый интерфейс с экземпляром игры Anki.

        Parameters
        ----------
        anki : Anki
            Экземпляр класса Anki, с которым будет работать интерфейс.

        Raises
        ------
        ValueError
            Если переданный аргумент `anki` равен None.
        """
        if anki is None:
            raise ValueError("anki не может быть None")
        self._anki_game = anki

    def start_game(self) -> None:
        """
        Запускает интерактивную игру на проверку знаний.

        В цикле случайно выбирается слово из словаря, пользователь вводит
        перевод. Если перевод верный, выводится подтверждение, иначе
        показывается правильный ответ. Игра продолжается до ввода
        стоп-слова (значение `STOP_WORD`) или пока словарь не станет пустым.

        Raises
        ------
        ValueError
            Косвенно, если словарь пуст и вызывается `get_random_word()`.

        Notes
        -----
        Для завершения игры введите стоп-слово «стоп».
        """
        print(f'Для завершения игры введите "{self.STOP_WORD}"')
        while True:
            try:
                word = self._anki_game.get_random_word()
            except ValueError:
                print('Словарь пуст. Добавьте слова для начала игры.')
                break
            print(f"\nСлово: {word}")
            user_input = input("Введите перевод: ").strip()
            if user_input.lower() == self.STOP_WORD:
                break
            if self._anki_game.check_translation(word, user_input):
                print('Правильно')
            else:
                correct = self._anki_game.get_translation(word)
                print(f'Неправильно. Правильный перевод: {correct}')

    def train_until_mistake(self) -> None:
        """
        Запускает интерактивную игру на проверку знаний до первой ошибки.

        Использует тренировочную сессию класса Anki (`start_session`).
        В цикле случайно выбирается слово из словаря, пользователь вводит
        перевод. Если перевод верный, игра продолжается со следующим словом.
        Если перевод неверный или пользователь вводит стоп-слово, сессия
        завершается.

        При активной сессии действует защита от накрутки: нельзя проверить
        перевод слова, которое не было только что выдано, или повторно
        проверить то же слово.

        После завершения игры выводится статистика: количество правильных
        ответов и общее время тренировки.

        Raises
        ------
        ValueError
            Косвенно, если словарь пуст и вызывается `get_random_word()`.
        """
        print(f'Для завершения игры введите "{self.STOP_WORD}"')
        self._anki_game.start_session()

        try:
            while True:
                try:
                    word = self._anki_game.get_random_word()
                except ValueError:
                    print('Словарь пуст. Добавьте слова для начала игры.')
                    break

                print(f'\nСлово: {word}')
                user_input = input('Введите перевод: ').strip()

                if user_input.lower() == self.STOP_WORD:
                    # Пользователь решил завершить тренировку
                    self._anki_game.end_session()
                    break

                try:
                    is_correct = self._anki_game.check_translation(
                        word, user_input
                    )
                except ValueError as e:
                    # Исключение при несовпадении слова (защита от накруток)
                    print(f'Ошибка: {e}')
                    # Сессия уже завершена в check_translation
                    break

                if is_correct:
                    print('Правильно')
                    # Сессия продолжается
                else:
                    correct_translation = self._anki_game.get_translation(word)
                    print('Неправильно. '
                          f'Правильный перевод: {correct_translation}')
                    # Сессия уже завершена в check_translation
                    break
        finally:
            # Убедимся, что сессия завершена (на случай непредвиденных ошибок)
            if self._anki_game._session_active:
                self._anki_game.end_session()

        # Вывод статистики
        stats = self._anki_game.last_session_stats
        print('\nТренировка завершена.')
        print(f'Правильных ответов: {stats["correct_answers"]}')
        print(f'Общее время: {stats["total_time"]:.2f} секунд')

    def add_words(self) -> None:
        """
        Режим добавления новых слов в словарь.

        В цикле запрашивает у пользователя слово и его перевод.
        Добавление происходит через метод `add_word` экземпляра Anki.
        При некорректном вводе (не строки) выводится сообщение об ошибке.
        Цикл прерывается вводом стоп-слова (значение `STOP_WORD`).

        Raises
        ------
        ValueError
            Косвенно, если `add_word` вызывает исключение (например,
            нестроковые аргументы).

        Notes
        -----
        Для завершения ввода введите стоп-слово «стоп».
        """
        print(f'Для завершения ввода введите "{self.STOP_WORD}"')
        while True:
            word = input('Введите слово: ').strip()
            if word.lower() == self.STOP_WORD:
                break
            translation = input('Введите перевод: ').strip()
            try:
                self._anki_game.add_word(word, translation)
                print(f'Слово "{word}" с переводом "{translation}" добавлено.')
            except ValueError as e:
                print(f'Ошибка: {e}')

    def show_words(self) -> None:
        """
        Выводит все слова и их переводы из словаря.

        Если словарь пуст, выводится только заголовок «Словарь:».
        """
        print(f'Словарь: {len(self._anki_game)}')

        for word, translation in self._anki_game:
            print(f'{word} - {translation}')

    def main_loop(self) -> None:
        """
        Основной цикл интерфейса, отображающий меню и обрабатывающий выбор.

        Бесконечно выводит меню и ожидает ввод номера команды.
        В зависимости от вызова выполняет соответствующий метод:
        - 1: `start_game`
        - 2: `add_words`
        - 3: `show_words`
        - 4: заглушка (функциональность не реализована)
        - 5: выход из программы

        Notes
        -----
        Меню содержит пять пунктов, описанных в атрибуте `MENU`.
        """
        while True:
            print(self.MENU)
            choice = input("> ").strip()

            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.add_words()
            elif choice == "3":
                self.show_words()
            elif choice == "4":
                # print("\nДанная функциональность ещё не реализована")
                self.train_until_mistake()
            elif choice == "5":
                print("\nВыход из программы.")
                break
            else:
                print("\nНеверный выбор. Пожалуйста, введите число от 1 до 5.")
