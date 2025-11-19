import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppConfig {
  static late SharedPreferences _prefs;

  // API Configuration
  static const String baseUrl = kDebugMode
      ? 'http://localhost:8000/api'
      : 'https://api.loksathi.in/api';

  // Mixpanel Configuration
  static const String mixpanelToken = 'YOUR_MIXPANEL_TOKEN';

  // App Configuration
  static const int apiTimeout = 30000; // 30 seconds
  static const int pageSize = 20;

  // Supported Languages
  static const List<String> supportedLanguages = ['en', 'hi', 'mr', 'te', 'ta'];

  static Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
  }

  static SharedPreferences get prefs => _prefs;

  // User preferences
  static String? get accessToken => _prefs.getString('access_token');
  static String? get refreshToken => _prefs.getString('refresh_token');

  static Future<void> setTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _prefs.setString('access_token', accessToken);
    await _prefs.setString('refresh_token', refreshToken);
  }

  static Future<void> clearTokens() async {
    await _prefs.remove('access_token');
    await _prefs.remove('refresh_token');
  }

  static bool get isLoggedIn => accessToken != null;

  // Language preference
  static String get preferredLanguage =>
      _prefs.getString('preferred_language') ?? 'en';

  static Future<void> setPreferredLanguage(String languageCode) async {
    await _prefs.setString('preferred_language', languageCode);
  }
}
