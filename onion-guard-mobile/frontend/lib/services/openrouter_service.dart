import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

/// Thin client for the backend's LLM proxy.
/// API keys live in the backend .env — never in the app bundle.
class OpenRouterService {
  Future<Map<String, dynamic>> analyzeFreshness(File imageFile) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse(ApiConfig.llmFreshness),
    )..files.add(await http.MultipartFile.fromPath('file', imageFile.path));

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    if (response.statusCode != 200) {
      throw Exception('Freshness analysis failed: ${response.statusCode}');
    }

    return Map<String, dynamic>.from(json.decode(response.body));
  }

  Future<String> translate(String text, String targetLanguage) async {
    if (targetLanguage == 'en') return text;

    final response = await http.post(
      Uri.parse(ApiConfig.llmTranslate),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'text': text, 'target_language': targetLanguage}),
    );

    if (response.statusCode != 200) {
      throw Exception('Translation failed: ${response.statusCode}');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return (data['translated_text'] as String?)?.trim() ?? text;
  }
}
