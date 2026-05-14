import json
import urllib.request
from typing import Dict


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