# Run StudyGenie locally

Requires Python 3.10+ and Flutter SDK with Chrome.

From the repository root:
1. Install dependencies: `python -m pip install -r requirements.txt`.
2. Set GEMINI_API_KEY and GEMINI_MODEL in your shell environment. Use a model available to your Gemini account. Never commit credentials. For PowerShell: `$env:GEMINI_API_KEY = 'your-key'` and `$env:GEMINI_MODEL = 'your-model'`.
3. Run `python backend.py`.
4. In a second terminal run `cd flutter_app`, then `flutter create --platforms=web .` to generate the web platform scaffolding, then `flutter pub get`.
5. Run `flutter run -d chrome --web-port=8080 --dart-define=API_URL=http://localhost:8000`.
6. Enter a study question and press Ask StudyGenie.

Python tests: from the root, run `python -m unittest -v`.
Flutter tests: from flutter_app, run `flutter test`.

The server binds to localhost and permits the configured local Flutter web origin by default. This is a development prototype, not a production deployment. Authentication, rate limiting and HTTPS are required before public hosting. Live credentials and Flutter runtime verification are not included.
