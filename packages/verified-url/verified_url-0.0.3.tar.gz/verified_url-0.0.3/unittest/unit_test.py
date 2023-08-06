#! /usr/bin/python
import unittest
import sys

sys.path.append("..")
from src.check_url import CheckUrls
from src.url_is_reacheable import check

class TestURL(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(5,5)
    def test_urls_status(self):
        self.assertEqual(CheckUrls.check_urls_by_json_file('E:/Users/Maxime/Documents/PYTHON - URL_VALID/unitTest/input_url.json', 'E:/Users/Maxime/Documents/PYTHON - URL_VALID/unitTest'), 0)
    def test_check_url_ok(self):
        self.assertEqual(check("https://www.nfinite.app/")['available'], True)
    def test_check_url_ko(self):
            self.assertEqual(check("https://www.hubstairs.com/image_dfe93ea2ce26b4284.png")['available'], False)
    def test_check_url_empty(self):
        r = check("")
        self.assertEqual(r['available'], False)
        self.assertEqual(r['status_code'], 400)

if __name__ == '__main__':
    unittest.main()
