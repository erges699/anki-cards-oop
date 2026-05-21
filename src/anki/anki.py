import time
from typing import Dict, Optional, Iterator, Tuple


class TrainingSession:
    """
    Базовый класс тренировочной сессии.

    Обеспечивает общую логику для различных типов тренировок:
    - отслеживание времени начала и окончания сессии,
    - подсчёт правильных ответов,
    - выдача случайных слов и проверка переводов.

    Parameters
    ----------
    anki : Anki
        Экземпляр игры Anki, с которым связана сессия.

    Attributes
    ----------
    active : bool
        Флаг активности сессии. True, пока сессия не завершена.
    _anki : Anki
        Ссылка на экземпляр игры Anki.
    _start_time : float
        Время начала сессии (в секундах с эпохи).
    _end_time : float
        Время окончания сессии (в секундах с эпохи).
    _user_score : int
        Количество правильных ответов в сессии.
    _last_word : str | None
        Последнее выданное слово.
    """

    def __init__(self, anki: "Anki") -> None:
        self.active: bool = True

        self._anki: "Anki" = anki
        self._start_time: float = time.time()
        self._end_time: float = self._start_time
        self._user_score: int = 0
        self._last_word: str | None = None

    def get_random_word(self) -> str:
        """
        Возвращает случайное слово из словаря игры.

        Returns
        -------
        str
            Случайное слово.

        Raises
        ------
        ValueError
            Если сессия не активна.
        """
        if not self.active:
            raise ValueError("Сессия не активна")
        word = self._anki.get_random_word()
        self._last_word = word
        return word

    def check_translation(self, word: str, translation: str) -> bool:
        """
        Проверяет, является ли перевод правильным.

        Parameters
        ----------
        word : str
            Слово, для которого нужно проверить перевод.
        translation : str
            Предложенный перевод.

        Returns
        -------
        bool
            True, если перевод правильный, иначе False.

        Raises
        ------
        ValueError
            Если сессия не активна или слово не соответствует последнему
            выданному.
        """
        if not self.active:
            raise ValueError("Сессия не активна")
        if self._last_word is None:
            raise ValueError(
                "Нельзя проверить перевод, пока не получено новое слово"
            )
        normalized_word = self._anki.normalize_word(word)
        if normalized_word != self._last_word:
            raise ValueError(
                "Можно проверять перевод только последнего выданного слова"
            )
        # Сбрасываем последнее слово, чтобы нельзя было проверить повторно
        self._last_word = None
        return self._anki.check_translation(word, translation)

    def end_session(self):
        """
        Завершает тренировочную сессию.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Если сессия уже завершена.
        """
        if not self.active:
            raise ValueError("Сессия уже завершена")
        self.active = False
        self._end_time = time.time()
        return self._anki.end_session()

    def get_stat(self):
        """
        Возвращает статистику сессии.

        Returns
        -------
        dict
            Словарь с ключами:
            - "correct_answers": количество правильных ответов,
            - "total_time": общее время сессии в секундах.
        """
        if self.active:
            total_time = time.time() - self._start_time
        else:
            total_time = self._end_time - self._start_time

        return {
            "correct_answers": self._user_score,
            "total_time":  total_time
        }


class ZeroMistakesTraining(TrainingSession):

    def check_translation(self, word: str, translation: str) -> bool:
        is_correct = super().check_translation(word, translation)

        if is_correct:
            self._user_score += 1
        else:
            self.end_session()

        return is_correct


class TimeLimitedTraining(TrainingSession):
    """
    Тренировочная сессия с ограничением по времени.

    Parameters
    ----------
    anki : Anki
        Экземпляр игры Anki, с которым связана сессия.
    time_limit : float, optional
        Лимит времени в секундах (по умолчанию 60.0).

    Attributes
    ----------
    _time_limit : float
        Максимальная продолжительность сессии в секундах.
    """

    def __init__(self, anki: "Anki", time_limit: float = 60.0) -> None:
        super().__init__(anki)
        self._time_limit: float = time_limit

    def check_translation(self, word: str, translation: str) -> bool:
        """
        Проверяет перевод слова с учётом ограничения по времени.

        Перед проверкой вычисляется, не истекло ли время сессии.
        Если время истекло, сессия завершается после проверки перевода.

        Parameters
        ----------
        word : str
            Слово, для которого нужно проверить перевод.
        translation : str
            Предложенный перевод.

        Returns
        -------
        bool
            True, если перевод правильный, иначе False.

        Raises
        ------
        ValueError
            Если сессия не активна.
        """
        # Проверяем, не истекло ли время до проверки перевода
        current_time = time.time()
        time_expired = (current_time - self._start_time) >= self._time_limit

        # Выполняем проверку перевода
        # (базовый метод проверит активность сессии)
        is_correct = super().check_translation(word, translation)

        if is_correct:
            self._user_score += 1

        # Если время истекло, завершаем сессию
        if time_expired:
            self.end_session()

        return is_correct


class Anki:
    """
    Основной класс для управления словарём слов и их переводов.

    Класс предоставляет методы для добавления, нормализации и получения слов.
    Все слова хранятся в нормализованном виде (нижний регистр, без пробелов
    по краям).

    Parameters
    ----------
    words : dict, optional
        Начальный словарь слов и переводов. Ключи и значения должны быть
        строками. Если не указан, используется пустой словарь.

    Raises
    ------
    ValueError
        Если `words` не является словарём.
        Если ключи или значения словаря не являются строками.

    Examples
    --------
    >>> anki = Anki()
    >>> anki.add_word("Hello", "Привет")
    >>> anki.get_words()
    {'hello': 'привет'}

    >>> anki = Anki(words={"Apple": "Яблоко", "Dog": "Собака"})
    >>> anki.get_words()
    {'apple': 'яблоко', 'dog': 'собака'}
    """
    def __init__(self, *, words: Optional[Dict[str, str]] = None) -> None:
        if words is None:
            self._words: Dict[str, str] = {}
        else:
            self._words = self._normalize_dict(words)
        # Начата ли сессия тренировки до первой ошибки.
        self._session_active: bool = False

    def __contains__(self, word: str) -> bool:
        """
        Проверяет, содержится ли слово в словаре.

        Слово нормализуется (приводится к нижнему регистру и обрезаются
        пробелы) перед проверкой. Это позволяет искать слова без учёта
        регистра и лишних пробелов.

        Parameters
        ----------
        word : str
            Слово для проверки наличия в словаре.

        Returns
        -------
        bool
            True, если нормализованное слово присутствует в словаре,
            иначе False.

        Raises
        ------
        ValueError
            Если `word` не является строкой.

        Examples
        --------
        >>> anki = Anki(words={"apple": "яблоко"})
        >>> "apple" in anki
        True
        >>> "Apple" in anki
        True
        >>> "banana" in anki
        False
        """
        if not isinstance(word, str):
            raise ValueError('Параметр `word` должен быть строкой')
        normalized_word = self.normalize_word(word)
        return normalized_word in self._words

    def __str__(self) -> str:
        """
        Возвращает неформальное строковое представление объекта Anki.

        Представление включает количество слов в словаре и предназначено
        для удобного чтения человеком.

        Returns
        -------
        str
            Строка в формате "Anki словарь с X слов(ами)".

        Notes
        -----
        Это представление используется функциями `str()`, `print()` и при
        неявном преобразовании в строку в пользовательском контексте.
        Для получения однозначного представления, пригодного для отладки,
        используйте `repr()`.

        Examples
        --------
        >>> anki = Anki()
        >>> str(anki)
        'Anki словарь с 0 слов(ами)'
        >>> anki.add_word("hello", "привет")
        >>> str(anki)
        'Anki словарь с 1 слов(ами)'
        """
        count = len(self._words)
        return f'Anki словарь с {count} слов(ами)'

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """
        Возвращает итератор по парам (слово, перевод).

        Returns
        -------
        iterator
            Итератор, который yields кортежи (слово, перевод) для каждого
            элемента словаря.

        Notes
        -----
        Порядок итерации соответствует порядку встроенного словаря Python
        (порядок вставки, начиная с Python 3.7).
        Слова и переводы возвращаются в нормализованном виде.

        Examples
        --------
        >>> anki = Anki(words={"apple": "яблоко", "dog": "собака"})
        >>> for word, translation in anki:
        ...     print(word, translation)
        apple яблоко
        dog собака
        """
        return iter(self._words.items())

    def __len__(self) -> int:
        """
        Возвращает количество слов в словаре.

        Returns
        -------
        int
            Количество пар слово-перевод в словаре.

        Examples
        --------
        >>> anki = Anki()
        >>> len(anki)
        0
        >>> anki.add_word("hello", "привет")
        >>> len(anki)
        1
        """
        return len(self._words)

    def end_session(self) -> None:
        """
        Завершает текущую тренировочную сессию.

        Raises
        ------
        RuntimeError
            Если сессия не активна.
        """
        if not self._session_active:
            raise RuntimeError("Нельзя завершить неактивную сессию")
        self._session_active = False

    def start_zero_mistakes_training(self) -> ZeroMistakesTraining:
        if self._session_active:
            raise RuntimeError("Нельзя начать тренировку, если она уже начата")
        self._session_active = True

        return ZeroMistakesTraining(self)

    def start_time_limited_training(
        self, time_limit: float = 60.0
    ) -> TimeLimitedTraining:
        """
        Начинает тренировочную сессию с ограничением по времени.

        Parameters
        ----------
        time_limit : float, optional
            Лимит времени в секундах (по умолчанию 60.0).

        Returns
        -------
        TimeLimitedTraining
            Экземпляр сессии с ограничением по времени.

        Raises
        ------
        RuntimeError
            Если сессия уже активна.
        """
        if self._session_active:
            raise RuntimeError("Нельзя начать тренировку, если она уже начата")
        self._session_active = True

        return TimeLimitedTraining(self, time_limit)

    @staticmethod
    def normalize_word(word: str) -> str:
        """
        Нормализует слово: приводит к нижнему регистру и удаляет пробелы
        по краям.

        Parameters
        ----------
        word : str
            Слово для нормализации.

        Returns
        -------
        str
            Нормализованное слово.

        Raises
        ------
        ValueError
            Если `word` не является строкой.

        Examples
        --------
        >>> Anki.normalize_word("  Hello ")
        'hello'
        >>> Anki.normalize_word("WORLD")
        'world'
        """
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        return word.lower().strip()

    def _normalize_dict(self, words: Dict[str, str]) -> Dict[str, str]:
        """Докстринг"""
        if not isinstance(words, dict):
            raise ValueError(
                'Значение параметра "words" должно быть словарём'
            )
        normalized_words = {}
        for word, translation in words.items():
            if not isinstance(word, str):
                raise ValueError('Ключ словаря должен быть строкой')

            if not isinstance(translation, str):
                raise ValueError('Значение словаря должно быть строкой')

            normalize_word = self.normalize_word(word)
            normalize_translation = self.normalize_word(translation)
            normalized_words[normalize_word] = normalize_translation
        return normalized_words

    def add_word(self, word: str, translation: str) -> None:
        """
        Добавляет слово и его перевод в словарь.

        Оба параметра нормализуются перед сохранением. Если слово уже
        присутствует в словаре, его перевод будет перезаписан.

        Parameters
        ----------
        word : str
            Слово для добавления.
        translation : str
            Перевод слова.

        Raises
        ------
        ValueError
            Если `word` или `translation` не являются строками.

        Examples
        --------
        >>> anki = Anki()
        >>> anki.add_word("Hello", "Привет")
        >>> anki.get_words()
        {'hello': 'привет'}
        """
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        if not isinstance(translation, str):
            raise ValueError('Перевод должен быть строкой')
        normalize_word = self.normalize_word(word)
        normalize_translation = self.normalize_word(translation)
        self._words[normalize_word] = normalize_translation

    @property
    def words(self) -> Dict[str, str]:
        """Докстринг геттер"""
        return {**self._words}

    @words.setter
    def words(self, new_words: Optional[Dict[str, str]]) -> None:
        """
        Устанавливает новый словарь слов.

        Заменяет текущий словарь полностью. Все слова нормализуются.
        Если передан `None`, устанавливается пустой словарь.

        Parameters
        ----------
        new_words : dict or None
            Новый словарь слово-перевод.

        Raises
        ------
        ValueError
            Если при активной тренировочной сессии предпринята попытка
            изменить словарь.
        """
        if self._session_active:
            raise ValueError(
                'Нельзя изменять словарь во время активной тренировки.'
            )
        if new_words is None:
            self._words = {}
        else:
            self._words = self._normalize_dict(new_words)

    def get_random_word(self) -> str:
        """
        Возвращает случайное слово из словаря.

        Returns
        -------
        str
            Случайное слово.

        Raises
        ------
        ValueError
            Если словарь пуст.

        Examples
        --------
        >>> anki = Anki(words={"Cat": "Кошка"})
        >>> word = anki.get_random_word()
        >>> word in anki
        True
        """
        if not self._words:
            raise ValueError('Словарь пуст')
        import random
        word = random.choice(list(self._words.keys()))
        return word

    def check_translation(self, word: str, translation: str) -> bool:
        """
        Проверяет, является ли перевод правильным.

        Parameters
        ----------
        word : str
            Слово, для которого нужно проверить перевод.
        translation : str
            Перевод слова.

        Returns
        -------
        bool
            True, если перевод правильный, иначе False.

        Raises
        ------
        ValueError
            Если `word` или `translation` не являются строками.
            Если слово отсутствует в словаре.

        Examples
        --------
        >>> anki = Anki(words={"Cat": "Кошка"})
        >>> anki.check_translation("Cat", "Кошка")
        True
        >>> anki.check_translation("Cat", "Собака")
        False
        """
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        if not isinstance(translation, str):
            raise ValueError('Перевод должен быть строкой')
        normalized_word = self.normalize_word(word)
        if normalized_word not in self._words:
            raise ValueError('Слово отсутствует в словаре')
        normalized_translation = self.normalize_word(translation)
        return self._words[normalized_word] == normalized_translation

    def get_translation(self, word: str) -> str:
        """
        Возвращает перевод слова.

        Parameters
        ----------
        word : str
            Слово, для которого нужно получить перевод.

        Returns
        -------
        str
            Перевод слова.

        Raises
        ------
        ValueError
            Если `word` не является строкой.
            Если слово отсутствует в словаре.

        Examples
        --------
        >>> anki = Anki(words={"Cat": "Кошка"})
        >>> anki.get_translation("Cat")
        'Кошка'
        """
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        normalized_word = self.normalize_word(word)
        if normalized_word not in self._words:
            raise ValueError('Слово отсутствует в словаре')
        return self._words[normalized_word]
