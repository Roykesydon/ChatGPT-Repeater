import argparse
import csv
import os
import re

from data_handler.JsonHandler import JsonHandler
from data_handler.PaperHandler import PaperHandler

"""
把回傳結果轉為 CSV
"""

if __name__ == "__main__":
    # 處理輸入參數
    parser = argparse.ArgumentParser(description="轉換輸出結果")
    parser.add_argument(
        "--result_folder_name", type=str, help="把輸出資料夾下的結果資料夾名稱(時間戳記)填入這裡"
    )
    args = parser.parse_args()
    result_folder_name = args.result_folder_name

    # 初始化
    json_handler = JsonHandler()
    config = json_handler.return_json_as_dict(json_path="./config.json")
    paper_handler = PaperHandler(config=config)
    all_row_list = []  # 存放資料集每一 row 的 list

    # 取得資料夾中的所有資料夾
    result_path = os.path.join(config["output_folder"], result_folder_name)
    subdirectories = paper_handler.get_sub_directories(result_path)
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

    # 把資料寫入 csv
    csv_path = os.path.join(config["output_folder"], f"result_{result_folder_name}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["question", "answer", "title", "filename"])
        writer.writerows(all_row_list)

    print(f"已生成 {csv_path}")
