import unittest
from app import app
from io import BytesIO

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_file(self):
        response = self.app.post('/upload', data={'file': (BytesIO(b"fake content"), 'test.mp4')})
        self.assertEqual(response.status_code, 200)

    def test_get_consent(self):
        response = self.app.post('/consent', json={'parental_consent': 'I agree'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
