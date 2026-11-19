import unittest
from unittest.mock import Mock
from backend import process_question

class BackendTests(unittest.TestCase):
    def test_invalid_question(self):
        answer = Mock()
        for payload in ({}, {"question": " "}, {"question": None}, None):
            self.assertEqual(process_question(payload, answer)[0], 400)
        answer.assert_not_called()

    def test_success(self):
        answer = Mock(return_value=(True, "Explanation"))
        self.assertEqual(process_question({"question": " AI? "}, answer),
                         (200, {"success": True, "message": "Explanation"}))
        answer.assert_called_once_with("AI?")

    def test_failure(self):
        answer = Mock(return_value=(False, "Service unavailable"))
        self.assertEqual(process_question({"question": "AI?"}, answer),
                         (503, {"success": False, "message": "Service unavailable"}))

    def test_exception(self):
        answer = Mock(side_effect=RuntimeError("private detail"))
        status, payload = process_question({"question": "AI?"}, answer)
        self.assertEqual(status, 503)
        self.assertNotIn("private detail", payload["message"])

    def test_length(self):
        answer = Mock()
        self.assertEqual(process_question({"question": "a"*8001}, answer)[0], 400)
        answer.assert_not_called()

if __name__ == "__main__":
    unittest.main()
