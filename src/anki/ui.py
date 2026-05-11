from textwrap import dedent


class TextUI():
    STOP_WORD = "стоп"
    
    MENU = dedent("""
        ========================================
                    КАРТЫ ANKI
        ========================================

        1. Начать игру
        2. Добавить слова
        3. Вывод всех слов
        4. Тренировка до первой ошибки
        5. Выйти

        Выберите действие (1-5):
    """).strip()
    
    def __init__(self, anki_game):
        """
        Инициализатор класса TextUI.
        
        Параметры:
            anki_game (Anki): экземпляр класса Anki.
        """
        if anki_game is None:
            raise ValueError("Аргумент anki_game обязателен")
        self._anki_game = anki_game

    def start_game(self):
        """
        Обрабатывает пункт меню «Начать игру».
        """
        print(f"\nДля завершения игры введите '{self.STOP_WORD}'.")
        while True:
            try:
                word = self._anki_game.get_random_word()
            except ValueError:
                print("Словарь пуст. Добавьте слова для начала игры.")
                break
            
            print(f"\nСлово: {word}")
            user_input = input("Введите перевод: ").strip()
            
            if user_input.lower() == self.STOP_WORD:
                print("Игра завершена.")
                break
            
            if self._anki_game.check_translation(word, user_input):
                print("Правильно! Молодец!")
            else:
                correct = self._anki_game.get_translation(word)
                print(f"Неправильно. Правильный перевод: {correct}")

    def add_words(self):
        """
        Обрабатывает пункт меню «Добавить слова».
        """
        print(f"\nДля завершения ввода введите '{self.STOP_WORD}' "
              "вместо слова.")
        while True:
            prompt = "\nВведите слово (или 'стоп' для завершения): "
            word = input(prompt).strip()
            if word.lower() == self.STOP_WORD:
                print("Добавление слов завершено.")
                break
            
            translation = input("Введите перевод: ").strip()
            if translation.lower() == self.STOP_WORD:
                print("Добавление слов завершено.")
                break
            
            try:
                self._anki_game.add_word(word, translation)
                print(f"Слово '{word}' с переводом '{translation}' добавлено.")
            except ValueError as e:
                print(f"Ошибка: {e}")

    def show_words(self):
        """
        Обрабатывает пункт меню «Вывод всех слов».
        """
        words = self._anki_game.get_words()
        if not words:
            print("\nСловарь пуст.")
            return
        
        print("\nСловарь:")
        for word, translation in words.items():
            print(f"{word} - {translation}")

    def main_loop(self):
        """
        Отрисовывает меню пользовательского интерфейса и обрабатывает ввод.
        """
        while True:
            print(self.MENU)
            choice = input("> ").strip()
            
            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.add_words()
            elif choice == "3":
                self.show_words()
            elif choice == "4":
                print("\nДанная функциональность ещё не реализована")
            elif choice == "5":
                print("\nВыход из программы.")
                break
            else:
                print("\nНеверный выбор. Пожалуйста, введите число от 1 до 5.")
