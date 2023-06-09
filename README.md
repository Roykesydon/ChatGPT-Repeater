# ChatGPT-Repeater

The aim of this project is to automate the process of repeatedly requesting ChatGPT to handle data.

This program concatenates  ```prompt_prefix``` and ```prompt_suffix``` with prompt(content in ```partx.txt```) and saves the response of ChatGPT.

## How To Execute

1. Generate and fill out config.json (Referencing config.example.json)

2. Put the tasks into the ```./data``` folder. The format for each task is as follows:
    ```
    └── task folder
        ├── meta.json
        ├── part1.txt
        ├── part2.txt
        ├── part3.txt
        └── part4.txt
    ```
    - Every part(1-based) will be used as prompt.
    - Each task will be outputted to its corresponding folder. The original information in meta.json will be preserved and additional information will be appended, such as "token usage" and "cost".

    - example
        - ```
            ./data
            ├── Task A
            │   ├── meta.json
            │   ├── part1.txt
            │   ├── part2.txt
            │   ├── part3.txt
            │   ├── part4.txt
            │   └── part5.txt
            └── Task B
                ├── meta.json
                ├── part1.txt
                ├── part2.txt
                ├── part3.txt
                └── part4.txt
            ```

3. Install python dependencies
    ```shell
    pip install -r requirements.txt
    ```

4. This script will save all ChatGPT completions to the output folder
    ```shell
    python get_result.py
    ```

## Output format
- The output of get_result.py will be in the following format:
    ```
    20230524_220036
    └── Task A
        ├── meta.json
        ├── output_1.json
        ├── output_2.json
        ├── output_3.json
        ├── output_4.json
        └── output_5.json
    ```
    
- The file ```meta.json``` will preserve its original key-value pairs and add information about token usage and cost. For example:
    ```
    {
        "title": "Paper title",
        "filename": "Paper filename",
        "token_usage": <total token usage>,
        "cost": <total cost>
    }
    ```
- ```output_x.json``` is the response of OpenAI API with ```part_x.txt```

## Supported task (post-processing)

- Generating Q&A related to agriculture from paper
    - Use this setting for generating output
        - prompt_prefix / suffix: see ```./task_record/task_prompt.md```
        - The format for meta.json is as follows:
            ```
            {
                "title": "Paper title",
                "filename": "Paper filename"
            }
            ```

    -  Generate a CSV file with the following columns:
        - "question", "answer", "title", "filename"-   
        ```shell
        python post_process.py --task AgricultureQA --result_folder_name <generated folder name under output folder> 
        ``` 
       
    
    