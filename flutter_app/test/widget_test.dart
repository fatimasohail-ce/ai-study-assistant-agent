import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:studygenie/main.dart';

void main() {
  testWidgets('Empty question is rejected', (tester) async {
    await tester.pumpWidget(const StudyGenie());
    await tester.tap(find.widgetWithText(FilledButton, 'Ask StudyGenie'));
    await tester.pumpAndSettle();
    expect(find.text('Please enter a study question.'), findsOneWidget);
  });
}
