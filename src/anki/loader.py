from pathlib import Path


class TextFileLoader:
    """загрузка слов из текстового файла"""
    def __init__(self, *, file_path="./words.txt"):
        file_path = Path(file_path)
        if file_path.is_dir():
            raise ValueError('Значение "file_path" не должно быть директорией')
        self.file_path = file_path
