from pathlib import Path


class TextFileLoader:
    """загрузка слов из текстового файла"""
    def __init__(self, *, file_path="./words.txt"):
        file_path = Path(file_path)
        if file_path.is_dir():
            raise ValueError('Значение "file_path" не должно быть директорией')
        self._file_path = file_path

    def load_words(self):
        """загрузка слов из текстового файла"""
        if not self._file_path.exists():
            return {}
        words = {}
        try:
            with self._file_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Игнорируем строки без запятой или с лишними запятыми
                    if line.count(',') != 1:
                        continue
                    word, translation = line.split(',', 1)
                    words[word.strip()] = translation.strip()
        except FileNotFoundError:
            return {}

        return words

    def save_words(self, words):
        """сохранение слов в текстовый файл"""
        if not isinstance(words, dict):
            raise ValueError('Параметр `words` должен быть словарём')
        try:
            with self._file_path.open("w", encoding="utf-8") as f:
                for word, translation in words.items():
                    f.write(f"{word},{translation}\n")
        except (IOError, OSError):
            raise ValueError('Не удалось сохранить слова')
