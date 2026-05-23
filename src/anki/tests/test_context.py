#!/usr/bin/env python3
"""Тестирование контекстного менеджера game_context."""
import sys
import os

from anki.loader import TextFileLoader
from anki.anki import Anki
from anki.main import game_context


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_game_context():
    # Создаём временный файл со словами
    import tempfile
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.txt',
        delete=False
    ) as f:
        f.write("hello,привет\n")
        f.write("world,мир\n")
        temp_path = f.name

    try:
        loader = TextFileLoader(file_path=temp_path)
        anki = Anki()
        # Проверяем, что до контекста слова пусты
        assert len(anki.words) == 0

        with game_context(loader, anki) as ctx:
            # Проверяем, что слова загрузились
            assert len(anki.words) == 2
            assert anki.words.get('hello') == 'привет'
            assert anki.words.get('world') == 'мир'
            # Проверяем, что ctx - это тот же anki
            assert ctx is anki
            # Модифицируем слова
            anki.add_word('test', 'тест')

        # После выхода из контекста слова должны сохраниться
        # Проверяем, загрузив заново
        loader2 = TextFileLoader(file_path=temp_path)
        reloaded = loader2.load_words()
        assert reloaded.get('hello') == 'привет'
        assert reloaded.get('world') == 'мир'
        assert reloaded.get('test') == 'тест'

        print("✅ Все тесты пройдены!")
    finally:
        os.unlink(temp_path)


if __name__ == '__main__':
    test_game_context()
