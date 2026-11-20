
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_response_body(self):
        response = self.client.get("/")
        self.assertEqual(
            response.get_data(as_text=True),
            "Wrong Response"
        )

if __name__ == "__main__":
    unittest.main()
