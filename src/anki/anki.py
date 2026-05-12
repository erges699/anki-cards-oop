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

    def get_words(self) -> Dict[str, str]:
        """
        Возвращает копию словаря слов.

        Возвращает:
            dict: Копия словаря вида {"слово": "перевод"}.
        """
        import copy
        return copy.deepcopy(self._words)

    def add_word(self, word, translation) -> None:
        """
        Добавляет слово и его перевод в словарь words.

        Параметры:
            word (str): Слово на иностранном языке.
            translation (str): Перевод слова.

        Исключения:
            ValueError: Если word или translation не являются строками.
        """
        if not isinstance(word, str):
            raise ValueError(
                f'Значение {word} должно быть строкой'
                )
        if not isinstance(translation, str):
            raise ValueError(
                f'Значение {translation} должно быть строкой'
                )
        normalized_word = self.normalize_word(word)
        normalized_translation = self.normalize_word(translation)
        self._words[normalized_word] = normalized_translation
