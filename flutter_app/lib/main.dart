import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const StudyGenie());

class StudyGenie extends StatelessWidget {
  const StudyGenie({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'StudyGenie',
    theme: ThemeData(colorSchemeSeed: Colors.indigo, useMaterial3: true),
    home: const QuestionScreen(),
  );
}

class QuestionScreen extends StatefulWidget {
  const QuestionScreen({super.key});
  @override
  State<QuestionScreen> createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  final controller = TextEditingController();
  final formKey = GlobalKey<FormState>();
  bool busy = false;
  bool success = false;
  String answer = '';
  static const baseUrl = String.fromEnvironment('API_URL',
      defaultValue: 'http://localhost:8000');

  Future<void> submit() async {
    if (busy || !formKey.currentState!.validate()) return;
    setState(() { busy = true; answer = ''; success = false; });
    bool ok = false;
    String message;
    try {
      final response = await http.post(Uri.parse('$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': controller.text.trim()}),
      ).timeout(const Duration(seconds: 45));
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      ok = response.statusCode == 200 && data['success'] == true;
      message = data['message'] is String
          ? data['message'] as String : 'Unexpected response. Please retry.';
    } catch (_) {
      message = 'Unable to connect to StudyGenie. Please try again.';
    }
    if (!mounted) return;
    setState(() { answer = message; success = ok; busy = false; });
  }

  @override
  void dispose() { controller.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('StudyGenie')),
    body: Center(child: ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 720),
      child: ListView(padding: const EdgeInsets.all(24), children: [
        Text('What would you like to learn?', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 16),
        Form(key: formKey, child: TextFormField(
          controller: controller,
          enabled: !busy,
          maxLength: 8000,
          minLines: 3, maxLines: 6,
          decoration: const InputDecoration(labelText: 'Study question', border: OutlineInputBorder()),
          validator: (value) => value == null || value.trim().isEmpty
            ? 'Please enter a study question.' : null,
        )),
        const SizedBox(height: 12),
        FilledButton(onPressed: busy ? null : submit,
          child: Text(busy ? 'Thinking...' : 'Ask StudyGenie')),
        if (busy) const Padding(padding: EdgeInsets.all(16), child: LinearProgressIndicator()),
        if (answer.isNotEmpty) Card(child: Padding(padding: const EdgeInsets.all(20),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(success ? 'Explanation' : 'Unable to answer',
              style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            SelectableText(answer),
          ]))),
      ]),
    )),
  );
}
