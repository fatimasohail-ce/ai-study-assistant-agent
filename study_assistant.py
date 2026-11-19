"""StudyGenie response validation and error handling (SCRUM-8)."""
import os
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def answer_question(question: str, api_key: str | None, request: Callable[[str], str]) -> tuple[bool, str]:
    """Return a success flag and a student-facing message."""
    if not isinstance(question, str) or not question.strip():
        return False, 'Please enter a study question.'
    if not isinstance(api_key, str) or not api_key.strip():
        return False, 'AI service is not configured.'
    try:
        response = request(question.strip())
        if not isinstance(response, str) or not response.strip():
            return False, 'No answer received. Please try again.'
        return True, response
    except Exception as exc:
        logger.warning('Study assistant request failed (%s)', type(exc).__name__)
        return False, 'AI service is unavailable. Please try again later.'


def ask_gemini(question: str, model: str | None = None) -> tuple[bool, str]:
    """Optional SDK adapter; requires google-genai and environment configuration."""
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    model = model or os.getenv('GEMINI_MODEL')

    def request(prompt: str) -> str:
        if not model:
            raise ValueError('Missing model configuration')
        from google import genai
        from google.genai import types
        with genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=30000)) as client:
            return client.models.generate_content(model=model, contents=prompt).text

    if isinstance(question, str) and question.strip() and api_key and api_key.strip() and not model:
        return False, 'AI service is not configured.'
    return answer_question(question, api_key, request)
