from pathlib import Path


class TextFileLoader():
    def __init__(self, *, file_path="./words.txt"):
        # Преобразуем переданный путь в объект Path
        self.file_path = Path(file_path)

        # Валидация: путь не должен быть директорией
        if self.file_path.is_dir():
            raise ValueError(
                f'Переданный путь {file_path} является директорией, '
                'а не файлом'
            )

    def load_words(self):
        """
        Загружает слова из файла, указанного в file_path.

        Возвращает:
            dict: Словарь вида {"слово": "перевод"}.
            Если файл не существует или пуст, возвращает пустой словарь.
        """
        # Проверяем существование файла
        if not self.file_path.exists():
            return {}

        words = {}
        try:
            with self.file_path.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:  # Пропускаем пустые строки
                        continue
                    # Разделяем по первой запятой
                    if ',' in line:
                        word, translation = line.split(',', 1)
                        words[word.strip()] = translation.strip()
                    else:
                        # Если запятой нет, пропускаем строку
                        continue
        except (IOError, OSError):
            # В случае ошибок чтения возвращаем пустой словарь
            return {}

        return words

    def save_words(self, words):
        """
        Сохраняет слова в файл, указанный в file_path.

        Параметры:
            words (dict): Словарь вида {"слово": "перевод"} для сохранения.

        Исключения:
            ValueError: Если параметр words не является словарём.
        """
        # Валидация: проверяем, что передан словарь
        if not isinstance(words, dict):
            raise ValueError('Параметр `words` должен быть словарём')

        try:
            with self.file_path.open('w', encoding='utf-8') as f:
                for word, translation in words.items():
                    # Записываем в формате "слово,перевод"
                    f.write(f"{word},{translation}\n")
        except (IOError, OSError) as e:
            # Пробрасываем исключение дальше
            raise e
