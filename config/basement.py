from dataclasses import dataclass
from dotenv import load_dotenv
import os


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


class EnvFileNotFound(Exception):
    def __init__(self, file_name: str, *args, **kwargs):
        self.file_name = file_name
        self.message = f'Env file "{file_name}" must be in env dir'
        super().__init__(self.message, *args, **kwargs)


def getenv(var_name: str, cast_to=str) -> str:
    try:
        value = os.environ[var_name]
        return cast_to(value)
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"The value {value} can't be cast to {cast_to}.")



@dataclass
class Api:
    api_key: str
    location_url: str
    weather_url: str


@dataclass
class Config:
    api: Api


def load_config() -> Config:
    load_dotenv()

    return Config(
        api=Api(
        api_key=getenv("API_KEY"),
            location_url=getenv("LOCATION_URL"),
            weather_url=getenv("WEATHER_URL"),
        ),
    )


config: Config = load_config()
