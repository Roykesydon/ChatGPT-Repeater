import unittest
from unittest.mock import patch

from model.ChatGPT import ChatGPT


class ChatGPTTestCase(unittest.TestCase):
    def test_generate_response_without_api_key(self):
        """
        測試沒有設置 API Key 的情況
        """
        # 建立 ChatGPT 實例
        chat_gpt = ChatGPT()

        # 測試 generate_response 方法是否拋出指定的異常
        with self.assertRaises(Exception) as context:
            chat_gpt.generate_response("Prompt")

        print(str(context.exception))

        # 檢查異常訊息是否符合預期
        self.assertEqual(
            str(context.exception), "Need to set API Key with ChatGPT.set_api_key()"
        )


if __name__ == "__main__":
    unittest.main()
