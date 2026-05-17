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
            self._words = normalized_words

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

    def get_words(self):
        """
        Возвращает копию словаря всех слов и переводов.

        Возвращается глубокая копия, чтобы предотвратить случайное
        изменение внутреннего состояния объекта.

        Returns
        -------
        dict
            Копия словаря, где ключи — нормализованные слова,
            значения — нормализованные переводы.

        Examples
        --------
        >>> anki = Anki(words={"Cat": "Кошка"})
        >>> words = anki.get_words()
        >>> words
        {'cat': 'кошка'}
        >>> words["dog"] = "собака"  # не влияет на внутренний словарь
        >>> anki.get_words()
        {'cat': 'кошка'}
        """
        import copy
        return copy.deepcopy(self._words)
