import tempfile
import os
import pytest

from anki.loader import TextFileLoader


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
    words = {
        "hello": "привет",
        "world": "мир",
        "python": "питон"
    }
    
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