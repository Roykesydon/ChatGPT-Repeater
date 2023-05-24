# ChatGPT-Repeater

The aim of this project is to automate the process of repeatedly requesting ChatGPT to handle data.

This program concatenates  ```prompt_prefix``` and ```prompt_suffix``` with prompt and saves the response of ChatGPT.

## How To Execute

1. Generate and fill out config.json (Referencing config.example.json)

2. Put the research paper data into the ```./data``` folder. The format for each paper is as follows:
    ```
    └── Paper folder
        ├── meta.json
        ├── part1.txt
        ├── part2.txt
        ├── part3.txt
        └── part4.txt
    ```
    - Paper's content has been split into multiple parts, each containing approximately 3,000 tokens.
    - The format for meta.json is as follows:
    ```
    {
        "title": "Paper title",
        "filename": "Paper filename"
    }
    ```

    - example
        - ```
            ./data
            ├── Paper A
            │   ├── meta.json
            │   ├── part1.txt
            │   ├── part2.txt
            │   ├── part3.txt
            │   ├── part4.txt
            │   └── part5.txt
            └── Paper B
                ├── meta.json
                ├── part1.txt
                ├── part2.txt
                ├── part3.txt
                └── part4.txt
            ```

    - Every paper folder will be considered a task, and the process will record the token usage and cost of the task in the output result.

3. Install python dependencies
    ```shell
    pip install -r requirements.txt
    ```

4. This script will save all ChatGPT completions to the output folder
    ```shell
    python get_result.py
    ```

5. This script will parse the QA information in the output folder to a CSV file
    ```shell
    python parse_result.py --result_folder_name <generated folder name under output folder>
    ```

## Output format
- The output of get_result.py will be in the following format:
    ```
    20230524_220036
    └── Paper A
        ├── meta.json
        ├── output_1.json
        ├── output_2.json
        ├── output_3.json
        ├── output_4.json
        └── output_5.json
    ```
    - The file ```meta.json``` will preserve its original key-value pairs and add information about token usage and cost. Its format is as follows:
    ```
    {
        "title": "Paper title",
        "filename": "Paper filename",
        "token_usage": <total token usage>,
        "cost": <total cost>
    }
    ```
    - ```output_x.json``` is the response of OpenAI API

- ```parse_result.py``` will generate a CSV file with the following columns:
    - "question", "answer", "title", "filename"
    
    