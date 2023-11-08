import unittest
import json
from app import app


class VotingAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_poll(self):
        data = {"title": "Лучший покемон", "options": ["Пикачу", "Чаризард", "Бластуз"]}
        response = self.app.post("/api/createPoll/", data=json.dumps(data), content_type="application/json")
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("poll_id", data)

    def test_vote(self):
        # Предположим, что у нас уже есть голосование с poll_id=1 и двумя вариантами ответов.
        data = {"poll_id": 1, "choice_id": 0}
        response = self.app.post("/api/poll/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_result(self):
        # Предположим, что у нас уже есть голосование с poll_id=1 и двумя вариантами ответов.
        data = {"poll_id": 1}
        response = self.app.post("/api/getResult/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIsInstance(data, dict)


if __name__ == '__main__':
    unittest.main()

