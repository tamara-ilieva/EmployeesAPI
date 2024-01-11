import unittest
import json

from app import app


class TestCalculatorApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Calculator API")

    def test_add_numbers(self):
        post_data = {"num1": 5, "num2": 7} # test podatoci
        response = self.app.post("/add", json=post_data) # pravime request na nasheto api
        self.assertEqual(response.status_code, 200) # ochekuvame 200 da e status code od ovoj request
        result = json.loads(response.data)["result"] # go pretvarame vo dictionary odgovorot,
        # od dictionaryto ja gledame vrednosta za kluchot "result"
        self.assertEqual(result, 12) # gledame dali taa vred e ednakva na 12

    def test_add_numbers_without_2_numbers(self):
        post_data = {"num1": 7} # test podatoci
        response = self.app.post("/add", json=post_data) # pravime request
        self.assertEqual(response.status_code, 400)
        error_message = json.loads(response.data)["error"]
        self.assertEqual(error_message, "Please enter 2 numbers") # dali apito vrakja tochna poraka

    def test_subtract(self):
        post_data = {"num1": 10, "num2": 3}
        response = self.app.post("/subtract", data=json.dumps(post_data))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        result = response_data["result"]

        self.assertEqual(result, 7)


if __name__ == "__main__":
    unittest.main()