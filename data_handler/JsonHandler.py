import json


class JsonHandler:
    def __init__(self):
        pass

    def return_json_as_dict(self, json_path: str) -> dict:
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def save_json(self, json_path: str, data: dict) -> None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
