<<<<<<< HEAD
import tempfile
import os
=======
>>>>>>> feature/add-ooop-top1l8
import pytest

from anki.loader import TextFileLoader


<<<<<<< HEAD
@pytest.fixture
def temp_file():
    """Создаёт временный файл и возвращает его путь."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False
    ) as f:
        yield f.name
    os.unlink(f.name)


def test_save_words_saves_words_as_comma_separated_values(temp_file):
    """Проверяет, что слова сохраняются в файл в формате «слово,перевод»."""
    loader = TextFileLoader(file_path=temp_file)
=======
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
    """Проверьте, что слова сохраняются в файл в формате «слово,перевод»."""
    loader = TextFileLoader(file_path=tmp_file)
>>>>>>> feature/add-ooop-top1l8
    words = {
        "hello": "привет",
        "world": "мир",
        "python": "питон"
    }
<<<<<<< HEAD
    
    # Сохраняем слова
    loader.save_words(words)
    
    # Читаем файл и проверяем содержимое
    with open(temp_file, 'r', encoding='utf-8') as f:
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
=======
    loader.save_words(words)
    loaded_words = loader.load_words()
    assert loaded_words == words
>>>>>>> feature/add-ooop-top1l8
