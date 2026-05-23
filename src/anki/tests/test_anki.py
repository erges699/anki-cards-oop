import pytest

from anki.anki import Anki


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


@pytest.mark.parametrize('invalid_input', [
    42,
    "not a dict",
    [],
    set(),
])
def test_anki_init_raises_ValueError_on_invalid_input(invalid_input):
    """Проверьте, что передача в параметр words значений,
    которые не являются словарём, вызывает ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Anki(words=invalid_input)
    assert 'быть словарём' in str(exc_info.value)


@pytest.mark.parametrize('word, translation', [
    (42, "valid"),
    ("valid", 42),
    ([], "valid"),
    ("valid", []),
    (None, "valid"),
    ("valid", None),
])
def test_anki_add_word_raises_ValueError_on_invalid_input(word, translation):
    """
    Проверьте, что передача в word или translation значений,
    которые не являются строками, вызывает ValueError."""
    anki = Anki()
    with pytest.raises(ValueError) as exc_info:
        anki.add_word(word, translation)
    assert 'быть строкой' in str(exc_info.value)
