import 'package:dio/dio.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

import '../../core/config/app_config.dart';

class ApiClient {
  late final Dio _dio;

  static final ApiClient _instance = ApiClient._internal();

  factory ApiClient() => _instance;

  ApiClient._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConfig.baseUrl,
        connectTimeout: const Duration(milliseconds: AppConfig.apiTimeout),
        receiveTimeout: const Duration(milliseconds: AppConfig.apiTimeout),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add interceptors
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Add auth token if available
          final token = AppConfig.accessToken;
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (error, handler) async {
          // Handle token refresh on 401
          if (error.response?.statusCode == 401) {
            final refreshed = await _refreshToken();
            if (refreshed) {
              // Retry the request
              final opts = error.requestOptions;
              opts.headers['Authorization'] = 'Bearer ${AppConfig.accessToken}';
              try {
                final response = await _dio.request(
                  opts.path,
                  options: Options(
                    method: opts.method,
                    headers: opts.headers,
                  ),
                  data: opts.data,
                  queryParameters: opts.queryParameters,
                );
                return handler.resolve(response);
              } catch (e) {
                return handler.next(error);
              }
            }
          }
          return handler.next(error);
        },
      ),
    );

    // Add logger in debug mode
    _dio.interceptors.add(
      PrettyDioLogger(
        requestHeader: true,
        requestBody: true,
        responseBody: true,
        responseHeader: false,
        error: true,
        compact: true,
      ),
    );
  }

  Dio get dio => _dio;

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = AppConfig.refreshToken;
      if (refreshToken == null) return false;

      final response = await _dio.post(
        '/auth/refresh/',
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        final accessToken = response.data['access'];
        await AppConfig.setTokens(
          accessToken: accessToken,
          refreshToken: refreshToken,
        );
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  // Auth endpoints
  Future<Response> register(Map<String, dynamic> data) =>
      _dio.post('/auth/register/', data: data);

  Future<Response> login(Map<String, dynamic> data) =>
      _dio.post('/auth/login/', data: data);

  Future<Response> getProfile() => _dio.get('/auth/profile/');

  Future<Response> updateProfile(Map<String, dynamic> data) =>
      _dio.put('/auth/profile/', data: data);

  // Bill endpoints
  Future<Response> getBills({Map<String, dynamic>? queryParameters}) =>
      _dio.get('/bills/', queryParameters: queryParameters);

  Future<Response> getBill(int id) => _dio.get('/bills/$id/');

  Future<Response> summarizeBill(Map<String, dynamic> data) =>
      _dio.post('/analysis/bills/summarize/', data: data);

  // News endpoints
  Future<Response> getNews({Map<String, dynamic>? queryParameters}) =>
      _dio.get('/news/', queryParameters: queryParameters);

  Future<Response> getNewsArticle(int id) => _dio.get('/news/$id/');

  Future<Response> analyzeNews(Map<String, dynamic> data) =>
      _dio.post('/analysis/news/analyze/', data: data);

  // Recommendations
  Future<Response> getRecommendations({int limit = 20}) =>
      _dio.get('/recommendations/', queryParameters: {'limit': limit});

  // Interactions
  Future<Response> createInteraction(Map<String, dynamic> data) =>
      _dio.post('/bills/interactions/', data: data);
}
