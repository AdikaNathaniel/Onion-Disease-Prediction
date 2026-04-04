import 'dart:convert';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class OpenRouterService {
  static String get _apiKey => dotenv.env['OPENROUTER_API_KEY'] ?? '';
  static String get _baseUrl => dotenv.env['OPENROUTER_BASE_URL'] ?? 'https://openrouter.ai/api/v1';
  static String get _model => dotenv.env['DEFAULT_LLM_MODEL'] ?? 'anthropic/claude-3-haiku';

  /// Analyze onion freshness from an image file
  Future<Map<String, dynamic>> analyzeFreshness(File imageFile) async {
    final bytes = await imageFile.readAsBytes();
    final base64Image = base64Encode(bytes);
    final mimeType = imageFile.path.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';

    final response = await http.post(
      Uri.parse('$_baseUrl/chat/completions'),
      headers: {
        'Authorization': 'Bearer $_apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'model': _model,
        'messages': [
          {
            'role': 'user',
            'content': [
              {
                'type': 'text',
                'text': '''Analyze this onion image and determine its freshness level.
Respond ONLY in this exact JSON format, nothing else:
{"freshness": "Fresh" or "Almost Spoilt" or "Rotten", "confidence": 0-100, "description": "brief explanation of visual signs", "tips": "storage or usage recommendation"}'''
              },
              {
                'type': 'image_url',
                'image_url': {
                  'url': 'data:$mimeType;base64,$base64Image',
                },
              },
            ],
          },
        ],
        'max_tokens': 300,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('API request failed: ${response.statusCode}');
    }

    final data = json.decode(response.body);
    final content = data['choices'][0]['message']['content'] as String;

    // Extract JSON from response
    final jsonMatch = RegExp(r'\{[\s\S]*\}').firstMatch(content);
    if (jsonMatch == null) {
      throw Exception('Invalid response format');
    }

    return json.decode(jsonMatch.group(0)!);
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
      Uri.parse('$_baseUrl/chat/completions'),
      headers: {
        'Authorization': 'Bearer $_apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'model': _model,
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
