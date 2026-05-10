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
