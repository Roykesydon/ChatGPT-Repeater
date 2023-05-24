import os
from datetime import datetime
from typing import List

from natsort import natsorted

from data_handler.JsonHandler import JsonHandler

"""
存取切割好的 paper 資料
"""


class PaperHandler:
    def __init__(self, config: dict):
        self._config = config

    def get_sub_directories(self, folder_path: str) -> List[str]:
        sub_directories = []

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                sub_directories.append(item_path)

        return sub_directories

    def _read_parts(self, folder_path: str) -> List[str]:
        """
        把資料夾中 part 開頭，.txt 結尾的檔案讀取出來，以 list 存取，並按照數字檔名把內容排序
        e.g.: ["part1.txt 的內容", "part2.txt 的內容", "part3.txt 的內容", "part10.txt 的內容"]
        """
        parts = []
        files = [
            item
            for item in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, item))
            and item.startswith("part")
            and item.endswith(".txt")
        ]

        sorted_files = natsorted(files, key=lambda x: x.lower())

        for file_name in sorted_files:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                parts.append(content)

        return parts

    def get_paper_data(self, folder_path: str) -> dict:
        """
        回傳論文資料夾中的資料
        """
        json_handler = JsonHandler()
        metadata = json_handler.return_json_as_dict(
            json_path=os.path.join(folder_path, "meta.json")
        )

        parts = self._read_parts(folder_path)
        folder_name = os.path.basename(folder_path)
        return {"metadata": metadata, "parts": parts, "folder_name": folder_name}

    def create_all_result_folder(self) -> str:
        """
        根據當下時間建立存放所有 paper 的 output 的資料夾
        """
        output_folder = self._config["output_folder"]

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder_path = os.path.join(output_folder, current_time)

        os.makedirs(output_folder_path)

        return output_folder_path

    def create_paper_result_folder(
        self, output_folder_path: str, paper_data: dict
    ) -> str:
        """
        建立 paper 資料夾
        """
        paper_path = os.path.join(output_folder_path, paper_data["folder_name"])
        os.makedirs(paper_path)
        return paper_path

    def save_response(
        self, result: dict, output_paper_path: str, part_index: int
    ) -> None:
        """
        儲存論文資訊，part_index 是 1-based
        """

        # 儲存 api 回傳結果
        result_json_path = os.path.join(output_paper_path, f"output_{part_index}.json")
        json_handler = JsonHandler()
        json_handler.save_json(json_path=result_json_path, data=result)

    def save_meta_data(self, output_paper_path: str, meta_data: dict) -> None:
        meta_data_path = os.path.join(output_paper_path, "meta.json")
        json_handler = JsonHandler()
        json_handler.save_json(json_path=meta_data_path, data=meta_data)
