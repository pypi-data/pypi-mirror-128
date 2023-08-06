import configparser
from pathlib import Path

configFile = str(Path.home()) + "/.euphoria.cfg"


def make_config_file():
    config = configparser.ConfigParser()
    config["settings"] = {
        "one_address": "",
    }
    with open(configFile, "w") as conf:
        config.write(conf)


def is_config_present():
    return Path(configFile).is_file()


def read_config():
    config = configparser.ConfigParser()
    config.read(configFile)
    return config["settings"]["one_address"]


def save_to_config(addr):
    config = configparser.ConfigParser()
    config["settings"] = {
        "one_address": addr,
    }
    with open(configFile, "w") as conf:
        config.write(conf)
