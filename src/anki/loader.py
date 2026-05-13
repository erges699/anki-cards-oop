import json

from pathlib import Path
from typing import Dict, Any


class BaseFileLoader:
    """Для класса `BaseFileLoader` разработан докстринг"""
    DEFAULT_FILE_PATH = './words.txt'

    def __init__(self, *, file_path=None):
        if file_path is None:
            file_path = self.DEFAULT_FILE_PATH

        self._file_path = Path(file_path)

        if self._file_path.exists() and self._file_path.is_dir():
            raise ValueError(
                f'Путь {file_path} является директорией, а должен быть файлом'
            )

    def load_words(self) -> Dict[str, str]:
        """
        Загружает слова из файла, указанного в file_path.

        Возвращает:
            dict: Словарь вида {"слово": "перевод"}.
            Если файл не существует или пуст, возвращает пустой словарь.
        """
        if not self._file_path.exists():
            return {}

        with self._file_path.open("r", encoding="utf-8") as f:
            return self._load_from_file(f)

    def save_words(self, words: Dict[str, str]) -> None:
        """
        Сохраняет слова в файл, указанный в file_path.

        Параметры:
            words (dict): Словарь вида {"слово": "перевод"} для сохранения.

        Исключения:
            ValueError: Если параметр words не является словарём.
        """
        if not isinstance(words, dict):
            raise ValueError("Значением параметра `words` должен быть словарь")

        with self._file_path.open("w", encoding="utf-8") as f:
            return self._save_to_file(words, f)

    def _load_from_file(self, file_object: Any):
        """Реализует логику загрузки данных определённого
        формата из `file_object`.

        Метод должен быть переопределён в наследниках

        Parameters
        ----------
        file_object : FileLike
            FileLike объект, из которого идёт чтение данных

        Returns
        -------
        dict
            Словарь с загруженными словами
        """
        raise NotImplementedError

    def _save_to_file(self, words: Dict[str, str], file_object: Any):
        """Реализует логику сохранения слов в определённом формате в
        файл `file_object`.

        Метод должен быть переопределён в наследниках

        Parameters
        ----------
        words : dict
            Словарь с словами и переводами
        file_object : FileLike
            FileLike объект, из которого идёт чтение данных

        Returns
        -------
        None
        """
        raise NotImplementedError


class TextFileLoader(BaseFileLoader):
    """
    Реализует логику загрузки слов из текстового файла и логику сохранения
    слов в текстовый файл.

    Формат записи: "слово,перевод"
    """
    DEFAULT_FILE_PATH = "./words.txt"

    def _load_from_file(self, file_object):
        words = {}
        for line in file_object:
            word, translation = line.split(",")
            words[word.strip()] = translation.strip()
        return words

    def _save_to_file(self, words, file_object):
        for word, translation in words.items():
            file_object.write(f'{word},{translation}\n')


class TSVFileLoader(BaseFileLoader):
    """
    Реализует логику загрузки слов из TSV  файла и логику сохранения
    слов в TSV файл.

    Формат записи: "слово\tперевод"
    """

    DEFAULT_FILE_PATH = "./words.tsv"

    def _load_from_file(self, file_object):
        words = {}
        for line in file_object:
            word, translation = line.split("\t")
            words[word.strip()] = translation.strip()
        return words

    def _save_to_file(self, words, file_object):
        for word, translation in words.items():
            file_object.write(f'{word}\t{translation}\n')


class JsonFileLoader(BaseFileLoader):
    """
    Реализует логику загрузки слов из JSON файла и логику сохранения
    слов в JSON файл.

    Формат записи: {"слово": "перевод"}
    """

    DEFAULT_FILE_PATH = "./words.json"

    def _load_from_file(self, file_object):
        return json.load(file_object)

    def _save_to_file(self, words, file_object):
        json.dump(words, file_object, indent=2, ensure_ascii=False)
