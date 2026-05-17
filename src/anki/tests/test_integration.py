import pytest

from anki.loader import TextFileLoader
from anki.anki import Anki


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
        "hello": "привет",
        "world": "мир",
        "python": "питон"
    }
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
