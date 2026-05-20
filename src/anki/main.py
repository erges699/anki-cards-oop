from __future__ import annotations

import argparse
import contextlib
import pathlib
from typing import Dict, Union, Iterator

from anki.anki import Anki
from anki.ui import TextUI
from anki.loader import loader_registry, BaseFileLoader, JsonNetworkLoader


@contextlib.contextmanager
def game_context(
    loader: Union[BaseFileLoader, JsonNetworkLoader],
    anki: Anki,
) -> Iterator[Anki]:
    """
    Контекстный менеджер для управления жизненным циклом игры.

    Принимает экземпляр загрузчика и экземпляр игры Anki.
    В __enter__ загружает слова и добавляет их в экземпляр Anki.
    В __exit__ сохраняет слова через вызов save_words загрузчика.
    Гарантирует сохранение слов даже при возникновении ошибок.

    Parameters
    ----------
    loader : BaseFileLoader or HttpLoader
        Загрузчик для загрузки и сохранения слов.
    anki : Anki
        Экземпляр игры Anki.

    Yields
    ------
    Anki
        Экземпляр игры Anki с загруженными словами.
    """
    try:
        # Загружаем слова из источника
        loaded_words = loader.load_words()
        # Добавляем загруженные слова в экземпляр Anki
        # (объединяем с существующими словами, чтобы не потерять их)
        current_words = anki.words
        current_words.update(loaded_words)
        anki.words = current_words
        yield anki
    finally:
        # Сохраняем слова, даже если произошла ошибка
        loader.save_words(anki.words)


def get_loader(source: str) -> Union[BaseFileLoader, JsonNetworkLoader]:
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


def main() -> None:
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

    # Создаём экземпляр Anki без слов,
    # слова будут загружены в контекстном менеджере
    anki = Anki()

    with game_context(loader, anki):
        ui = TextUI(anki)
        ui.main_loop()


if __name__ == "__main__":
    main()
