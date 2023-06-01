import argparse

import os
import re

from data_handler.JsonHandler import JsonHandler
from data_handler.TaskHandler import TaskHandler
from data_handler.CsvHandler import CsvHandler

from post_process_scripts.PostProcessInterface import PostProcessInterface

class AgricultureQA(PostProcessInterface):
    def __init__(self, args: dict) -> None:
        super().__init__()
        self.result_folder_name = args["--result_folder_name"]
        

    def _filter_row_by_question(self, row_data: list) -> list:
        ban_keywords = ['研究', '本文', '上文', '內文']
        filtered_row_data = []

        for row in row_data:
            question = row[0]
            if not any(keyword in question for keyword in ban_keywords):
                filtered_row_data.append(row)

        return filtered_row_data

    def run(self):
        """
        把回傳結果轉為 CSV
        """
        result_folder_name = self.result_folder_name

        # 初始化
        json_handler = JsonHandler()
        config = json_handler.return_json_as_dict(json_path="./config.json")
        task_handler = TaskHandler(config=config)
        all_row_list = []  # 存放資料集每一 row 的 list

        # 取得資料夾中的所有資料夾
        result_path = os.path.join(config["output_folder"], result_folder_name)
        subdirectories = task_handler.get_sub_directories(result_path)
        for subdirectory in subdirectories:
            # 讀取 meta.json
            meta_json_path = os.path.join(subdirectory, "meta.json")
            meta_data = json_handler.return_json_as_dict(json_path=meta_json_path)

            # 遍歷所有的 output 開頭的 json 檔案
            for item in os.listdir(subdirectory):
                if item.startswith("output") and item.endswith(".json"):
                    json_path = os.path.join(subdirectory, item)
                    response_data = json_handler.return_json_as_dict(json_path=json_path)

                    completion = response_data["choices"][0]["message"]["content"]

                    # 把 completion 的每組問題和答案切出來
                    qa_list = re.split(r"問題(?:\d+)|问题(?:\d+)", completion)
                    qa_list = [p for p in qa_list if p]

                    # 如果 耗費的總 token 數量大於等於 max_context_tokens_length
                    # 代表很有可能最後一個問答回答不完整，這裡直接放棄
                    if (
                        response_data["usage"]["total_tokens"]
                        >= config["max_context_tokens_length"]
                    ):
                        qa_list = qa_list[:-1]

                    # 對於小於等於 2 組問答的資料，會被視作出錯而放棄，因為可能真的是有某種未考慮因素導致問答無法被正常切割
                    if len(qa_list) <= 2:
                        print(f"{meta_data['filename']}-{item} 發生錯誤，無法分出 3 組以上的問答")
                        continue

                    # 把問題和答案分開，並對格式進行簡單處理
                    row_list = []
                    for qa in qa_list:
                        split_qa = re.split(r"答案(?:\d+)", qa)
                        split_qa = [p for p in split_qa if p]

                        if len(split_qa) >= 2:
                            split_qa = [split_qa[0], "".join(split_qa[1:])]
                            split_qa[0] = split_qa[0].lstrip("0123456789：:").strip()
                            split_qa[1] = split_qa[1].lstrip("0123456789：:").strip()

                        if len(split_qa) != 2:
                            print(f"{meta_data['filename']}-{item} 發生錯誤，無法切成一問一答")
                            continue

                        row = split_qa + [meta_data["title"], meta_data["filename"]]
                        row_list.append(tuple(row))

                    all_row_list += row_list

        # 把原始問答資料寫入 csv
        csv_handler = CsvHandler()

        csv_path = os.path.join(config["output_folder"], f"raw_result_{result_folder_name}.csv")
        csv_handler.save_csv(csv_path=csv_path, data=all_row_list, title=["question", "answer", "title", "filename"])

        print(f"已生成 {csv_path}")

        filtered_row_list = self._filter_row_by_question(all_row_list)
        csv_path = os.path.join(config["output_folder"], f"filtered_result_{result_folder_name}.csv")
        csv_handler.save_csv(csv_path=csv_path, data=filtered_row_list, title=["question", "answer", "title", "filename"])
        print(f"已生成 {csv_path}")
