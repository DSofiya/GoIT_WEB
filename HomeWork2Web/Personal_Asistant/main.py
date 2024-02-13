from abc import ABC, abstractmethod

class MenuItem(ABC):
    @abstractmethod
    def run(self):
        pass

class AddressBookMenuItem(MenuItem):
    def run(self):
        from AdressBook.AB import main as ab_main
        ab_main()

class NoteBookMenuItem(MenuItem):
    def run(self):
        from NoteBook.NB import main as noteb_main
        noteb_main()

class MapMenuItem(MenuItem):
    def run(self):
        from Map.Map import main as map_main
        map_main()

class SortMenuItem(MenuItem):
    def run(self):
        from sort.sort import main as sort_main
        sort_main()

class GameMenuItem(MenuItem):
    def run(self):
        from Game.game import main as game_main
        game_main()

def menu():
    menu_items = {
        '1': AddressBookMenuItem(),
        '2': NoteBookMenuItem(),
        '3': MapMenuItem(),
        '4': SortMenuItem(),
        '5': GameMenuItem(),
        '0': None  # To exit
    }

    while True:
        print('MENU')
        choice = input(
            'Вітаю, я ваш персональний помічник.\n Оберіть функцію:\n1. Записна книжка\n2. Нотатник\n3. Карта\n4. Сортування папки\n5. Гра\n0. Вихід\n>>>')
        
        if choice in menu_items:
            if choice == '0':
                break
            menu_items[choice].run()
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == '__main__':
    menu()
