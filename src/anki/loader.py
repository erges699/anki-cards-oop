import json
import urllib.request

from pathlib import Path
from typing import Dict, Any


class LoaderRegistry:

    def __init__(self):
        self._registry = {}

    def register(self, ident):
        """Регистрирует класс загрузчик в реестре `self._registry`"""
        def decorator(cls):
            self._registry[ident] = cls
            return cls

        return decorator

    def get_loader(self, ident):
        """Выбирает конкретный класс загрузчика по идентификатору"""

        try:
            return self._registry[ident]
        except KeyError:
            raise ValueError(f"Неизвестный тип источника слов: {ident}")


loader_registry = LoaderRegistry()


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


@loader_registry.register('.txt')
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


@loader_registry.register('.tsv')
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


@loader_registry.register('.json')
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


@loader_registry.register('http')
class JsonNetworkLoader:
    """
    Загружает слова по сети из JSON-файла, доступного по URL.
    Не поддерживает сохранение (метод save_words является заглушкой).
    """
    def __init__(self, *, url: str):
        """
        Инициализатор класса JsonNetworkLoader.

        Параметры:
            url (str): URL JSON-файла со словами.
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError(
                'URL должен начинаться с http:// или https://, '
                f'получено: {url}'
            )
        self.url = url

    def load_words(self) -> Dict[str, str]:
        """
        Загружает слова по ссылке из атрибута url.
        Поддерживает JSON-формат и текстовый CSV-формат (слово,перевод).

        Возвращает:
            dict: Словарь вида {"слово": "перевод"}.
                  Если ответ не является словарём или произошла ошибка сети,
                  возвращает пустой словарь.
        """
        try:
            with urllib.request.urlopen(self.url) as response:
                data = response.read().decode('utf-8')
                # Пробуем разобрать как JSON
                try:
                    words = json.loads(data)
                    if not isinstance(words, dict):
                        # Если структура не словарь, возвращаем пустой словарь
                        return {}
                    result = {}
                    for key, value in words.items():
                        result[str(key)] = str(value)
                    return result
                except json.JSONDecodeError:
                    # Если не JSON, пробуем текстовый формат (CSV)
                    lines = data.strip().splitlines()
                    result = {}
                    for i, line in enumerate(lines):
                        line = line.strip()
                        if not line:
                            continue
                        # Пропускаем заголовок, если он есть
                        if i == 0 and line.lower() in ('слово,перевод', 'word,translation'):
                            continue
                        if ',' not in line:
                            continue
                        parts = line.split(',', 1)
                        if len(parts) != 2:
                            continue
                        word, translation = parts
                        result[word.strip()] = translation.strip()
                    return result
        except (urllib.error.URLError, ValueError):
            # В случае ошибки сети возвращаем пустой словарь
            return {}

    def save_words(self, words: Dict[str, str]) -> None:
        """
        Метод-заглушка, который ничего не делает.
        Сохранение на удалённый URL не поддерживается.

        Параметры:
            words (dict): Словарь вида {"слово": "перевод"} для сохранения.
        """
        pass