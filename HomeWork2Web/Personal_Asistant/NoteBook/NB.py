import json
import os
from datetime import datetime
from .promp_ut import Completer, RainbowLexer, Sort_Completer
from prompt_toolkit import prompt
from colorama import Fore

class InputError(Exception):
    pass

class Note:
    def __init__(self, title, content, tags=None, created_at=None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = created_at

class NoteManagerBuilder:
    def __init__(self, storage_path):
        self.note_manager = NoteManager(storage_path)

    def build(self):
        self.note_manager.upload_notes()
        return self.note_manager

    def add_note_command(self, title, content, tags=None):
        self.note_manager.add_note(title, content, tags)
        self.note_manager.save_notes()
        print(Fore.GREEN + "Note added!")

    def edit_note_command(self, index, title, content, tags=None):
        self.note_manager.edit_note(index, title, content, tags)
        self.note_manager.save_notes()
        print(Fore.GREEN + "Note edited!")

    def delete_note_command(self, index):
        note = self.note_manager.notes[index]
        self.note_manager.display_note(index, note)
        to_delete = input("Delete? Press 'Y'+'Enter' -> Yes; Press 'Enter' -> No >>")
        if to_delete.lower() == 'y':
            self.note_manager.delete_note(index)
            self.note_manager.save_notes()
            print(Fore.GREEN + "Note deleted!")

    def search_tag_command(self, tag):
        matching_notes = self.note_manager.search_notes_by_tag(tag)
        if matching_notes:
            for i, note in enumerate(matching_notes):
                self.note_manager.display_note(i, note)
        else:
            print(Fore.GREEN + "No notes found with this tag.")

    def search_content_command(self, keyword):
        matching_notes = self.note_manager.search_notes_by_content(keyword)
        if matching_notes:
            for i, note in enumerate(matching_notes):
                self.note_manager.display_note(i, note)
        else:
            print(Fore.GREEN + "No notes found with this keyword.")

    def sort_notes_command(self, sort_choice):
        if sort_choice == "Sort by name":
            sorted_notes = self.note_manager.sort_notes(by_name=True)
        elif sort_choice == "Sort by tags":
            sorted_notes = self.note_manager.sort_notes(by_tags=True)
        elif sort_choice == "Sort by date":
            sorted_notes = self.note_manager.sort_notes(by_created_date=True)
        else:
            print("Невірний вибір сортування")
            return

        if sorted_notes:
            for i, note in enumerate(sorted_notes):
                self.note_manager.display_note(i, note)

class NoteManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.notes = []

    def upload_notes(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as file:
                data = json.load(file)
                self.notes = [Note(**note_data) for note_data in data]

    def save_notes(self):
        with open(self.storage_path, 'w') as file:
            data = [note.__dict__ for note in self.notes]
            json.dump(data, file, indent=4)

    def add_note(self, title, content, tags=None):
        note = Note(title, content, tags, created_at=datetime.now().strftime('%Y-%m-%d %H:%M'))
        self.notes.append(note)

    def edit_note(self, note_index, title, content, tags=None):
        note = self.notes[note_index]
        note.title = title
        note.content = content
        note.tags = tags or []
        note.created_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    def delete_note(self, note_index):
        del self.notes[note_index]

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag.lower() in [t.lower() for t in note.tags]]

    def search_notes_by_content(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower()]

    def display_note(self, index, note):
        print(f"Note {index + 1}:")
        print(f"Title: {note.title.upper()}")
        print(f"Content: {note.content}")
        print(f"Tags: {', '.join(note.tags)}")
        print(f"Created At: {note.created_at}")

    def display_notes(self):
        for i, note in enumerate(self.notes):
            print(f"Note {i + 1}:")
            print(f"Title: {note.title.upper()}")
            print(f"Content: {note.content}")
            print(f"Tags: {', '.join(note.tags)}")
            print(f"Created At: {note.created_at}")
            print("-" * 30)

    def sort_notes(self, by_name=False, by_tags=False, by_created_date=False):
        if by_name:
            sorted_notes = sorted(self.notes, key=lambda x: x.title)
        elif by_tags:
            sorted_notes = sorted(self.notes, key=lambda x: x.tags)
        elif by_created_date:
            sorted_notes = sorted(self.notes, key=lambda x: x.created_at)
        else:
            return None
        return sorted_notes

def main():
    storage_path = 'notes.json'
    builder = NoteManagerBuilder(storage_path)
    note_manager = builder.build()
    
    print("Доступні команди:'add_note','edit_note','delete_note', 'search_tag', 'search_content', 'display_notes','sort','exit'")
    
    while True:
        choice = prompt('Enter your command: ', completer=Completer, lexer=RainbowLexer())
       
        if choice == 'add_note':
            title = prompt("Enter title: ", lexer=RainbowLexer())
            content = prompt("Enter note: ", lexer=RainbowLexer())
            input_tags = prompt("Enter tags (comma-separated): ", lexer=RainbowLexer())
            tags = [tag.strip() for tag in input_tags.split(',') if tag.strip()]
            builder.add_note_command(title, content, tags)
        elif choice == 'edit_note':
            builder.edit_note_command()
        elif choice == 'delete_note':
            builder.delete_note_command()
        elif choice == 'search_tag':
            tag = prompt("Enter tag to search for: ", lexer=RainbowLexer())
            builder.search_tag_command(tag)
        elif choice == 'search_content':
            keyword = prompt("Enter keyword to search for: ", lexer=RainbowLexer())
            builder.search_content_command(keyword)
        elif choice == 'display_notes':
            note_manager.display_notes()
        elif choice == "sort":
            sort_choice = prompt('Enter sort type: ', completer=Sort_Completer, lexer=RainbowLexer())
            builder.sort_notes_command(sort_choice)
        elif choice == 'exit':
            print("Good bye!")
            break

            

if __name__ == "__main__":
    init(autoreset=True)
    main()

