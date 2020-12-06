import json


def get_json_content(path):
    with open(path, 'r') as js:
        content = json.load(js)
        js.close()
    return content


def trans_temp_kelvin_to_Celsius(temp):
    return int(temp - 273.15)
