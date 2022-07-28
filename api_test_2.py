import unittest
import requests
import timestamp
import functions

class ApiTest(unittest.TestCase):
    def test_9_function_is_accepted_last(self):
        ###TEST function_is_accepted_last from functions.py
        API_URL_DNS = "https://api.stackexchange.com/2.3/answers?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&pagesize=100&fromdate=1656633600&todate=1656720000&order=desc&sort=activity&filter=default&page=51"
        r = requests.get(API_URL_DNS)
        json_response = r.json()
        self.assertEqual(len(functions.function_is_accepted_last_page(json_response['items'], 2)), 4)

if __name__=='__main__':
    unittest.main()