class Anki:
    """основная логики игры"""
    def __init__(self, *, words=None):
        if words is None:
            self.words = {}
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
            self.words = normalized_words

    @staticmethod
    def normalize_word(word):
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        return word.lower().strip()

    def add_word(self, word, translation):
        if not isinstance(word, str):
            raise ValueError('Слово должно быть строкой')
        if not isinstance(translation, str):
            raise ValueError('Перевод должен быть строкой')
        normalize_word = self.normalize_word(word)
        normalize_translation = self.normalize_word(translation)
        self.words[normalize_word] = normalize_translation
