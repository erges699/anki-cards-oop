import argparse
import pathlib

from anki.anki import Anki
from anki.ui import TextUI
from anki.loader import loader_registry


def get_loader(source):
    """
    Автоматические выбирает конкретную реализацию загрузчика,
    в зависимости от `source`.
    """

    if source.startswith("http"):
        identity = "http"
        args = {"url": source}
    else:
        identity = pathlib.Path(source).suffix
        args = {"file_path": source}

    loader_cls = loader_registry.get_loader(identity)

    return loader_cls(**args)


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
