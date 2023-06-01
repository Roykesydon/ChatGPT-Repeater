from typing import List
import csv

class CsvHandler:
    def __init__(self):
        pass

    def save_csv(self, csv_path: str, data: list, title: List[str]) -> None:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["question", "answer", "title", "filename"])
            writer.writerows(data)
