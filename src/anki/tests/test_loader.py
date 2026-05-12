import os
import pathlib
import pytest

from anki.loader import TextFileLoader


@pytest.fixture()
def tmp_file(tmp_path):
    # Создаём объект пути до файла.
    path = tmp_path / "test_words.txt"
    # Сохраняем в файл слова.
    path.write_text("hello,привет\n", encoding="utf-8")
    # Возвращаем путь до файла из фикстуры.
    return str(path)


def test_load_words_loads_words_from_comma_separated_values(tmp_file):
    """Метод `load_words` класса `TextFileLoader` должен выполнить
    загрузку слов из файла, путь до которого передан
    при инициализации экземпляра класса `TextFileLoader`.
    """
    loader = TextFileLoader(file_path=tmp_file)
    words = loader.load_words()
    assert words == {"hello": "привет"}


def test_save_words_saves_words_as_comma_separated_values(tmp_file):
    """Проверьте, что слова сохраняются в файл в формате «слово,перевод»"""
    loader = TextFileLoader(file_path=tmp_file)
    words = {
        "hello": "привет",
        "world": "мир",
        "python": "питон"
    }

    # Сохраняем слова
    loader.save_words(words)

    # Читаем файл и проверяем содержимое
    with open(tmp_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    # Ожидаемые строки
    expected_lines = [
        "hello,привет",
        "world,мир",
        "python,питон"
    ]

    # Проверяем, что строки совпадают (порядок может быть любым)
    assert len(lines) == len(expected_lines)
    for line in lines:
        assert line in expected_lines
