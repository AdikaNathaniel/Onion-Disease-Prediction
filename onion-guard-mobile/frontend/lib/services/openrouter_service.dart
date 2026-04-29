import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import '../config/api_config.dart';

/// Thin client for the backend's LLM proxy.
/// API keys live in the backend .env — never in the app bundle.
class OpenRouterService {
  /// Build a MultipartFile with an explicit `image/*` content-type.
  /// `http.MultipartFile.fromPath` defaults to `application/octet-stream`,
  /// which the backend rejects with `400 "File must be an image"`.
  static Future<http.MultipartFile> _imagePart(File imageFile) async {
    final lower = imageFile.path.toLowerCase();
    String subtype;
    if (lower.endsWith('.png')) {
      subtype = 'png';
    } else if (lower.endsWith('.gif')) {
      subtype = 'gif';
    } else if (lower.endsWith('.webp')) {
      subtype = 'webp';
    } else if (lower.endsWith('.heic') || lower.endsWith('.heif')) {
      subtype = 'heic';
    } else {
      subtype = 'jpeg';
    }
    return http.MultipartFile.fromPath(
      'file',
      imageFile.path,
      contentType: MediaType('image', subtype),
    );
  }

  Future<Map<String, dynamic>> analyzeFreshness(File imageFile) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse(ApiConfig.llmFreshness),
    )..files.add(await _imagePart(imageFile));

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    if (response.statusCode != 200) {
      throw Exception('Freshness analysis failed: ${response.statusCode}');
    }

    return Map<String, dynamic>.from(json.decode(response.body));
  }

  /// Pre-check used before disease/freshness scans to verify the image is an onion.
  /// Returns {detected_object, is_onion, confidence}. On network/API failure,
  /// the caller should fall through and allow the scan rather than block.
  Future<Map<String, dynamic>> identifyObject(File imageFile) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse(ApiConfig.llmIdentifyObject),
    )..files.add(await _imagePart(imageFile));

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    if (response.statusCode != 200) {
      throw Exception('Object identification failed: ${response.statusCode}');
    }

    return Map<String, dynamic>.from(json.decode(response.body));
  }

  /// High-level pre-check used by both the disease and freshness scan pages.
  /// Always returns a map with shape:
  ///   {status: 'onion' | 'not_onion' | 'retake', detected_object?: String}
  ///
  /// - `onion`     → caller proceeds with the scan.
  /// - `not_onion` → caller shows a dialog with `detected_object`.
  /// - `retake`    → caller shows a generic "please retake the photo" dialog.
  ///                 Used for ANY upstream issue (5xx from Gemini, parse error,
  ///                 network timeout, etc.) so the user never sees backend details.
  Future<Map<String, dynamic>> checkIsOnion(File imageFile) async {
    try {
      final request = http.MultipartRequest('POST', Uri.parse(ApiConfig.llmIdentifyObject))
        ..files.add(await _imagePart(imageFile));
      final streamed = await request.send().timeout(const Duration(seconds: 30));
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode != 200) {
        return const {'status': 'retake'};
      }
      final parsed = Map<String, dynamic>.from(json.decode(response.body));
      if (parsed['is_onion'] == true) {
        return const {'status': 'onion'};
      }
      return {
        'status': 'not_onion',
        'detected_object': parsed['detected_object']?.toString() ?? '',
      };
    } catch (_) {
      return const {'status': 'retake'};
    }
  }

  /// Debug-only variant of [identifyObject] that NEVER throws and always returns
  /// a diagnostic map describing what happened end-to-end. No API keys are
  /// involved client-side — the keys live in the backend .env, so this only
  /// surfaces request URL, HTTP status, parsed body, and exception text.
  Future<Map<String, dynamic>> identifyObjectDebug(File imageFile) async {
    const url = ApiConfig.llmIdentifyObject;
    final stopwatch = Stopwatch()..start();
    try {
      final request = http.MultipartRequest('POST', Uri.parse(url))
        ..files.add(await _imagePart(imageFile));
      final streamed = await request.send().timeout(const Duration(seconds: 30));
      final response = await http.Response.fromStream(streamed);
      stopwatch.stop();

      Map<String, dynamic>? parsed;
      String? parseError;
      try {
        parsed = Map<String, dynamic>.from(json.decode(response.body));
      } catch (e) {
        parseError = e.toString();
      }

      return {
        'url': url,
        'status_code': response.statusCode,
        'duration_ms': stopwatch.elapsedMilliseconds,
        'raw_body': _truncate(response.body, 600),
        'parsed': parsed,
        'is_onion': parsed?['is_onion'],
        'detected_object': parsed?['detected_object'],
        'confidence': parsed?['confidence'],
        'parse_error': parseError,
        'exception': null,
      };
    } catch (e, st) {
      stopwatch.stop();
      return {
        'url': url,
        'status_code': null,
        'duration_ms': stopwatch.elapsedMilliseconds,
        'raw_body': null,
        'parsed': null,
        'is_onion': null,
        'detected_object': null,
        'confidence': null,
        'parse_error': null,
        'exception': '${e.runtimeType}: $e',
        'stack_first_line': st.toString().split('\n').first,
      };
    }
  }

  static String _truncate(String s, int max) =>
      s.length <= max ? s : '${s.substring(0, max)}…(${s.length - max} more chars)';

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
