import copy
import random

from typing import Dict


class Anki:
    """Для класса `Anki` разработан докстринг"""
    app_version = '0.0.1'

    def __init__(self, *, words=None):
        if words is None:
            self._words = {}
        else:
            self._words = self._normalize_dict(words)
        self._last_word = None
        self._training_active = False

    def __iter__(self):
        """Возвращает объект типа dict_items"""
        return iter(self._words.items())

    def __len__(self):
        """Вычисляет количество слов в игре (вызовом len(anki))"""
        return len(self._words)

    def __str__(self):
        """
        Возвращает строковое представление объекта Anki.

        Возвращает:
            str: Информация о количестве слов в словаре.
        """
        count = len(self._words)
        return f"Anki словарь с {count} слов(ами)"

    def __contains__(self, word):
        """
        Проверяет, содержится ли слово в словаре.

        Параметры:
            word (str): Слово для проверки.

        Возвращает:
            bool: True если слово присутствует в словаре (после нормализации),
                  False иначе.

        Исключения:
            ValueError: Если переданный аргумент не является строкой.
        """
        if not isinstance(word, str):
            raise ValueError('Параметр `word` должен быть строкой')
        normalized_word = self.normalize_word(word)
        return normalized_word in self._words

    @staticmethod
    def normalize_word(word: str) -> str:
        """
        Нормализует слово: удаляет пробелы по краям и приводит к
        нижнему регистру.

        Параметры:
            word (str): Слово для нормализации.

        Возвращает:
            str: Нормализованная строка.

        Исключения:
            ValueError: Если переданный аргумент не является строкой.
        """
        if not isinstance(word, str):
            raise ValueError(f'Слово {word} должно быть строкой')
        return word.strip().lower()

    def _normalize_dict(self, words: dict) -> dict:
        """
        Принимает словарь и возвращает нормализованный словарь.
        Валидирует, что keys и values являются строками, нормализует их.

        Параметры:
            words (dict): Словарь для нормализации.

        Возвращает:
            dict: Нормализованный словарь.

        Исключения:
            ValueError: Если words не является словарём или содержит
                       нестроковые значения.
        """
        if not isinstance(words, dict):
            raise ValueError('Значение параметра "words" должно быть словарём')
        normalized_words = {}
        for word, translation in words.items():
            if not isinstance(word, str):
                raise ValueError(f'Значение {word} должно быть строкой')
            if not isinstance(translation, str):
                raise ValueError(f'Значение {translation} должно быть строкой')

            normalized_key = self.normalize_word(word)
            normalized_value = self.normalize_word(translation)
            normalized_words[normalized_key] = normalized_value
        return normalized_words

    @property
    def words(self) -> Dict[str, str]:
        """
        Возвращает копию словаря слов.

        Возвращает:
            dict: Копия словаря вида {"слово": "перевод"}.
        """
        return copy.deepcopy(self._words)

    @words.setter
    def words(self, new_words: dict) -> None:
        """
        Устанавливает новый словарь слов, выполняя валидацию и нормализацию.

        Параметры:
            new_words (dict): Новый словарь для установки.

        Исключения:
            ValueError: Если new_words не является словарём или содержит
                       нестроковые значения, или если попытка изменить словарь
                       во время активной тренировки.
        """
        if self._training_active:
            raise ValueError(
                'Нельзя изменять словарь во время активной тренировки.'
            )
        if new_words is None:
            self._words = {}
        else:
            self._words = self._normalize_dict(new_words)

    def add_word(self, word, translation):
        """
        Добавляет слово и его перевод в словарь words.

        Параметры:
            word (str): Слово на иностранном языке.
            translation (str): Перевод слова.

        Исключения:
            ValueError: Если word или translation не являются строками.
        """
        if not isinstance(word, str):
            raise ValueError('Параметр `word` должен быть строкой')
        if not isinstance(translation, str):
            raise ValueError('Параметр `translation` должен быть строкой')

        normalized_word = self.normalize_word(word)
        normalized_translation = self.normalize_word(translation)

        self._words[normalized_word] = normalized_translation

    def get_random_word(self) -> str:
        """
        Возвращает случайное слово из словаря.

        Возвращает:
            str: Случайное слово (ключ) из словаря _words.

        Исключения:
            ValueError: Если словарь пуст.
        """
        if not self._words:
            raise ValueError('Словарь пуст')
        word = random.choice(list(self._words.keys()))
        self._last_word = word
        self._training_active = True
        return word

    def check_translation(self, word, translation) -> bool:
        """
        Проверяет, соответствует ли переданный перевод
        правильному переводу слова.

        Параметры:
            word (str): Слово для проверки.
            translation (str): Предполагаемый перевод.

        Возвращает:
            bool: True если перевод корректен, False если некорректен.

        Исключения:
            ValueError: Если слово отсутствует в словаре,
                       переданные аргументы не являются строками,
                       или переданное слово не совпадает с последним
                       выданным словом при активной тренировке.
        """
        if not isinstance(word, str):
            raise ValueError(
                f'Значение {word} должно быть строкой'
                )
        normalized_word = self.normalize_word(word)
        if normalized_word not in self._words:
            raise ValueError(
                f'Слово {word} отсутствует в словаре'
                )
        if not isinstance(translation, str):
            raise ValueError(
                f'Значение {translation} должно быть строкой'
                )

        # Защита от повторной проверки слова
        if self._training_active:
            if self._last_word is None:
                # Не должно происходить, но на всякий случай
                self._training_active = False
            elif normalized_word != self.normalize_word(self._last_word):
                self._training_active = False
                raise ValueError(
                    f'Переданное слово "{word}" не совпадает с последним '
                    f'выданным словом "{self._last_word}". '
                    'Тренировка завершена.'
                )

        normalized_translation = self.normalize_word(translation)
        correct_translation = self._words[normalized_word]
        return normalized_translation == correct_translation

    def get_translation(self, word) -> str:
        """
        Возвращает перевод указанного слова.

        Параметры:
            word (str): Слово, перевод которого требуется получить.

        Возвращает:
            str: Перевод слова.

        Исключения:
            ValueError: Если слово отсутствует в словаре или
                       переданный аргумент не является строкой.
        """
        if not isinstance(word, str):
            raise ValueError(f'Параметр {word} должен быть строкой')
        normalized_word = self.normalize_word(word)
        if normalized_word not in self._words:
            raise ValueError(
                f'Слово {word} отсутствует в словаре'
                )
        return self._words[normalized_word]
