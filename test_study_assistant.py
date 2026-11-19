import unittest
from unittest.mock import Mock, patch
from study_assistant import answer_question, ask_gemini


class StudyAssistantTests(unittest.TestCase):
    def test_empty_question(self):
        request = Mock()
        for question in ('', '  ', None):
            with self.subTest(question=question):
                self.assertEqual(answer_question(question, 'key', request),
                                 (False, 'Please enter a study question.'))
        request.assert_not_called()

    def test_success(self):
        request = Mock(return_value='A useful explanation')
        self.assertEqual(answer_question(' What is AI? ', 'key', request),
                         (True, 'A useful explanation'))
        request.assert_called_once_with('What is AI?')

    def test_api_failure(self):
        for exc in (RuntimeError('secret internal detail'), TimeoutError('timeout')):
            with self.subTest(exc=type(exc).__name__):
                request = Mock(side_effect=exc)
                with self.assertLogs('study_assistant', level='WARNING') as logs:
                    result = answer_question('AI?', 'key', request)
                self.assertEqual(result, (False, 'AI service is unavailable. Please try again later.'))
                self.assertNotIn('secret internal detail', str(logs.output))

    def test_missing_key(self):
        request = Mock()
        for key in (None, '', '  '):
            self.assertEqual(answer_question('AI?', key, request),
                             (False, 'AI service is not configured.'))
        request.assert_not_called()

    def test_empty_response(self):
        for response in ('', '  ', None):
            self.assertEqual(answer_question('AI?', 'key', Mock(return_value=response)),
                             (False, 'No answer received. Please try again.'))

    @patch.dict('os.environ', {}, clear=True)
    def test_adapter_missing_key(self):
        self.assertEqual(ask_gemini('AI?'), (False, 'AI service is not configured.'))

    @patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}, clear=True)
    def test_adapter_missing_model(self):
        self.assertEqual(ask_gemini('AI?'), (False, 'AI service is not configured.'))


if __name__ == '__main__':
    unittest.main()
