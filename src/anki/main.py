import argparse
import pathlib

from anki.anki import Anki
from anki.loader import (
    TextFileLoader,
    TSVFileLoader,
    JsonFileLoader,
    JsonNetworkLoader,
)
from anki.ui import TextUI


def get_loader(source):
    """Выбирает реализацию загрузчика в зависимости от `source`.

    Parameters
    ----------
    source : str
        Источник для получения слов, файл или URL.

    Returns
    -------
    Any
        Экземпляр загрузчика.
    """
    # Проверяем, является ли source URL
    if source.startswith(('http://', 'https://')):
        return JsonNetworkLoader(url=source)

    loaders = {
        ".txt": TextFileLoader,
        ".tsv": TSVFileLoader,
        ".json": JsonFileLoader
    }

    file_path = pathlib.Path(source)

    try:
        # suffix возвращает расширение файла
        loader = loaders[file_path.suffix]
        return loader(file_path=str(file_path))
    except KeyError:
        raise ValueError(f"Неизвестный тип источника слов: {source}")


def main():
    # Создали объект парсера аргументов командной строки.
    parser = argparse.ArgumentParser(prog="anki")

    # Добавили новый аргумент.
    parser.add_argument(
        "--source", default="./words.txt",
        help="Путь до источника со словами (файл или URL)",
        metavar="SOURCE_PATH",
    )

    # Распарсили аргументы командной строки.
    args = parser.parse_args()

    loader = get_loader(args.source)

    anki = Anki(words=loader.load_words())

    ui = TextUI(anki)
    ui.main_loop()
    loader.save_words(anki.words)


if __name__ == "__main__":
    main()
