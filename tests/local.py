
import unittest
import json
import lambda_function
from . import MockContext
from . import load_test_data_from


class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self):
        event = load_test_data_from("tests/data/contact_flow_event_1.json")
        print(json.dumps(event))
        response = lambda_function.lambda_handler(
            event, MockContext("TestLambdaFunction"))
        print(json.dumps(response))


if __name__ == '__main__':
    unittest.main()
