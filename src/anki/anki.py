import copy
import random

from typing import Dict


class Anki:
    """Для класса `Anki` разработан докстринг"""
    app_version = '0.0.1'

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
                    raise ValueError(
                        f'Значение {word} должно быть строкой'
                        )
                if not isinstance(translation, str):
                    raise ValueError(
                        f'Значение {translation} должно быть строкой'
                        )

                normalized_key = self.normalize_word(word)
                normalized_value = self.normalize_word(translation)
                normalized_words[normalized_key] = normalized_value

            self._words = normalized_words

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

    def get_words(self) -> Dict[str, str]:
        """
        Возвращает копию словаря слов.

        Возвращает:
            dict: Копия словаря вида {"слово": "перевод"}.
        """
        return copy.deepcopy(self._words)

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
        return random.choice(list(self._words.keys()))

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
            ValueError: Если слово отсутствует в словаре или
                       переданные аргументы не являются строками.
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
