import unittest

from data_handler.JsonHandler import JsonHandler


class JsonHandlerTestCase(unittest.TestCase):
    def test_return_json_as_dict(self):
        # 建立測試用的 JsonHandler 實例
        json_handler = JsonHandler()

        # 呼叫被測試的方法
        result = json_handler.return_json_as_dict("./test/data_handler/test_json.json")

        # 預期結果
        expected_result = {"openai_api_key": "", "model": "turbo"}

        # 比較結果
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
