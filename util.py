import json


def read_config(key):
    """read config file by key and return values
    """
    try:
        with open("./config.json", "r") as f:
            data = f.read()
            config = json.loads(data)
        return config[key]
    except Exception('Unable to load config using key: "{}"'.format(key)):
        return None
