from pathlib import Path


class TextFileLoader:
    """
    Загрузчик и сохранение слов из/в текстовый файл.

    Класс предоставляет методы для чтения слов из текстового файла
    в формате "слово,перевод" и сохранения словаря обратно в файл.

    Parameters
    ----------
    file_path : str or Path, optional
        Путь к текстовому файлу. По умолчанию "./words.txt".

    Raises
    ------
    ValueError
        Если `file_path` является директорией.

    Examples
    --------
    >>> loader = TextFileLoader()
    >>> words = loader.load_words()
    >>> isinstance(words, dict)
    True

    >>> loader = TextFileLoader(file_path="custom_words.txt")
    >>> loader.save_words({"hello": "привет"})
    """
    def __init__(self, *, file_path="./words.txt"):
        file_path = Path(file_path)
        if file_path.is_dir():
            raise ValueError('Значение "file_path" не должно быть директорией')
        self._file_path = file_path

    def load_words(self):
        """
        Загружает слова из текстового файла.

        Файл должен содержать строки в формате "слово,перевод".
        Строки без запятой или с более чем одной запятой игнорируются.
        Пустые строки также игнорируются.

        Returns
        -------
        dict
            Словарь, где ключи — слова, значения — переводы.
            Если файл не существует, возвращается пустой словарь.

        Examples
        --------
        >>> loader = TextFileLoader()
        >>> # Предположим, файл words.txt содержит "hello,привет"
        >>> words = loader.load_words()
        >>> words.get("hello")
        'привет'
        """
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
        """
        Сохраняет словарь слов в текстовый файл.

        Каждая пара "слово,перевод" записывается на отдельной строке.
        Существующее содержимое файла перезаписывается.

        Parameters
        ----------
        words : dict
            Словарь, где ключи — слова, значения — переводы.

        Raises
        ------
        ValueError
            Если `words` не является словарём.
            Если произошла ошибка ввода-вывода при записи.

        Examples
        --------
        >>> loader = TextFileLoader(file_path="test.txt")
        >>> loader.save_words({"cat": "кошка", "dog": "собака"})
        >>> # Файл test.txt теперь содержит:
        >>> # cat,кошка
        >>> # dog,собака
        """
        if not isinstance(words, dict):
            raise ValueError('Параметр `words` должен быть словарём')
        try:
            with self._file_path.open("w", encoding="utf-8") as f:
                for word, translation in words.items():
                    f.write(f"{word},{translation}\n")
        except (IOError, OSError):
            raise ValueError('Не удалось сохранить слова')
