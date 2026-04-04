class ApiConfig {
  // For Android emulator use 10.0.2.2, for iOS simulator use localhost
  // For physical device use your computer's local IP
  static const String baseUrl = 'http://16.16.90.16:8000';

  // Auth endpoints
  static const String register = '$baseUrl/api/v1/auth/register';
  static const String login = '$baseUrl/api/v1/auth/login';
  static String profile(String email) => '$baseUrl/api/v1/auth/profile/$email';
  static const String changePassword = '$baseUrl/api/v1/auth/change-password';
  static String forgotPassword(String email) =>
      '$baseUrl/api/v1/auth/forgot-password/$email';

  // Diagnosis endpoints
  static const String predict = '$baseUrl/api/v1/diagnosis/predict';
  static String diagnosisHistory(String email) =>
      '$baseUrl/api/v1/diagnosis/history/$email';

  // Treatment endpoints
  static String treatment(String disease) =>
      '$baseUrl/api/v1/treatment/$disease';
  static String treatmentVoice(String disease, String lang) =>
      '$baseUrl/api/v1/treatment/$disease/voice/$lang';

  // Analytics endpoints
  static const String analyticsLog = '$baseUrl/api/v1/analytics/log';
  static String analyticsSummary(String email) =>
      '$baseUrl/api/v1/analytics/summary/$email';
  static const String analyticsRegional = '$baseUrl/api/v1/analytics/regional';
}
