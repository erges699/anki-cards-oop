import time


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
    def __init__(self, *, words=None):
        if words is None:
            self._words = {}
        else:
            self._words = self._normalize_dict(words)
        # Начата ли сессия тренировки до первой ошибки.
        self._session_active = False
        # Время начала тренировки.
        self._session_start_time = 0.0
        # Количество правильных ответов.
        self._session_user_score = 0
        self._last_word = None
        # Информация о последней тренировке.
        self.last_session_stats = {
            "correct_answers": 0,
            "total_time": 0.0,
        }

    def __contains__(self, word):
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

    def __str__(self):
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

    def __iter__(self):
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

    def __len__(self):
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

    def start_session(self):
        """Начинает новую тренировочную сессию."""
        if self._session_active:
            raise RuntimeError("Нельзя начать тренировку, если она уже начата")

        self._session_active = True
        self._session_start_time = time.time()
        self._session_user_score = 0

    def end_session(self):
        """Завершает текущую тренировочную сессию."""
        if not self._session_active:
            raise RuntimeError("Нельзя завершить неактивную сессию")

        self.last_session_stats = {
            "correct_answers": self._session_user_score,
            "total_time": time.time() - self._session_start_time
        }

        # Сбрасываем состояние.
        self._session_active = False
        self._session_user_score = 0
        self._session_start_time = 0.0

    @staticmethod
    def normalize_word(word):
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

    def _normalize_dict(self, words):
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

    def add_word(self, word, translation):
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
    def words(self):
        """Докстринг геттер"""
        return {**self._words}

    @words.setter
    def words(self, new_words):
        """Докстринг сеттер"""
        if self._session_active:
            raise ValueError(
                'Нельзя изменять словарь во время активной тренировки.'
            )            
        if new_words is None:
            self._words = {}
        else:
            self._words = self._normalize_dict(new_words)

    def get_random_word(self):
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
        self._last_word = word
        return word

    def check_translation(self, word, translation):
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
        is_correct = self._words[normalized_word] == normalized_translation
        # Логика сессии.
        if self._session_active:
            if is_correct:
                self._session_user_score += 1
            if self._last_word is None:
                # Не должно происходить, но на всякий случай
                self._session_active = False
            elif normalized_word != self.normalize_word(self._last_word):
                self._session_active = False
                raise ValueError(
                    f'Переданное слово "{word}" не совпадает с последним '
                    f'выданным словом "{self._last_word}". '
                    'Тренировка завершена.'
                )
            else:
                self.end_session()
        return is_correct

    def get_translation(self, word):
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
