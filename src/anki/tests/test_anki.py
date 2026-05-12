import pytest

from anki.anki import Anki


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
        ),
        (
            "python",
            "корректных данных",
            "python"
        )
    ]
)
def test_normalize_word_method_returns_valid_input_unchanged(word, case, expected):
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
    """Метод `normalize_word` класса `Anki` должен выполнить нормализацию
    строки:
        - все символы приведены к нижнему регистру;
        - удалены пробелы в начале и в конце строки.
    """
    assert Anki.normalize_word(word) == expected, (
        "Метод `normalize_word` должен нормализовать"
        " некорректно отформатированные строки."
    )


@pytest.mark.parametrize('invalid_input', [
    1,
    [],
    set(),
])
def test_normalize_word_raises_ValueError_on_invalid_input(invalid_input):
    """Метод `normalize_word` класса `Anki` должен выдавать исключение
    `ValueError`, если в качестве значения параметра `word`
    передана не строка.
    """
    with pytest.raises(ValueError, match='должно быть строкой'):
        Anki.normalize_word(invalid_input)
        pytest.fail(
            "Метод `normalize_word` должен выдавать ValueError"
            " для нестроковых параметров"
        )


@pytest.mark.parametrize('invalid_words', [
    42,
    "not a dict",
    [],
    set(),
])
def test_anki_init_raises_ValueError_on_invalid_input(invalid_words):
    """Проверьте, что передача в параметр words значений, которые не являются словарём,
    вызывает ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Anki(words=invalid_words)
    assert 'должно быть словарём' in str(exc_info.value)


@pytest.mark.parametrize('word,translation', [
    (42, "valid"),
    ("valid", 42),
    ([], "valid"),
    ("valid", []),
    (None, "valid"),
    ("valid", None),
])
def test_anki_add_word_raises_ValueError_on_invalid_input(word, translation):
    """Проверяет, что передача в word или translation значений, которые не
    являются строками, вызывает ValueError."""
    anki = Anki()
    with pytest.raises(ValueError) as exc_info:
        anki.add_word(word, translation)
    assert 'должен быть строкой' in str(exc_info.value)
