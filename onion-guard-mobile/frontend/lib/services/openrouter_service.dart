import 'dart:convert';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class OpenRouterService {
  static String get _openRouterKey => dotenv.env['OPENROUTER_API_KEY'] ?? '';
  static String get _openRouterUrl => dotenv.env['OPENROUTER_BASE_URL'] ?? 'https://openrouter.ai/api/v1';
  static String get _openRouterModel => dotenv.env['DEFAULT_LLM_MODEL'] ?? 'anthropic/claude-3-haiku';
  static String get _geminiKey => dotenv.env['GEMINI_API_KEY'] ?? '';

  /// Analyze onion freshness using Gemini Vision API
  Future<Map<String, dynamic>> analyzeFreshness(File imageFile) async {
    final bytes = await imageFile.readAsBytes();
    final base64Image = base64Encode(bytes);
    final mimeType = imageFile.path.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';

    final apiKey = _geminiKey;
    if (apiKey.isEmpty) {
      throw Exception('Gemini API key not configured');
    }

    final response = await http.post(
      Uri.parse('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$apiKey'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'contents': [
          {
            'parts': [
              {
                'text': 'Analyze this onion image and determine its freshness level. Respond ONLY in this exact JSON format, nothing else: {"freshness": "Fresh" or "Almost Spoilt" or "Rotten", "confidence": 0-100, "description": "brief explanation of visual signs", "tips": "storage or usage recommendation"}'
              },
              {
                'inline_data': {
                  'mime_type': mimeType,
                  'data': base64Image,
                },
              },
            ],
          },
        ],
        'generationConfig': {
          'maxOutputTokens': 1024,
          'responseMimeType': 'application/json',
        },
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Gemini API failed: ${response.statusCode}');
    }

    final data = json.decode(response.body);
    final candidates = data['candidates'] as List?;
    if (candidates == null || candidates.isEmpty) {
      throw Exception('No response from Gemini');
    }

    final parts = candidates[0]['content']['parts'] as List;

    // Find the text part containing JSON
    String fullText = '';
    for (final part in parts) {
      if (part['text'] != null) {
        fullText += part['text'].toString();
      }
    }

    // Strip markdown code block wrapping if present
    fullText = fullText.replaceAll(RegExp(r'```json\s*'), '').replaceAll(RegExp(r'```\s*'), '').trim();

    // Try to parse the full text as JSON directly first
    try {
      return Map<String, dynamic>.from(json.decode(fullText));
    } catch (_) {
      // Fall back to regex extraction
      final jsonMatch = RegExp(r'\{[\s\S]*\}').firstMatch(fullText);
      if (jsonMatch == null) {
        throw Exception('Could not parse response');
      }
      return Map<String, dynamic>.from(json.decode(jsonMatch.group(0)!));
    }
  }

  /// Translate text to a target language
  Future<String> translate(String text, String targetLanguage) async {
    final langNames = {
      'en': 'English',
      'tw': 'Twi (Akan)',
      'dg': 'Dagbani',
      'ee': 'Ewe',
      'ha': 'Hausa',
    };

    final langName = langNames[targetLanguage] ?? 'English';
    if (targetLanguage == 'en') return text;

    final response = await http.post(
      Uri.parse('$_openRouterUrl/chat/completions'),
      headers: {
        'Authorization': 'Bearer $_openRouterKey',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'model': _openRouterModel,
        'messages': [
          {
            'role': 'user',
            'content': 'Translate the following text to $langName. Return ONLY the translated text, nothing else:\n\n$text',
          },
        ],
        'max_tokens': 1000,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Translation failed: ${response.statusCode}');
    }

    final data = json.decode(response.body);
    return data['choices'][0]['message']['content'].toString().trim();
  }
}
