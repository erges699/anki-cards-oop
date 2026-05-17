class Anki:
    """основная логики игры"""
    def __init__(self, *, words=None):
        if words is None:
            words = {}
        else:
            if not isinstance(words, dict):
                raise ValueError(
                    'Значение параметра "words" должно быть словарём'
                )
            for word, translation in words.items():
                if not isinstance(word, str):
                    raise ValueError('Ключ словаря должен быть строкой')
                if not isinstance(translation, str):
                    raise ValueError('Значение словаря должно быть строкой')
        self.words = words
