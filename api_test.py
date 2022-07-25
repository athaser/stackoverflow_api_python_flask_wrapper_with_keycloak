import unittest
import requests

class ApiTest(unittest.TestCase):
    def test_1_DNS_status_code_json_length(self):
        ###TEST IN DNS for one day (2022-07-01 - 2022-07-02)
        API_URL_DNS = "https://encode.karmanirvami.com/api/v1/stackstats?since=2022-07-01 00:00:00&until=2022-07-02 00:00:00"
        r = requests.get(API_URL_DNS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)

    def test_2_IP_status_code_json_length(self):
        ###TEST IN IP for one day (2022-07-01 - 2022-07-02)
        API_URL_IP = "http://88.80.188.249:5000/api/v1/stackstats?since=2022-07-01 00:00:00&until=2022-07-02 00:00:00"
        r = requests.get(API_URL_IP)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)

    def test_3_DNS_status_code_json_length(self):
        ###TEST IN DNS for two days (2022-07-01 - 2022-07-03)
        API_URL_DNS = "https://encode.karmanirvami.com/api/v1/stackstats?since=2022-07-01 00:00:00&until=2022-07-03 00:00:00"
        r = requests.get(API_URL_DNS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)

    def test_4_IP_status_code_json_length(self):
        ###TEST IN IP for two day (2022-07-01 - 2022-07-03)
        API_URL_IP = "http://88.80.188.249:5000/api/v1/stackstats?since=2022-07-01 00:00:00&until=2022-07-03 00:00:00"
        r = requests.get(API_URL_IP)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)
    
    def test_5_DNS_status_code_json_length(self):
        ###TEST IN DNS without queries since and until
        API_URL_DNS = "https://encode.karmanirvami.com/api/v1/stackstats"
        r = requests.get(API_URL_DNS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)

    def test_6_IP_status_code_json_length(self):
        ###TEST IN IP without queries since and until
        API_URL_IP = "http://88.80.188.249:5000/api/v1/stackstats"
        r = requests.get(API_URL_IP)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)

if __name__=='__main__':
    unittest.main()
