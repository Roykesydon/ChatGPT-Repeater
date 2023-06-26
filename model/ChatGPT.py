import time
from typing import Tuple

import backoff
import openai
import tiktoken


class ChatGPT:
    _api_key: str = ""

    def __init__(self, config: dict):
        self.last_generate_time = None
        self._config = config
        self._token_count = 0

    """
    設置 API Key 是全局設置的，不限於 Instance
    """

    @staticmethod
    def set_api_key(api_key: str) -> None:
        ChatGPT._api_key = api_key
        openai.api_key = ChatGPT._api_key

    @backoff.on_exception(backoff.expo, openai.error.ServiceUnavailableError)
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def generate_response(self, prompt: str) -> dict:
        # Check API Key setting
        if ChatGPT._api_key == "":
            raise Exception("Need to set API Key with ChatGPT.set_api_key()")

        """
        處理 rpm 和 tpm 
        目前依賴於用 backoff 解決
        """
        # # check for rpm limit
        # if self.last_generate_time is not None:
        #     elapsed_time = time.time() - self.last_generate_time
        #     min_interval = 60 / self._config["rpm"]  # 每分鐘 60 次請求
        #     if elapsed_time < min_interval:
        #         sleep_time = min_interval - elapsed_time
        #         time.sleep(sleep_time)

        # # check for tmp limit
        # pass

        """
        API 參數參考: https://platform.openai.com/docs/api-reference/chat/create#chat/create-max_tokens
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # max_tokens=128, # Completion 可產生的最大 token 數，預設是無限，輸入和輸出的總長受到 context length 的限制
            # temperature=1.0, # 0~2 較高的數值會讓回應更有變化，預設是 1
            # n=1, # 產生幾個回應，預設是 1
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        self.last_generate_time = time.time()
        self._token_count += response["usage"]["total_tokens"]

        return response

    def init_count_token_usage(self) -> None:
        self._token_count = 0

    def get_token_usage_and_cost(self) -> Tuple[int, float]:
        price_per_1k_tokens = self._config["price_per_1k_tokens"]
        return self._token_count, self._token_count / 1000 * price_per_1k_tokens

    def count_message_token(self, message: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        encoded_message = encoding.encode(message)

        return len(encoded_message)

    def check_message_token_length_limit(self, message: str) -> bool:
        max_context_tokens_length = self._config["max_context_tokens_length"]
        return self.count_message_token(message) <= max_context_tokens_length
