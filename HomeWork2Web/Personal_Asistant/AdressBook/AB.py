from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os
import re
import dill as pickle
from dateparser import parse as dateparse
from prompt_toolkit import prompt


from .prompt_tool import Completer, RainbowLetter


class Field(ABC):
    def __init__(self, some_value):
        self._value = self.validate(some_value)

    @property
    def value(self):
        return self._value

    @abstractmethod
    def validate(self, value):
        pass

    def __str__(self):
        return str(self.value)


class NameField(Field):
    def validate(self, value):
        if not value.isalpha():
            raise ValueError("Name should consist of letters only")
        return value


class PhoneField(Field):
    def validate(self, value):
        for i in value:
            if i not in '0123456789+()':
                raise ValueError("Invalid characters in phone number")
        return value


class BirthdayField(Field):
    def validate(self, value):
        obj_datetime = dateparse(value)
        if obj_datetime:
            return obj_datetime.date()
        else:
            raise ValueError('Invalid date format')


class EmailField(Field):
    def validate(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError('Invalid email format')
        return value


class AddressField(Field):
    def validate(self, value):
        valid_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,.")
        if not all(char in valid_characters for char in value):
            raise ValueError("Address should consist of letters, digits, hyphen, comma, and period")
        return value


class Record:
    def __init__(self, name: NameField, phone: PhoneField, birthday: BirthdayField, email: EmailField, address=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, phone):
        phone_number = PhoneField(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def remove_phone(self, phone):
        phone_obj = PhoneField(phone)
        if phone_obj in self.phones:
            self.phones.remove(phone_obj)

    def days_to_birthday(self):
        pass


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        self.data.pop(name, None)

    def dump(self, filename='AddressBook.bin'):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self, filename='AddressBook.bin'):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)


contact_list = AddressBook()


class CommandError(Exception):
    pass


class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        raise NotImplementedError


class AddCommand(Command):
    def execute(self, name, phone, birthday, email, address):
        name = NameField(name)
        phone = PhoneField(phone)
        birthday = BirthdayField(birthday)
        email = EmailField(email)
        address = AddressField(address)
        contacts = Record(name, phone, birthday, email, address)
        contact_list.add_record(contacts)
        return f"Contact {name} has been added."


class DeleteCommand(Command):
    def execute(self, name):
        _, name = name.title()
        contact_list.delete_record(name)
        return f'Contact {name} successfully deleted'


class ChangeCommand(Command):
    def execute(self, name, phone, birthday, email, address):
        name = NameField(name)
        phone = PhoneField(phone)
        birthday = BirthdayField(birthday)
        email = EmailField(email)
        address = AddressField(address)
        update = Record(name, phone, birthday, email, address)
        contact_list.add_record(update)
        return f"Contact {name} has been updated."


class SearchCommand(Command):
    def execute(self, name):
        _, name = name.title()
        result = contact_list.get(name, None)
        if result:
            return result.name.value, result.phones[0].value, str(result.birthday.value), result.email.value, result.address.value
        return "Contact not found."


class ShowAllCommand(Command):
    def execute(self):
        command_show_all()


def command_show_all():
    if not contact_list:
        return "The contact list is empty."
    result = "Contacts:"
    print(result)
    print('------------------------------------------------------------------------------------------------------------------')
    print('Name          |     Number     |     Birthday     |            Email             |             Address           |')
    for name, value in contact_list.items():
        print('--------------|----------------|------------------|------------------------------|-------------------------------|')
        print('{:<14}|{:^16}|{:^18}|{:^30}|{:^30} |'.format(name, value.phones[0].value, str(
            value.birthday.value), value.email.value, value.address.value))
    print('------------------------------------------------------------------------------------------------------------------')


class DaysToBirthdayCommand(Command):
    def execute(self, days):
        _, days = int(days)
        result = command_days_to_birthday(days)
        return result


# @input_error
def command_days_to_birthday(input_str):
    _, days = input_str.split()
    try:
        days = int(days)
        if days <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Invalid number of days")

    result = ''
    today = datetime.now().date()
    for key, value in contact_list.items():
        birthday = value.birthday.value.replace(year=today.year)
        next_birthday = birthday.replace(year=today.year + 1)
        if today <= birthday <= (today + timedelta(days=days)) or today <= next_birthday <= (today + timedelta(days=days)):
            result += f'{key} has a birthday in the next {days} days. ({value.birthday})\n'

    return result.strip() if result else f'No birthdays in the next {days} days'


def main():
    if os.path.exists('AddressBook.bin'):
        contact_list.load()
    print("Available commands: 'hello', 'add', 'change', \
          'delete', 'search', 'birthday', 'show all', 'good bye', 'close', 'exit'")

    while True:
        input_str = prompt("Enter your command: ", completer=Completer, lexer=RainbowLetter())
        command = None

        if input_str == "hello":
            print("How can I help you?")
        elif input_str.startswith("add"):
            command = AddCommand()
        elif input_str.startswith("change"):
            command = ChangeCommand()
        elif input_str.startswith("delete "):
            command = DeleteCommand()
        elif input_str.startswith("search "):
            command = SearchCommand()
        elif input_str.startswith("birthday "):
            command = DaysToBirthdayCommand()
        elif input_str == "show all":
            command = ShowAllCommand()
        elif input_str in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Available commands: 'hello',\
                   'add', 'change', 'delete', 'search', 'birthday', 'show all', 'good bye', 'close', 'exit'")

        if command:
            try:
                result = command.execute(*input_str.split())
                print(result)
                contact_list.dump()
            except CommandError as e:
                print(e)


if __name__ == "__main__":
    main()



