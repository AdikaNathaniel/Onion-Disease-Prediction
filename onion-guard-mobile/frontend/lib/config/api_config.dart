class ApiConfig {
  // For Android emulator use 10.0.2.2, for iOS simulator use localhost
  // For physical device use your computer's local IP
  static const String baseUrl = 'https://onion-guard.duckdns.org';

  // Auth endpoints
  static const String register = '$baseUrl/api/v1/auth/register';
  static const String login = '$baseUrl/api/v1/auth/login';
  static String profile(String email) => '$baseUrl/api/v1/auth/profile/$email';
  static const String changePassword = '$baseUrl/api/v1/auth/change-password';
  static String forgotPassword(String email) =>
      '$baseUrl/api/v1/auth/forgot-password/$email';
  static const String resetPassword = '$baseUrl/api/v1/auth/reset-password';
  static const String feedback = '$baseUrl/api/v1/feedback';

  // Diagnosis endpoints
  static const String predict = '$baseUrl/api/v1/diagnosis/predict';
  static String diagnosisHistory(String email) =>
      '$baseUrl/api/v1/diagnosis/history/$email';

  // LLM endpoints (keys live on the server)
  static const String llmFreshness = '$baseUrl/api/v1/llm/freshness';
  static const String llmTranslate = '$baseUrl/api/v1/llm/translate';
  static const String llmIdentifyObject = '$baseUrl/api/v1/llm/identify-object';

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
  static const String analyticsSummaryAll = '$baseUrl/api/v1/analytics/summary-all';
  static const String analyticsAllScans = '$baseUrl/api/v1/analytics/all-scans';
  static String analyticsTimeseries(String email, {int days = 30}) =>
      '$baseUrl/api/v1/analytics/timeseries/$email?days=$days';

  // Admin endpoints
  static const String usersList = '$baseUrl/api/v1/auth/users';
  static String toggleUserStatus(String email) =>
      '$baseUrl/api/v1/auth/users/$email/toggle-status';
}
