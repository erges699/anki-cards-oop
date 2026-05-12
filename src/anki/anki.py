class Anki:
    app_version = '0.0.1'

    def __init__(self, *, words=None):
        if words is None:
            self.words = {}
        else:
            if not isinstance(words, dict):
                raise ValueError(
                    'Значение параметра "words" должно быть словарём'
                    )

            for word, translation in words.items():
                if not isinstance(word, str):
                    raise ValueError(
                        f'Значение {word} должно быть строкой'
                        )
                if not isinstance(translation, str):
                    raise ValueError(
                        f'Значение {translation} должно быть строкой'
                        )
            self.words = words
