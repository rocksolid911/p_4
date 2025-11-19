import 'package:flutter/material.dart';

import '../../features/splash/presentation/splash_screen.dart';
import '../../features/onboarding/presentation/onboarding_screen.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/auth/presentation/register_screen.dart';
import '../../features/home/presentation/home_screen.dart';
import '../../features/bills/presentation/bills_list_screen.dart';
import '../../features/bills/presentation/bill_detail_screen.dart';
import '../../features/news/presentation/news_list_screen.dart';
import '../../features/news/presentation/news_detail_screen.dart';
import '../../features/profile/presentation/profile_screen.dart';

class AppRouter {
  static const String splash = '/';
  static const String onboarding = '/onboarding';
  static const String login = '/login';
  static const String register = '/register';
  static const String home = '/home';
  static const String bills = '/bills';
  static const String billDetail = '/bill-detail';
  static const String news = '/news';
  static const String newsDetail = '/news-detail';
  static const String profile = '/profile';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case splash:
        return MaterialPageRoute(builder: (_) => const SplashScreen());

      case onboarding:
        return MaterialPageRoute(builder: (_) => const OnboardingScreen());

      case login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());

      case register:
        return MaterialPageRoute(builder: (_) => const RegisterScreen());

      case home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());

      case bills:
        return MaterialPageRoute(builder: (_) => const BillsListScreen());

      case billDetail:
        final billId = settings.arguments as int;
        return MaterialPageRoute(
          builder: (_) => BillDetailScreen(billId: billId),
        );

      case news:
        return MaterialPageRoute(builder: (_) => const NewsListScreen());

      case newsDetail:
        final newsId = settings.arguments as int;
        return MaterialPageRoute(
          builder: (_) => NewsDetailScreen(newsId: newsId),
        );

      case profile:
        return MaterialPageRoute(builder: (_) => const ProfileScreen());

      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(
              child: Text('No route defined for ${settings.name}'),
            ),
          ),
        );
    }
  }
}
