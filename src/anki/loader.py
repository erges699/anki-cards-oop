from __future__ import annotations

import json
import requests
from pathlib import Path
from typing import Dict,Type, Optional, Union, Any, Protocol, runtime_checkable, TextIO


class LoaderRegistry:

    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseFileLoader]] = {}

    def register(self, ident: str):
        """Регистрирует класс загрузчик в реестре `self._registry`"""
        def decorator(cls: Type[BaseFileLoader]) -> Type[BaseFileLoader]:
            self._registry[ident] = cls
            return cls

        return decorator

    def get_loader(self, ident: str) -> Type[BaseFileLoader]:
        """Выбирает конкретный класс загрузчика по идентификатору"""

        try:
            return self._registry[ident]
        except KeyError:
            raise ValueError(f"Неизвестный тип источника слов: {ident}")


loader_registry = LoaderRegistry()


class BaseFileLoader:
    """
    Базовый класс для загрузчиков файлов со словами.

    Предоставляет общий интерфейс для загрузки и сохранения словаря слов
    из/в файлы различных форматов.

    Parameters
    ----------
    file_path : str or Path, optional
        Путь к файлу для загрузки/сохранения слов.
        По умолчанию './words.txt'.

    Raises
    ------
    ValueError
        Если переданный путь является директорией, а не файлом.

    Notes
    -----
    Класс является абстрактным базовым классом. Реализации конкретных форматов
    должны быть предоставлены в наследниках через переопределение методов
    `_load_from_file` и `_save_to_file`.
    """

    def __init__(self, *, file_path: Union[str, Path] = './words.txt') -> None:
        self._file_path = Path(file_path)

        if self._file_path.exists() and self._file_path.is_dir():
            raise ValueError(
                f"Путь {file_path} является директорией, а должен быть файлом"
            )

    def load_words(self) -> Dict[str, str]:
        """
        Загружает слова из файла.

        Returns
        -------
        dict
            Словарь, где ключи - слова, значения - переводы.
            Если файл не существует, возвращает пустой словарь.

        Notes
        -----
        Метод открывает файл в режиме чтения с кодировкой UTF-8 и передаёт
        файловый объект в метод `_load_from_file`, который должен быть
        реализован в наследниках.
        """
        if not self._file_path.exists():
            return {}

        with self._file_path.open("r", encoding="utf-8") as f:
            return self._load_from_file(f)

    def save_words(self, words: Dict[str, str]) -> None:
        """
        Сохраняет слова в файл.

        Parameters
        ----------
        words : dict
            Словарь, где ключи - слова, значения - переводы.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Если `words` не является словарём.

        Notes
        -----
        Метод открывает файл в режиме записи с кодировкой UTF-8 и передаёт
        файловый объект в метод `_save_to_file`, который должен быть
        реализован в наследниках.
        """
        if not isinstance(words, dict):
            raise ValueError("Значением параметра `words` должен быть словарь")

        with self._file_path.open("w", encoding="utf-8") as f:
            return self._save_to_file(words, f)

    def _load_from_file(self, file_object):
        """
        Реализует логику загрузки данных определённого формата из файла.

        Метод должен быть переопределён в наследниках.

        Parameters
        ----------
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для чтения.

        Returns
        -------
        dict
            Словарь, где ключи - слова, значения - переводы.

        Raises
        ------
        NotImplementedError
            Если метод не переопределён в наследнике.

        Notes
        -----
        Этот метод вызывается из `load_words` после открытия файла.
        Наследники должны реализовать конкретную логику парсинга формата.
        """
        raise NotImplementedError

    def _save_to_file(self, words, file_object):
        """
        Реализует логику сохранения слов в определённом формате в файл.

        Метод должен быть переопределён в наследниках.

        Parameters
        ----------
        words : dict
            Словарь, где ключи - слова, значения - переводы.
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для записи.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            Если метод не переопределён в наследнике.

        Notes
        -----
        Этот метод вызывается из `save_words` после открытия файла.
        Наследники должны реализовать конкретную логику сериализации формата.
        """
        raise NotImplementedError


@loader_registry.register('.txt')
class TextFileLoader(BaseFileLoader):
    """
    Загрузчик для текстовых файлов с разделителем-запятой.

    Реализует логику загрузки слов из текстового файла и сохранения
    слов в текстовый файл в формате "слово,перевод".

    Parameters
    ----------
    file_path : str or Path, optional
        Путь к текстовому файлу. По умолчанию './words.txt'.

    Attributes
    ----------
    DEFAULT_FILE_PATH : str
        Путь по умолчанию ('./words.txt').

    Notes
    -----
    Формат файла: каждая строка содержит одно слово и его перевод,
    разделённые запятой. Пробелы вокруг слова и перевода обрезаются.

    Пример содержимого файла:
        apple,яблоко
        cat,кот
        dog,собака

    Raises
    ------
    ValueError
        Если строка не содержит запятой или содержит более одной запятой.
    """

    DEFAULT_FILE_PATH = "./words.txt"

    def _load_from_file(self, file_object):
        """
        Загружает слова из текстового файла с разделителем-запятой.

        Parameters
        ----------
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для чтения.

        Returns
        -------
        dict
            Словарь, где ключи - слова, значения - переводы.

        Raises
        ------
        ValueError
            Если строка не содержит ровно одной запятой.

        Notes
        -----
        Каждая строка файла должна иметь формат "слово,перевод".
        Пробелы вокруг слова и перевода обрезаются.
        Пустые строки игнорируются (split вызовет ValueError).
        """
        words = {}
        for line in file_object:
            word, translation = line.split(",")
            words[word.strip()] = translation.strip()
        return words

    def _save_to_file(
            self, words: Dict[str, str], file_object: TextIO
    ) -> None:
        """
        Сохраняет слова в текстовый файл с разделителем-запятой.

        Parameters
        ----------
        words : dict
            Словарь, где ключи - слова, значения - переводы.
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для записи.

        Returns
        -------
        None

        Notes
        -----
        Каждая пара "слово,перевод" записывается на отдельной строке.
        Пробелы вокруг слова и перевода не добавляются.
        """
        for word, translation in words.items():
            file_object.write(f'{word},{translation}\n')


@loader_registry.register('.tsv')
class TSVFileLoader(BaseFileLoader):
    """
    Загрузчик для TSV (Tab‑Separated Values) файлов.

    Реализует логику загрузки слов из TSV‑файла и сохранения
    слов в TSV‑файл в формате "слово\tперевод".

    Parameters
    ----------
    file_path : str or Path, optional
        Путь к TSV‑файлу. По умолчанию './words.tsv'.

    Attributes
    ----------
    DEFAULT_FILE_PATH : str
        Путь по умолчанию ('./words.tsv').

    Notes
    -----
    Формат файла: каждая строка содержит одно слово и его перевод,
    разделённые символом табуляции (\\t). Пробелы вокруг слова и перевода
    обрезаются.

    Пример содержимого файла:
        apple\tяблоко
        cat\tкот
        dog\tсобака

    Raises
    ------
    ValueError
        Если строка не содержит ровно одной табуляции.
    """

    DEFAULT_FILE_PATH = "./words.tsv"

    def _load_from_file(self, file_object: TextIO) -> Dict[str, str]:
        """
        Загружает слова из TSV‑файла с разделителем-табуляцией.

        Parameters
        ----------
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для чтения.

        Returns
        -------
        dict
            Словарь, где ключи - слова, значения - переводы.

        Raises
        ------
        ValueError
            Если строка не содержит ровно одной табуляции.

        Notes
        -----
        Каждая строка файла должна иметь формат "слово\\tперевод".
        Пробелы вокруг слова и перевода обрезаются.
        Пустые строки игнорируются (split вызовет ValueError).
        """
        words = {}
        for line in file_object:
            word, translation = line.split("\t")
            words[word.strip()] = translation.strip()
        return words

    def _save_to_file(self, words, file_object):
        """
        Сохраняет слова в TSV‑файл с разделителем-табуляцией.

        Parameters
        ----------
        words : dict
            Словарь, где ключи - слова, значения - переводы.
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для записи.

        Returns
        -------
        None

        Notes
        -----
        Каждая пара "слово\\tперевод" записывается на отдельной строке.
        Пробелы вокруг слова и перевода не добавляются.
        """
        for word, translation in words.items():
            file_object.write(f'{word}\t{translation}\n')


@loader_registry.register('.json')
class JsonFileLoader(BaseFileLoader):
    """
    Загрузчик для JSON‑файлов.

    Реализует логику загрузки слов из JSON‑файла и сохранения
    слов в JSON‑файл.

    Parameters
    ----------
    file_path : str or Path, optional
        Путь к JSON‑файлу. По умолчанию './words.json'.

    Attributes
    ----------
    DEFAULT_FILE_PATH : str
        Путь по умолчанию ('./words.json').

    Notes
    -----
    Формат файла: JSON‑объект, где ключи - слова, значения - переводы.
    Файл сохраняется с отступами (indent=2) и поддержкой Unicode
    (ensure_ascii=False).

    Пример содержимого файла:
        {
          "apple": "яблоко",
          "cat": "кот",
          "dog": "собака"
        }

    Raises
    ------
    json.JSONDecodeError
        Если файл содержит некорректный JSON.
    """

    DEFAULT_FILE_PATH = "./words.json"

    def _load_from_file(self, file_object):
        """
        Загружает слова из JSON‑файла.

        Parameters
        ----------
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для чтения.

        Returns
        -------
        dict
            Словарь, где ключи - слова, значения - переводы.

        Raises
        ------
        json.JSONDecodeError
            Если файл содержит некорректный JSON.
        """
        return json.load(file_object)

    def _save_to_file(self, words, file_object):
        """
        Сохраняет слова в JSON‑файл.

        Parameters
        ----------
        words : dict
            Словарь, где ключи - слова, значения - переводы.
        file_object : io.TextIOBase
            Текстовый файловый объект, открытый для записи.

        Returns
        -------
        None

        Notes
        -----
        JSON записывается с отступами (indent=2) и поддержкой Unicode
        (ensure_ascii=False).
        """
        json.dump(words, file_object, indent=2, ensure_ascii=False)


@loader_registry.register('http')
class JsonNetworkLoader():
    """
    Загрузчик для JSON-файлов.

    Реализует логику загрузки слов из JSON-файла и сохранения
    слов в JSON-файл.

    Parameters
    ----------
    url : str or Path, optional
    """

    def __init__(self, url: str):
        """
        Инициализатор класса JsonNetworkLoader.

        Параметры:
            url (str): URL JSON-файла со словами.
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError(
                f'URL должен начинаться с http:// или https://, получено:'
                f'{url}'
            )
        self.url = url

    def load_words(self):
        """
        Загружает слова по ссылке из атрибута url.
        Поддерживает JSON-формат и текстовый CSV-формат (слово,перевод).

        Возвращает:
            dict: Словарь вида {"слово": "перевод"}.
                  Если ответ не является словарём или произошла ошибка сети,
                  возвращает пустой словарь.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            # Пробуем разобрать как JSON
            try:
                words = response.json()
                if not isinstance(words, dict):
                    # Если структура не словарь, возвращаем пустой словарь
                    return {}
                result = {}
                for key, value in words.items():
                    result[str(key)] = str(value)
                return result
            except json.JSONDecodeError:
                # Если не JSON, пробуем текстовый формат (CSV)
                data = response.text
                lines = data.strip().splitlines()
                result = {}
                for i, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    # Пропускаем заголовок, если он есть
                    if i == 0 and line.lower() in (
                        'слово,перевод',
                        'word,translation'
                    ):
                        continue
                    if ',' not in line:
                        continue
                    parts = line.split(',', 1)
                    if len(parts) != 2:
                        continue
                    word, translation = parts
                    result[word.strip()] = translation.strip()
                return result
        except (requests.RequestException, ValueError):
            # В случае ошибки сети возвращаем пустой словарь
            return {}

    def save_words(self, words):
        """
        Метод-заглушка, который ничего не делает.
        Сохранение на удалённый URL не поддерживается.

        Параметры:
            words (dict): Словарь вида {"слово": "перевод"} для сохранения.
        """
        pass
