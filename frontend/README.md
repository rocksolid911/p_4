# LokSathi Flutter App

Political Participation Platform - Flutter Frontend

## Getting Started

### Prerequisites
- Flutter SDK 3.x
- Dart SDK 3.x
- Android Studio / Xcode (for mobile development)
- Chrome (for web development)

### Installation

1. Install dependencies:
```bash
flutter pub get
```

2. Configure API endpoint in `lib/core/config/app_config.dart`

3. Run the app:
```bash
# Mobile
flutter run

# Web
flutter run -d chrome

# Specific device
flutter devices
flutter run -d <device-id>
```

### Build for Production

```bash
# Android
flutter build apk --release
flutter build appbundle --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## Features

- ✅ Authentication (Login/Register)
- ✅ Home Screen with Recommendations
- ✅ Bills List & Detail
- ✅ News List & Detail
- ✅ Bill Summarization
- ✅ News Analysis
- ✅ Profile Management
- ✅ Multi-language Support
- ✅ Clean Architecture
- ✅ State Management (Riverpod)

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── core/
│   ├── config/              # App configuration
│   ├── theme/               # App theme
│   └── router/              # Navigation
├── data/
│   ├── api/                 # API client
│   └── models/              # Data models
├── features/
│   ├── auth/                # Authentication
│   ├── home/                # Home screen
│   ├── bills/               # Bills feature
│   ├── news/                # News feature
│   └── profile/             # Profile
└── l10n/                    # Localization
```

## Contributing

See main project README for contribution guidelines.
