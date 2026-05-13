import csv
import random
import sys
import time
from typing import Dict, Tuple


STOP_WORD = 'СТОП'


def load_words(filename: str = 'words.txt') -> Dict[str, str]:
    """
    Загружает пары слов («слово, перевод») из текстового файла
    и возвращает словарь.

    Args:
        filename (str): Имя файла для загрузки данных.
            По умолчанию 'words.txt'.

    Returns:
        Dict[str, str]: Словарь, где ключ — исходное слово,
        значение — перевод.

    Raises:
        SystemExit: Если файл не найден, выводит сообщение об ошибке
        и завершает программу с кодом 1.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
        sys.exit(1)

    result = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Игнорируем строки без запятой или с лишними запятыми
        if line.count(',') != 1:
            continue
        word, translation = line.split(',', 1)
        result[word] = translation
    return result


def print_statistics(score: int, total_time: float) -> None:
    """
    Выводит статистику игры: итоговый счет и время.

    Args:
        score (int): Количество правильных ответов.
        total_time (float): Общее время игры в секундах.
    """
    print(f'Ваш итоговый счет: {score}')
    if score > 0:
        avg_time = total_time / score
        print(f'Время игры: {total_time:.2f} секунд '
              f'(среднее время: {avg_time:.2f} сек.)')
    else:
        print(f'Время игры: {total_time:.2f} секунд (среднее время: —)')


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Спрашивает у пользователя перевод заданного слова,
    возвращает необходимость выхода, правильность ответа и время.

    Args:
        word (str): слово, перевод которого нужно ввести пользователю.
        correct (str): правильный перевод слова.

    Returns:
        Tuple[bool, bool, float]: флаг выхода, флаг правильности,
        время ответа в секундах.
    """
    print(f'Введите перевод слова "{word}":')
    start_time = time.time()
    answer = input("").strip()
    end_time = time.time()

    if answer.upper() == STOP_WORD:
        return (True, False, 0.0)

    answer_time = end_time - start_time
    is_correct = answer.lower().strip() == correct.lower().strip()
    return (False, is_correct, answer_time)


def start_game(words: Dict[str, str]) -> None:
    """
    Запускает обычную игру (тренировку) по словам.

    Args:
        words (Dict[str, str]): Словарь слов для тренировки.
    """
    if not words:
        print('Словарь пуст. Добавьте слова через меню.')
        return

    score = 0
    total_time = 0.0

    print('Игра началась! Для завершения введите СТОП.')

    while True:
        word = random.choice(list(words.keys()))
        correct_translation = words[word]

        result = ask_and_check(word, correct_translation)
        is_stop, is_correct, answer_time = result

        if is_stop:
            print('Игра завершена.')
            break

        total_time += answer_time

        if is_correct:
            score += 1
            print(f'Верно! Время на ответ: {answer_time:.2f} сек.')
        else:
            print(f'Неверно. Правильный перевод: {correct_translation}. '
                  f'Время на ответ: {answer_time:.2f} сек.')

    print_statistics(score, total_time)


def train_until_mistake(words: Dict[str, str]) -> None:
    """
    Запускает игровой режим «до первой ошибки»: пользователь переводит
    случайные слова из словаря, игра завершается после первой ошибки
    или при вводе завершающего слова.

    Args:
        words (Dict[str, str]): Словарь, в котором ключ — слово,
        а значение — его перевод.
    """
    if not words:
        print('Словарь пуст. Добавьте слова через меню.')
        return

    print('Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП.')

    score = 0
    total_time = 0.0
    word_list = list(words.keys())

    while True:
        word = random.choice(word_list)
        correct_translation = words[word]

        result = ask_and_check(word, correct_translation)
        is_stop, is_correct, answer_time = result

        if is_stop:
            print('Выход из режима по запросу пользователя.')
            break

        total_time += answer_time

        if is_correct:
            score += 1
            print(f'Верно! Ваш счет: {score}. '
                  f'Время на ответ: {answer_time:.2f} сек.')
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct_translation}.')
            break

    print_statistics(score, total_time)


def add_words(words: Dict[str, str]) -> None:
    """
    Добавляет новые слова в словарь.

    Args:
        words (Dict[str, str]): Текущий словарь слов (будет изменен).
    """
    print('Для завершения ввода введите служебное слово — СТОП.')
    while True:
        word_input = input('Введите слово: ').strip()
        if word_input.upper() == STOP_WORD:
            break
        translation_input = input('Введите перевод: ').strip()
        if translation_input.upper() == STOP_WORD:
            break
        words[word_input] = translation_input
        print(f'Добавлена пара: {word_input} - {translation_input}')


def show_all_words(words: Dict[str, str]) -> None:
    """
    Выводит все пары «слово — перевод» из словаря в одну строку.

    Формат вывода: слово - перевод; слово - перевод; ...

    Args:
        words (Dict[str, str]): Словарь слов для отображения.

    Returns:
        None
    """
    pairs = [f'{word} - {translation}' for word, translation in words.items()]
    output = '; '.join(pairs)
    print(output)


def save_words(words: Dict[str, str], filename: str) -> None:
    """
    Сохраняет словарь в файл.

    Args:
        words (Dict[str, str]): Словарь для сохранения.
        filename (str): Имя файла.

    Raises:
        OSError: Если произошла ошибка при записи в файл.
    """
    if not words:
        print(f'Словарь пуст, файл {filename} не будет создан.')
        return

    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for word, translation in words.items():
                writer.writerow([word, translation])
    except OSError as e:
        print(f'Ошибка при сохранении файла {filename}: {e}')
        raise

    count = len(words)
    last_digit = count % 10
    if last_digit == 1:
        word_form = 'слово'
    elif last_digit in (2, 3, 4):
        word_form = 'слова'
    else:
        word_form = 'слов'
    print(f'Было сохранено {count} {word_form} в файл {filename}')


def main() -> None:
    """
    Главное меню программы-тренажёра для изучения слов.
    Загружает словарь, выводит количество загруженных слов,
    предоставляет меню выбора режимов и обеспечивает взаимодействие
    с пользователем.
    """
    filename = 'words.txt'
    words = load_words()
    count = len(words)
    last_digit = count % 10
    if last_digit == 1:
        word_form = 'слово'
    elif last_digit in (2, 3, 4):
        word_form = 'слова'
    else:
        word_form = 'слов'
    print(f'Было загружено {count} {word_form} из файла {filename}')

    while True:
        menu = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''
        print(menu)
        menu_choice = input('Пункт меню: ')

        if menu_choice == '1':
            start_game(words)
        elif menu_choice == '2':
            add_words(words)
        elif menu_choice == '3':
            train_until_mistake(words)
        elif menu_choice == '4':
            show_all_words(words)
        elif menu_choice == '5':
            save_words(words, filename)
            sys.exit()
        else:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()
