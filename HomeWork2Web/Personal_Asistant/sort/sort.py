import os
import shutil
import zipfile
from abc import ABC, abstractmethod
from rarfile import RarFile

class ExtensionStrategy(ABC):
    @abstractmethod
    def process_file(self, file_sorter, root, file):
        pass

    @abstractmethod
    def print_results(self, file_sorter):
        pass

class DefaultExtensionStrategy(ExtensionStrategy):
    extensions = {
        'images': ('.jpg', '.png', '.jpeg', '.svg'),
        'videos': ('.avi', '.mp4', '.mov', '.mkv'),
        'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
        'music': ('.mp3', '.ogg', '.wav', '.amr'),
        'archives': ('.zip', '.gz', '.tar', '.rar'),  # Додано підтримку .rar
        'python': ('.py')
    }

    def __init__(self):
        self.unknown_extensions = set()
        self.for_print = {key: [] for key in self.extensions.keys()}

    def process_file(self, file_sorter, root, file):
        filename, extension = os.path.splitext(file)
        found = False
        for folder, exts in self.extensions.items():
            if extension.lower() in exts:
                new_path = os.path.join(root, folder, file_sorter.normalize(file))
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(os.path.join(root, file), new_path)
                found = True
                self.add_and_print_extensions(file_sorter, folder, extension.lower())
                break
        if not found:
            self.add_and_print_extensions(file_sorter, None, extension.lower())

    def add_and_print_extensions(self, file_sorter, folder, extension):
        if folder in file_sorter.for_print:
            if extension not in file_sorter.for_print[folder]:
                file_sorter.for_print[folder].append(extension)
        else:
            file_sorter.unknown_extensions.add(extension)

    def print_results(self, file_sorter):
        print('Знайдені розширення:')
        for folder, extensions in file_sorter.for_print.items():
            if extensions:
                print(f'{folder}: {", ".join(extensions)}')

        print('Невідомі розширення:')
        print(', '.join(file_sorter.unknown_extensions))
        print('Сортування завершено. Вихід у головне меню')

class ZipExtensionStrategy(ExtensionStrategy):
    def process_file(self, file_sorter, root, file):
        filename, extension = os.path.splitext(file)
        if extension.lower() in file_sorter.extensions['archives']:
            file_sorter.for_print['archives'].append(extension.lower())
            self.extract_zip(os.path.join(root, file), os.path.join(root, file_sorter.normalize(filename)))
        elif extension.lower() == '.rar':  # Додано підтримку .rar
            file_sorter.for_print['archives'].append(extension.lower())
            self.extract_rar(os.path.join(root, file), os.path.join(root, file_sorter.normalize(filename)))

    def extract_zip(self, source, destination):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(destination)
        os.remove(source)

    def extract_rar(self, source, destination):
        with RarFile(source, 'r') as rar_ref:
            rar_ref.extractall(destination)
        os.remove(source)

    def normalize(self, name):
        return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()

    def print_results(self, file_sorter):
        pass

class FileSorter:
    def __init__(self, path, extension_strategy=None):
        self.path = path
        self.extension_strategy = extension_strategy or DefaultExtensionStrategy()
        self.unknown_extensions = set()
        self.for_print = {key: [] for key in self.extension_strategy.extensions.keys()}

    def sort_files(self):
        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                if folder.lower() in self.extension_strategy.extensions.keys():
                    dirs.remove(folder)

            for file in files:
                self.extension_strategy.process_file(self, root, file)

    def print_results(self):
        self.extension_strategy.print_results(self)

    def normalize(self, name):
        return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()

def main():
    print('Приклад - C:\Users\Admin\Documents\trash')
    path = input("Шлях до папки ==>")
    sorter = FileSorter(path)
    sorter.sort_files()
    sorter.print_results()

if __name__ == "__main__":
    main()
