<<<<<<< HEAD
import pytest   # Не забудьте добавить импорт библиотеки.

from anki.anki import Anki
=======
import pytest
from anki.anki import Anki  # импорт из пакета anki, файла anki.py класса Anki


def test_everything_works_ok():
    """Проверяет, что наш способ организации тестов работает."""
    assert True, "Что-то пошло не так"


@pytest.mark.parametrize(
    "word, case, expected", [
        (
            "hello",
            "корректных данных",
            "hello"
        ),
        (
            "hello world",
            "отсутствия пробельных символов в начале или конце строки",
            "hello world"
        )
    ]
)
def test_normalize_word_method_returns_valid_input_unchanged(
    word, case, expected
):
    """Метод `normalize_word` класса `Anki` должен вернуть переданную строку
    неизменённой, если:
     - строка записана в нижнем регистре,
     - в начале и в конце строки нет пробелов.
    """
    assert Anki.normalize_word(word) == expected, (
        "Метод `normalize_word` должен возвращать неизменённую строку,"
        f" если {case}"
    )


@pytest.mark.parametrize(
    "word, expected", [
        ("pYtHoN", "python"),
        ("Hello World", "hello world"),
        ("   Python   ", "python"),
        ("\tHello World\n", "hello world")]
)
def test_normalize_word_method_normalizes_word(word, expected):
    """
    Метод `normalize_word` класса `Anki` должен
    выполнить нормализацию строки:
        - все символы приведены к нижнему регистру;
        - удалены пробелы в начале и в конце строки.
    """
    assert Anki.normalize_word(word) == expected, (
        "Метод `normalize_word` должен нормализовать"
        " некорректно отформатированные строки."
    )
>>>>>>> feature/add-ooop-top1l8


@pytest.mark.parametrize('invalid_input', [
    1,
    [],
    set(),
<<<<<<< HEAD
    "Hello",  # корректное значение - строка
=======
>>>>>>> feature/add-ooop-top1l8
])
def test_normalize_word_raises_ValueError_on_invalid_input(invalid_input):
    """Метод `normalize_word` класса `Anki` должен выдавать исключение
    `ValueError`, если в качестве значения параметра `word`
    передана не строка.
<<<<<<< HEAD
    
    Этот тест демонстрирует использование pytest.fail для явного провала теста
    в случае, когда ожидаемое исключение не было выброшено. Для нестроковых
    данных (число, список, множество) метод должен выбросить ValueError
    с сообщением, содержащим "должен быть строкой". Для строки исключение
    не ожидается, и тест проваливается с помощью pytest.fail, что позволяет
    разработчику увидеть разницу в поведении.
    
    Чтобы понять, почему тест ведёт себя именно так, разработчик должен
    открыть этот файл и найти определение тестовной функции, а также
    ознакомиться с реализацией метода normalize_word в anki.py.
    """
    if isinstance(invalid_input, str):
        # Для строки ожидаем нормализацию, а не исключение
        result = Anki.normalize_word(invalid_input)
        assert result == "hello"
    else:
        # Для нестроковых данных ожидаем ValueError
        with pytest.raises(ValueError) as exc_info:
            Anki.normalize_word(invalid_input)
        assert 'должен быть строкой' in str(exc_info.value)


@pytest.mark.parametrize('invalid_words', [
=======
    """
    with pytest.raises(ValueError, match='должно быть строкой'):
        Anki.normalize_word(invalid_input)
        pytest.fail(
            "Метод `normalize_word` должен выдавать ValueError"
            " для нестроковых параметров"
        )


@pytest.mark.parametrize('invalid_input', [
>>>>>>> feature/add-ooop-top1l8
    42,
    "not a dict",
    [],
    set(),
])
<<<<<<< HEAD
def test_anki_init_raises_ValueError_on_invalid_input(invalid_words):
    """Проверяет, что передача в параметр words значений, которые не являются
    словарём, вызывает ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Anki(words=invalid_words)
    assert 'должно быть словарём' in str(exc_info.value)


@pytest.mark.parametrize('word,translation', [
=======
def test_anki_init_raises_ValueError_on_invalid_input(invalid_input):
    """Проверьте, что передача в параметр words значений,
    которые не являются словарём, вызывает ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Anki(words=invalid_input)
    assert 'быть словарём' in str(exc_info.value)


@pytest.mark.parametrize('word, translation', [
>>>>>>> feature/add-ooop-top1l8
    (42, "valid"),
    ("valid", 42),
    ([], "valid"),
    ("valid", []),
    (None, "valid"),
    ("valid", None),
])
def test_anki_add_word_raises_ValueError_on_invalid_input(word, translation):
<<<<<<< HEAD
    """Проверяет, что передача в word или translation значений, которые не
    являются строками, вызывает ValueError."""
    anki = Anki()
    with pytest.raises(ValueError) as exc_info:
        anki.add_word(word, translation)
    assert 'должен быть строкой' in str(exc_info.value)


def test_contains():
    """Проверяет работу магического метода __contains__."""
    anki = Anki(words={"Python": "Питон", "Java": "Джава"})
    
    # Существующие слова (с учётом нормализации)
    assert "python" in anki
    assert "Python" in anki
    assert "PYTHON" in anki
    assert "java" in anki
    assert "Java" in anki
    
    # Несуществующие слова
    assert "javascript" not in anki
    assert "TypeScript" not in anki
    
    # Проверка, что метод использует normalize_word
    # (слова с пробелами по краям)
    assert "  python  " in anki
    assert "  Java  " in anki


def test_contains_raises_ValueError_on_non_string():
    """Проверяет, что __contains__ вызывает ValueError для нестроковых
    аргументов."""
    anki = Anki(words={"Python": "Питон"})
    
    with pytest.raises(ValueError) as exc_info:
        _ = 42 in anki
    assert 'должен быть строкой' in str(exc_info.value)
    
    with pytest.raises(ValueError) as exc_info:
        _ = [] in anki
    assert 'должен быть строкой' in str(exc_info.value)
    
    with pytest.raises(ValueError) as exc_info:
        _ = None in anki
    assert 'должен быть строкой' in str(exc_info.value)


def test_str():
    """Проверяет работу магического метода __str__."""
    # Пустой словарь
    anki = Anki()
    assert str(anki) == "Anki словарь с 0 слов(ами)"
    
    # С одним словом
    anki = Anki(words={"Python": "Питон"})
    assert str(anki) == "Anki словарь с 1 слов(ами)"
    
    # С несколькими словами
    anki = Anki(words={
        "Python": "Питон",
        "Java": "Джава",
        "C++": "Си плюс плюс"
    })
    assert str(anki) == "Anki словарь с 3 слов(ами)"


def test_get_random_word():
    """Проверяет работу метода get_random_word."""
    # Словарь с несколькими словами
    anki = Anki(words={
        "Python": "Питон",
        "Java": "Джава",
        "C++": "Си плюс плюс"
    })
    random_word = anki.get_random_word()
    assert random_word in {"python", "java", "c++"}
    
    # Пустой словарь должен вызывать ValueError
    empty_anki = Anki()
    with pytest.raises(ValueError) as exc_info:
        empty_anki.get_random_word()
    assert 'Словарь пуст' in str(exc_info.value)


def test_check_translation():
    """Проверяет работу метода check_translation."""
    anki = Anki(words={"Python": "Питон", "Java": "Джава"})
    
    # Корректный перевод
    assert anki.check_translation("Python", "Питон") is True
    assert anki.check_translation("python", "питон") is True
    assert anki.check_translation("  Python  ", "  Питон  ") is True
    
    # Некорректный перевод
    assert anki.check_translation("Python", "Джава") is False
    assert anki.check_translation("java", "Питон") is False
    
    # Проверка нормализации
    assert anki.check_translation("PYTHON", "ПИТОН") is True
    
    # Отсутствующее слово вызывает ValueError
    with pytest.raises(ValueError) as exc_info:
        anki.check_translation("JavaScript", "Джаваскрипт")
    assert 'отсутствует в словаре' in str(exc_info.value)
    
    # Нестроковые аргументы вызывают ValueError
    with pytest.raises(ValueError) as exc_info:
        anki.check_translation(42, "Питон")
    assert 'должен быть строкой' in str(exc_info.value)
    
    with pytest.raises(ValueError) as exc_info:
        anki.check_translation("Python", 42)
    assert 'должен быть строкой' in str(exc_info.value)


def test_get_translation():
    """Проверяет работу метода get_translation."""
    anki = Anki(words={"Python": "Питон", "Java": "Джава"})
    
    # Получение перевода
    assert anki.get_translation("Python") == "питон"
    assert anki.get_translation("python") == "питон"
    assert anki.get_translation("  Python  ") == "питон"
    assert anki.get_translation("JAVA") == "джава"
    
    # Отсутствующее слово вызывает ValueError
    with pytest.raises(ValueError) as exc_info:
        anki.get_translation("JavaScript")
    assert 'отсутствует в словаре' in str(exc_info.value)
    
    # Нестроковый аргумент вызывает ValueError
    with pytest.raises(ValueError) as exc_info:
        anki.get_translation(42)
    assert 'должен быть строкой' in str(exc_info.value)
=======
    """
    Проверьте, что передача в word или translation значений,
    которые не являются строками, вызывает ValueError."""
    anki = Anki()
    with pytest.raises(ValueError) as exc_info:
        anki.add_word(word, translation)
    assert 'быть строкой' in str(exc_info.value)
>>>>>>> feature/add-ooop-top1l8
