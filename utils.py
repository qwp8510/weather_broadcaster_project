import json


def get_json_content(path):
    with open(path, 'r') as js:
        content = json.load(js)
        js.close()
    return content
