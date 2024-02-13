import folium
import requests
import os
import re
from prompt_toolkit import prompt
from abc import ABC, abstractmethod


from .prompt_tool import RainbowLetter,Completer


class MapBuilder(ABC):
    @abstractmethod
    def build_map(self):
        pass

class RussiaMapBuilder(MapBuilder):
    def build_map(self):
        return folium.Map(location=[55.7558, 37.6176], zoom_start=5)

class MarkerFactory:
    def create_marker(self, lat, lon):
        return folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(icon_size=(12, 12),
                html='<div style="background-color: red; width: 12px; height: 12px;"></div>'),
            tooltip=f'Координати: {lat}, {lon}')

class MapSaver:
    def save_map(self, map_obj, map_name):
        map_obj.save(map_name)
        return map_name

class FileValidator:
    def validate_file(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                coordinates = line.strip().split(',')
                if len(coordinates) != 2:
                    raise ValueError("Файл має містити координати,що складаються з двох чисел, \
                                     розділені комою. Наприклад: 55.7558,37.6176")


def get_coordinates(city_name):
    api_key = "5cef6f4446b24817a8ebc8c727403c0a" 
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = { "q": city_name, "key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get("results") and data["results"][0]["geometry"]:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        return lat, lng
    else:
        raise ValueError(f"Не вдалося знайти координати для міста {city_name}")

class CoordinatesValidator:
    def validate_coordinates(self, coordinates):
        pattern = r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$'
        if re.match(pattern, coordinates):
            return True
        else:
            raise ValueError(f"Координати {coordinates} мають неправильний формат.")

class CoordinatesFileManager:
    def read_coordinates(self, file_name):
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def write_coordinates(self, file_name, coordinates):
        with open(file_name, 'a') as file:
            file.write('\n' + coordinates)

class MapDirector:
    def __init__(self, map_builder, marker_factory, map_saver):
        self.map_builder = map_builder
        self.marker_factory = marker_factory
        self.map_saver = map_saver

    def build_and_save_map(self, file_name, map_name):
        russia_map = self.map_builder.build_map()
        file_validator = FileValidator()
        coordinates_validator = CoordinatesValidator()
        coordinates_file_manager = CoordinatesFileManager()

        for line in coordinates_file_manager.read_coordinates(file_name):
            lat, lon = line.split(',')
            coordinates_validator.validate_coordinates(line)
            marker = self.marker_factory.create_marker(float(lat), float(lon))
            marker.add_to(russia_map)

        self.map_saver.save_map(russia_map, map_name)
        return map_name

def main():
    map_builder = RussiaMapBuilder()
    marker_factory = MarkerFactory()
    map_saver = MapSaver()
    map_director = MapDirector(map_builder, marker_factory, map_saver)
    current_directory = os.getcwd()
 
    print("Вітаю. Доступні команди:")
    print("Зберегти карту ядерних обєктів країни 404 - 'save_nuclear'")
    print("Додати кординати до файлу з ядерними обєктами -'add_nuclear'")
    print("Зберегти карту аеропортів країни 404 - 'save_air'")
    print("Додати кординати до файлу з аеропортами -'add_air'")
    print("Зберегти карту адміністративних обєктів країни 404 - 'save_admin'")
    print("Додати кординати до файлу з ядерними обєктами -'add_admin'")
    print("Отримати кординати за назвою міста -'coordinates'")
    print("Вийти - 'good bye','close','exit'") 
    
    while True:
      

        input_str = prompt("Enter your command: ", completer=Completer, lexer=RainbowLetter())

        if  input_str.startswith("save_nuclear"):
            try:
                result =map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_nuclear.txt",
                                                        'russia_map_nuclear.html')
                print(f"Карта з  прапорцями збережена у файлі {result}.") 
            except Exception as e:
                print(f"Помилка: {str(e)}")  

        elif input_str.startswith("save_air"):
            try:
                result = map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_air.txt",
                                                         'russia_map_air.html')
                print(f"Карта з  прапорцями збережена у файлі {result}.")
            except Exception as e:
                print(f"Помилка: {str(e)}") 
        elif input_str.startswith("save_admin"):
            try:
                result =map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_admin.txt",
                                                        'russia_map_admin.html')
                print(f"Карта з  прапорцями збережена у файлі {result}.") 
            except Exception as e:
                print(f"Помилка: {str(e)}")   
        elif input_str == "add_nuclear":
            try:
                input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
                print(map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_nuclear.txt", 
                                                      input_str))
            except Exception as e:
                print(f"Помилка: {str(e)}") 
        elif input_str == "add_air":
            try:
                input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
                print(map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_air.txt", 
                                                      input_str))
            except Exception as e:
                print(f"Помилка: {str(e)}") 
        elif input_str == "add_admin":
            try:
                input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
                print(map_director.build_and_save_map(f"{current_directory}\Personal_assistant\Map\coordinates_admin.txt",
                                                       input_str))
            except Exception as e:
                print(f"Помилка: {str(e)}") 
        elif input_str == "coordinates":
            input_str = input("Приклад: Москва. Введіть назву міста:")
            print(get_coordinates(input_str)) 
        
        elif input_str in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невірно введена команда. Доступні команди:")
            print("Зберегти карту ядерних обєктів країни 404 - 'save_nuclear'")
            print("Додати кординати до файлу з ядерними обєктами -'add_nuclear'")
            print("Зберегти карту аеропортів країни 404 - 'save_air'")
            print("Додати кординати до файлу з аеропортами -'add_air'")
            print("Зберегти карту адміністративних обєктів країни 404 - 'save_admin'")
            print("Додати кординати до файлу з ядерними обєктами -'add_admin'")
            print("Отримати кординати за назвою міста -'coordinates'")
            print("Вийти - 'good bye','close','exit'") 



if __name__ == "__main__":
    main()