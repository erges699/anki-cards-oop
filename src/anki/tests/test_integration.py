<<<<<<< HEAD
import tempfile
import os
=======
>>>>>>> feature/add-ooop-top1l8
import pytest

from anki.loader import TextFileLoader
from anki.anki import Anki


<<<<<<< HEAD
@pytest.fixture
def temp_file_with_words():
    """Создаёт временный файл с начальными словами."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False, encoding='utf-8'
    ) as f:
        f.write("hello,привет\n")
        f.write("world,мир\n")
        f.flush()
        os.fsync(f.fileno())
        temp_path = f.name
    # файл закрыт, данные записаны
    yield temp_path
    os.unlink(temp_path)


def test_integration(temp_file_with_words):
    """Проверяет полный сценарий работы приложения."""
    # 1. Создайте TextFileLoader с временным файлом.
    loader = TextFileLoader(file_path=temp_file_with_words)
    
    # 2. Загрузите слова методом load_words().
    loaded_words = loader.load_words()
    assert loaded_words == {"hello": "привет", "world": "мир"}
    
    # 3. Создайте Anki с загруженными словами.
    anki = Anki(words=loaded_words)
    
    # 4. Проверьте, что get_words() возвращает правильные слова.
    words_from_anki = anki.get_words()
    assert words_from_anki == {"hello": "привет", "world": "мир"}
    
    # 5. Добавьте новое слово через add_word().
    anki.add_word("python", "питон")
    
    # Проверяем, что слово добавилось
    updated_words = anki.get_words()
    expected = {
=======
@pytest.fixture()
def tmp_file(tmp_path):
    # Создаём объект пути до файла.
    path = tmp_path / "test_words.txt"
    # Сохраняем в файл слова.
    path.write_text("hello,привет\nworld,мир\npython,питон\n")
    # Возвращаем путь до файла из фикстуры.
    return str(path)


def test_integration(tmp_file):
    # 1. Создайте TextFileLoader с временным файлом.
    loader = TextFileLoader(file_path=tmp_file)
    words = {
>>>>>>> feature/add-ooop-top1l8
        "hello": "привет",
        "world": "мир",
        "python": "питон"
    }
<<<<<<< HEAD
    assert updated_words == expected
    
    # 6. Сохраните слова через save_words().
    loader.save_words(updated_words)
    
    # 7. Проверьте, что файл содержит все слова (исходные и новое).
    with open(temp_file_with_words, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    lines = content.split('\n')
    assert len(lines) == 3
    assert "hello,привет" in lines
    assert "world,мир" in lines
    assert "python,питон" in lines
=======
    loader.save_words(words)

    # 2. Загрузите слова методом load_words().
    loaded_words = loader.load_words()
    assert loaded_words == words

    # 3. Создайте Anki с загруженными словами.
    anki = Anki(words=loaded_words)

    # 4. Проверьте, что get_words() возвращает правильные слова.
    words_from_anki = anki.get_words()
    assert words_from_anki == words

    # 5. Добавьте новое слово через add_word().
    anki.add_word("apple", "яблоко")

    updated_words = anki.get_words()
    expected_words = {
        "hello": "привет",
        "world": "мир",
        "python": "питон",
        "apple": "яблоко"
    }
    assert updated_words == expected_words

    # 6. Сохраните слова через save_words().
    loader.save_words(updated_words)

    # 7. Проверьте, что файл содержит все слова (исходные и новое).
    loaded_words = loader.load_words()
    assert loaded_words == expected_words
>>>>>>> feature/add-ooop-top1l8
