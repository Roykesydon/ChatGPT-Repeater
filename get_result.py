import os

from data_handler.JsonHandler import JsonHandler
from data_handler.TaskHandler import TaskHandler
from model.ChatGPT import ChatGPT

"""
用來把切割好的論文資料，輪流丟給 ChatGPT 並儲存回傳結果
"""

if __name__ == "__main__":
    """
    設置 ChatGPT
    """
    json_handler = JsonHandler()
    config = json_handler.return_json_as_dict(json_path="./config.json")

    model = ChatGPT(config=config)
    model.set_api_key(config["openai_api_key"])

    """
    讀取論文資料
    """
    task_handler = TaskHandler(config=config)
    all_task_data = []

    # 指定資料夾路徑
    folder_path = "./data"

    # 取得資料夾中的所有資料夾
    subdirectories = task_handler.get_sub_directories(folder_path)

    # 存取所有論文資料
    for subdirectory in subdirectories:
        task_data = task_handler.get_task_data(subdirectory)
        all_task_data.append(task_data)

    """
    詢問 ChatGPT 並儲存結果
    """
    output_folder_path = task_handler.create_all_result_folder()

    total_token_usage = 0
    total_cost = 0

    for task_data in all_task_data:
        prompt = ""
        output_task_path = task_handler.create_task_result_folder(
            output_folder_path, task_data
        )
        model.init_count_token_usage()

        # 詢問每個 part
        for index, part in enumerate(task_data["parts"]):
            prompt = config["prompt_prefix"] + part + config["prompt_suffix"]

            # 確認 token 長度沒有超過限制
            if not model.check_message_token_length_limit(prompt):
                print(f"prompt 長度超過限制，{task_data['folder_name']}-part {index + 1}")
                print(
                    f"總長度: {model.count_message_token(prompt)}, part 長度: {model.count_message_token(part)}, prompt_prefix + prompt_suffix 長度: {model.count_message_token(config['prompt_prefix'] + config['prompt_suffix'])}"
                )
                continue

            response = model.generate_response(prompt=prompt)

            task_handler.save_response(
                result=response,
                output_task_path=output_task_path,
                part_index=index + 1,
            )

        # 輸出本篇論文花費資訊
        token_usage, cost = model.get_token_usage_and_cost()
        print(f"{task_data['folder_name']} 消耗了 {token_usage} 個 token")
        print(f"花費 $ {cost}")
        print("-----")

        # 儲存 meta.json 原有資訊以及花費資訊
        meta_data = task_data["metadata"]
        meta_data["token_usage"] = token_usage
        meta_data["cost"] = cost
        task_handler.save_meta_data(output_task_path, meta_data)

        total_token_usage += token_usage
        total_cost += cost

    print(f"本次任務消耗了 {total_token_usage} 個 token")
    print(f"共花費 $ {total_cost}")
