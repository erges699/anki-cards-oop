from pathlib import Path
from typing import Dict


class TextFileLoader:
    def __init__(self, *, file_path="./words.txt"):
        self._file_path = Path(file_path)

        if self._file_path.is_dir():
            raise ValueError(
                f'Переданный путь {file_path} является директорией, '
                'а не файлом'
            )

    def load_words(self) -> Dict[str, str]:
        if not self._file_path.exists():
            return {}

        words = {}
        try:
            with open(self._file_path, "r", encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.count(',') != 1:
                        continue
                    word, description = line.split(',', 1)
                    words[word.strip()] = description.strip()
        except (IOError, OSError):
            return {}

        return words

    def save_words(self, words: Dict[str, str]) -> None:
        if not isinstance(words, dict):
            raise ValueError('Параметр "words" должен быть словарём')
        try:
            with open(self._file_path, "w", encoding='utf-8') as output:
                for word, translation in words.items():
                    # Сохраняем в формате "слово, перевод\n"
                    output.write(f'{word},{translation}\n')
        except (IOError, OSError) as e:
            # Пробрасываем исключение дальше
            raise e

        # count, word_form = make_word_form(words)
        # print(f'Было сохранено {count} {word_form} в файл {filename}')
