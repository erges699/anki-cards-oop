class Anki:
    app_version = '0.0.1'

    @staticmethod
    def normalize_word(word):
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

    def get_words(self):
        """
        Возвращает копию словаря слов.
        
        Возвращает:
            dict: Копия словаря вида {"слово": "перевод"}.
        """
        import copy
        return copy.deepcopy(self._words)

    def add_word(self, word, translation):
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
