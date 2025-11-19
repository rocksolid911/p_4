import 'package:flutter/widgets.dart';

class L10n {
  static final all = [
    const Locale('en'),
    const Locale('hi'),
  ];
}

class AppLocalizations {
  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  // Common strings
  String get appName => 'LokSathi';
  String get home => 'Home';
  String get bills => 'Bills';
  String get news => 'News';
  String get profile => 'Profile';

  // Auth strings
  String get login => 'Login';
  String get register => 'Register';
  String get email => 'Email';
  String get password => 'Password';
  String get name => 'Name';

  // Button labels
  String get submit => 'Submit';
  String get cancel => 'Cancel';
  String get save => 'Save';
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => ['en', 'hi'].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations();
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
