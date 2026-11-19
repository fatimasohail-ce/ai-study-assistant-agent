# SCRUM-8 and SCRUM-10

## Run the tests

With Python 3.10 or later, from the repository root:

```sh
python -m unittest -v test_study_assistant
```

The tests do not require network access, an API key, or the Gemini SDK.

## Integration

Install the optional Gemini SDK with `python -m pip install google-genai`.
Set `GEMINI_API_KEY` and `GEMINI_MODEL` in the server process environment. Do not commit credentials or expose them to Flutter clients.

Call `study_assistant.ask_gemini(question)` from the Python backend, or pass an existing Gemini request adapter into `answer_question(question, api_key, request)`. Both return a pair consisting of a Boolean success flag and a student-facing message. Display the returned message in the UI; use the flag to distinguish error responses.

The request adapter must return text and enforce a bounded timeout. The optional adapter sets a 30-second SDK timeout.

## Verification and limitations

Seven unit tests passed locally; see TEST_RESULTS.txt. Tests use mocks and do not validate a real Gemini API request. Flutter integration, teammate API integration, and end-to-end testing are pending. No claim is made that the full application is complete.
