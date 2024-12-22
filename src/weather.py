import json

from src.api.accuweather_api import AccuWeatherAPI



class Weather:
    def __init__(self):
        self.cached_data = {}
        self.data_path = "data/"

        self.api = AccuWeatherAPI()

        self.load_cached_data("weather.json")
    
    def load_cached_data(self, file_name: str):
        file_path = self.data_path + file_name

        with open(file_path, 'r') as file:
            data: dict = json.load(file)
            for index, value in data.items():
                if index not in self.cached_data.keys():
                    self.cached_data[index] = value

    def write_cached_data(self, file_name: str):
        file_path = self.data_path + file_name
        with open(file_path, 'w') as file:
            json.dump(self.cached_data, file)

    def get_weather(self, city_name: str):
        city_name = city_name.lower().strip()
        
        response_data = self.api.get_weather(city_name)

        response_data_temperature = response_data.get("DailyForecasts", [])

        weather_days = []
        for day in response_data_temperature:
            weather_data = {
                "temperature_max": day["Temperature"]["Maximum"]["Value"],
                "temperature_min": day["Temperature"]["Minimum"]["Value"],
                "date": day.get("Date"),
            }
            weather_data["temperature_avg"] = (weather_data["temperature_max"] + weather_data["temperature_min"]) / 2
            weather_days.append(weather_data)

        self.cached_data[city_name] = weather_days
        self.write_cached_data("weather.json") # аккуратнее с кол-вом запросов

        return weather_days
