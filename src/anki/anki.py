class Anki:
    app_version = '0.0.1'

    def __init__(self, *, words=None):
        # Инициализируем пустым словарём, если не передано значение
        if words is None:
            self.words = {}
        else:
            # Валидация: проверяем, что передан словарь
            if not isinstance(words, dict):
                raise ValueError(
                    'Значение параметра `words` должно быть словарём'
                )

            # Валидация: все ключи и значения должны быть строками
            for key, value in words.items():
                if not isinstance(key, str):
                    raise ValueError(
                        f'Ключ {repr(key)} должен быть строкой'
                    )
                if not isinstance(value, str):
                    raise ValueError(
                        f'Значение {repr(value)} должно быть строкой'
                    )

            # Создаем копию, чтобы избежать изменяемости
            self.words = words.copy()
