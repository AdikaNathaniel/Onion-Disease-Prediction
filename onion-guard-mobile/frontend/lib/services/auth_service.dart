import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api_config.dart';
import '../models/user_model.dart';

class AuthService {
  static const String _tokenKey = 'auth_token';
  static const String _emailKey = 'user_email';
  static const String _userKey = 'user_data';

  Future<Map<String, dynamic>> register({
    required String name,
    required String email,
    required String phone,
    required String password,
    required String userType,
    required String username,
    String languagePreference = 'en',
  }) async {
    final response = await http.post(
      Uri.parse(ApiConfig.register),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        'name': name,
        'email': email,
        'phone': phone,
        'password': password,
        'user_type': userType,
        'username': username,
        'language_preference': languagePreference,
      }),
    );
    return json.decode(response.body);
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
    required String userType,
  }) async {
    final response = await http.post(
      Uri.parse(ApiConfig.login),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        'email': email,
        'password': password,
        'user_type': userType,
      }),
    );

    final data = json.decode(response.body);

    if (response.statusCode == 200 && data['success'] == true) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_tokenKey, data['token']);
      await prefs.setString(_emailKey, email);
      await prefs.setString(_userKey, json.encode(data['user']));
    }

    return data;
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  Future<String?> getSavedEmail() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_emailKey);
  }

  Future<UserModel?> getSavedUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userData = prefs.getString(_userKey);
    if (userData != null) {
      return UserModel.fromJson(json.decode(userData));
    }
    return null;
  }

  Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_emailKey);
    await prefs.remove(_userKey);
  }

  Future<Map<String, dynamic>> changePassword({
    required String email,
    required String oldPassword,
    required String newPassword,
  }) async {
    final response = await http.post(
      Uri.parse(ApiConfig.changePassword),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        'email': email,
        'old_password': oldPassword,
        'new_password': newPassword,
      }),
    );
    return json.decode(response.body);
  }

  Future<Map<String, dynamic>> forgotPassword(String email) async {
    final response = await http.post(
      Uri.parse(ApiConfig.forgotPassword(email)),
      headers: {"Content-Type": "application/json"},
    );
    return json.decode(response.body);
  }

  Future<Map<String, dynamic>> resetPassword({
    required String email,
    required String code,
    required String newPassword,
  }) async {
    final response = await http.post(
      Uri.parse(ApiConfig.resetPassword),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        'email': email,
        'code': code,
        'new_password': newPassword,
      }),
    );
    return json.decode(response.body);
  }

  Future<Map<String, dynamic>> sendFeedback({
    required String name,
    required String email,
    required String subject,
    required String message,
  }) async {
    final response = await http.post(
      Uri.parse(ApiConfig.feedback),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
      }),
    );
    return json.decode(response.body);
  }
}
