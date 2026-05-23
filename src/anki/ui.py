from __future__ import annotations

from anki.anki import Anki
from typing import Callable


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
        self._is_running: bool = False
        if anki is None:
            raise ValueError("anki не может быть None")
        self._anki_game = anki
        # (Функция, описание, условие_видимости)
        self._command_definition: list[tuple[Callable[..., None], str,
                                             Callable[..., bool]]] = [
            (self.start_game, "Начать игру", lambda: len(self._anki_game) > 0),
            (self.add_words, "Добавить слова", lambda: True),
            (self.train_until_mistake, "Тренировка до первой ошибки",
             lambda: len(self._anki_game) > 0),
            (self.train_until_time_runs_out, "Тренировка на время",
             lambda: len(self._anki_game) > 0),
            (self.show_words, "Показать все слова",
             lambda: len(self._anki_game) > 0),
            (self.find_translation, "Найти перевод",
             lambda: len(self._anki_game) > 0),
            (self.stop, "Выход", lambda: True),
        ]

    def stop(self):
        self._is_running = False

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
        print(
            f"Удачной игры до первой ошибки! Чтобы завершить игру введите: "
            f"{self.STOP_WORD}"
        )
        training_session = self._anki_game.start_zero_mistakes_training()

        while True:
            word = training_session.get_random_word()
            print(f"Переведите слово: {word}")

            translation = input()
            if translation == self.STOP_WORD:
                training_session.end_session()
                user_stat = training_session.get_stat()
                print(
                    f"Итоговый счёт: {user_stat['correct_answers']}, "
                    f"время игры: {user_stat['total_time']:.3f} секунд"
                )
                break

            is_correct = training_session.check_translation(word, translation)
            if is_correct:
                print("Все верно!")
            else:
                user_stat = training_session.get_stat()
                print(
                    f"Неправильно, игра окончена, ваш вариант "
                    f"{repr(translation)} правильный перевод:",
                    self._anki_game.get_translation(word)
                )
                print(
                    f"Итоговый счёт: {user_stat['correct_answers']}, "
                    f"время игры: {user_stat['total_time']:.3f} секунд"
                )
                break

    def train_until_time_runs_out(self) -> None:
        """
        Запускает интерактивную игру на проверку знаний с ограничением
        по времени.

        Использует тренировочную сессию класса Anki
        с ограничением по времени.
        В цикле случайно выбирается слово из словаря, пользователь вводит
        перевод.
        Если перевод верный, игра продолжается со следующим словом.
        Если время истекло, сессия завершается после проверки ответа.
        Пользователь может завершить игру досрочно, введя стоп-слово.

        После завершения игры выводится статистика: количество правильных
        ответов и общее время тренировки.
        """
        print(
            f"Удачной игры на время! Чтобы завершить игру досрочно введите: "
            f"{self.STOP_WORD}"
        )
        while True:
            try:
                time_limit = float(input("Введите время игры в секундах: "))
                if time_limit <= 0:
                    print("Время должно быть положительным числом.")
                    continue
                break
            except ValueError:
                print("Пожалуйста, введите число.")
        training_session = self._anki_game.start_time_limited_training(
            time_limit
        )

        while True:
            word = training_session.get_random_word()
            print(f"Переведите слово: {word}")

            translation = input()
            if translation == self.STOP_WORD:
                training_session.end_session()
                user_stat = training_session.get_stat()
                print(
                    f"Итоговый счёт: {user_stat['correct_answers']}, "
                    f"время игры: {user_stat['total_time']:.3f} секунд"
                )
                break

            is_correct = training_session.check_translation(word, translation)
            if is_correct:
                print("Все верно!")
            else:
                # Ошибка перевода (не время)
                user_stat = training_session.get_stat()
                print(
                    f"Неправильно, ваш вариант {repr(translation)} "
                    f"правильный перевод:",
                    self._anki_game.get_translation(word)
                )
                print(
                    f"Итоговый счёт: {user_stat['correct_answers']}, "
                    f"время игры: {user_stat['total_time']:.3f} секунд"
                )
                break

            # Проверяем, активна ли ещё сессия (возможно, время истекло)
            if not training_session.active:
                user_stat = training_session.get_stat()
                print("Время вышло! Игра окончена.")
                print(
                    f"Итоговый счёт: {user_stat['correct_answers']}, "
                    f"время игры: {user_stat['total_time']:.3f} секунд"
                )
                break

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

    def find_translation(self) -> None:
        """
        Находит перевод слова в словаре игры.

        Запрашивает у пользователя слово для поиска.
        Проверяет наличие слова в словаре игры.
        Выводит перевод, если слово найдено.
        Если слова нет в словаре, сообщает об этом.
        """
        word = input('Введите слово для поиска: ').strip()
        if word in self._anki_game:
            translation = self._anki_game.get_translation(word)
            print(f'Перевод слова "{word}": {translation}')
        else:
            print(f'Слово "{word}" не найдено в словаре.')

    def get_available_commands(self) -> list[tuple[Callable[..., None], str]]:
        """Возвращает доступные команды для меню."""
        commands = []
        for func, description, is_visible in self._command_definition:
            if is_visible():
                commands.append((func, description))
        return commands

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
        self._is_running = True

        while self._is_running:
            menu_choices: list[str] = []
            commands = {}

            for i, (func, description) in enumerate(
                self.get_available_commands(), 1
            ):
                menu_choices.append(f"{i}. {description}")
                commands[str(i)] = func

            # Показываем меню
            print("Меню:\n" + "\n".join(menu_choices))
            choice = input("Выберите пункт: ")

            if choice in commands:
                commands[choice]()
            else:
                print("Неверный пункт меню")
            print()
