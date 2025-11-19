# LokSathi - Political Participation Platform for India

> Empowering citizens to participate in democracy through technology

LokSathi is a production-ready political participation platform designed to increase civic engagement in India by providing simple bill summaries, news bias detection, and personalized content recommendations.

## 🎯 Features

### 1. Bill & Policy Summarizer
- Upload or select legislative bills
- Generate summaries in multiple Indian languages (English, Hindi, Marathi, Telugu, Tamil, etc.)
- View key points, pros, and cons in simple language
- Track bill status and history

### 2. News Bias & Sentiment Checker
- Analyze news articles for sentiment (Positive/Neutral/Negative)
- Detect political leaning (Government/Opposition/Neutral)
- Identify propaganda and emotionally charged language
- Get clear explanations for classifications

### 3. Personalized Content Recommendations
- PostgresML-powered recommendation engine
- Content based on user interests and reading history
- Mix of bills and news articles
- Intelligent topic matching

### 4. Multi-language Support
- UI available in English and Hindi
- Content summaries in 8+ Indian languages
- Easy extension for additional languages

### 5. User Profiles & Analytics
- Profile with state, district, and interests
- Role-based access (Citizen/Researcher/Admin)
- Mixpanel analytics for engagement tracking

## 🏗️ Architecture

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL with PostgresML extension
- **Authentication**: JWT-based (djangorestframework-simplejwt)
- **AI/LLM**: Modular service layer (supports OpenAI, etc.)
- **Analytics**: Mixpanel integration

### Frontend
- **Framework**: Flutter 3.x (Mobile + Web)
- **State Management**: Riverpod
- **Architecture**: Clean Architecture (Data/Domain/Presentation layers)
- **Localization**: Flutter's official l10n system

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL with PostgresML
- **Web Server**: Gunicorn + WhiteNoise (production)

## 📋 Project Structure

```
loksathi/
├── backend/                      # Django backend
│   ├── loksathi_backend/         # Main Django project
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # URL routing
│   │   └── wsgi.py              # WSGI config
│   ├── accounts/                 # User authentication & profiles
│   │   ├── models.py            # Custom User model
│   │   ├── serializers.py       # DRF serializers
│   │   ├── views.py             # Auth endpoints
│   │   └── tests.py             # Unit tests
│   ├── content/                  # Bills & News models
│   │   ├── models.py            # Bill, BillSummary, NewsArticle, etc.
│   │   ├── serializers.py       # Content serializers
│   │   └── views.py             # Content viewsets
│   ├── analysis/                 # AI analysis services
│   │   ├── services/
│   │   │   ├── bill_summarizer.py    # Bill summarization
│   │   │   ├── news_analyzer.py      # News bias detection
│   │   │   └── llm_provider.py       # LLM abstraction
│   │   └── views.py             # Analysis endpoints
│   ├── recommendation/           # PostgresML recommendations
│   │   ├── services.py          # Recommendation engine
│   │   └── views.py             # Recommendation endpoints
│   ├── analytics/                # Mixpanel integration
│   │   └── mixpanel_client.py   # Analytics utilities
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Docker configuration
│   └── .env.example             # Environment variables template
├── frontend/                     # Flutter frontend
│   ├── lib/
│   │   ├── main.dart            # App entry point
│   │   ├── core/
│   │   │   ├── config/          # App configuration
│   │   │   ├── theme/           # App theming
│   │   │   └── router/          # Navigation
│   │   ├── data/
│   │   │   ├── api/             # API client
│   │   │   └── models/          # Data models
│   │   ├── features/
│   │   │   ├── auth/            # Authentication screens
│   │   │   ├── home/            # Home screen
│   │   │   ├── bills/           # Bills feature
│   │   │   ├── news/            # News feature
│   │   │   └── profile/         # Profile screen
│   │   └── l10n/                # Localization
│   └── pubspec.yaml             # Flutter dependencies
└── docker-compose.yml           # Docker Compose config
```

## 🚀 Getting Started

### Prerequisites

- **Backend**:
  - Docker & Docker Compose
  - Python 3.11+ (for local development)
  - PostgreSQL 14+

- **Frontend**:
  - Flutter SDK 3.x
  - Dart SDK 3.x

### Backend Setup

#### Option 1: Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd loksathi
   ```

2. **Create environment file**:
   ```bash
   cd backend
   cp .env.example .env
   ```

3. **Edit `.env` with your configuration**:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=loksathi_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   MIXPANEL_TOKEN=your-mixpanel-token
   OPENAI_API_KEY=your-openai-api-key
   ```

4. **Start services**:
   ```bash
   cd ..  # Back to project root
   docker-compose up -d
   ```

5. **Create superuser**:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Access the application**:
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

#### Option 2: Local Development

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL** (install PostgresML separately if needed)

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   flutter pub get
   ```

3. **Update API URL** in `lib/core/config/app_config.dart`:
   ```dart
   static const String baseUrl = 'http://localhost:8000/api';
   ```

4. **Run the app**:

   For mobile:
   ```bash
   flutter run
   ```

   For web:
   ```bash
   flutter run -d chrome
   ```

### Running Tests

**Backend**:
```bash
cd backend
pytest
```

**Frontend**:
```bash
cd frontend
flutter test
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Bills
- `GET /api/bills/` - List bills (with filters)
- `GET /api/bills/{id}/` - Get bill details
- `POST /api/analysis/bills/summarize/` - Summarize a bill

### News
- `GET /api/news/` - List news articles
- `GET /api/news/{id}/` - Get article details
- `POST /api/analysis/news/analyze/` - Analyze news article

### Recommendations
- `GET /api/recommendations/?limit=20` - Get personalized recommendations

### Example API Calls

**Register User**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "Test User",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "state": "Maharashtra",
    "preferred_languages": ["en", "hi"],
    "interests": ["Economy", "Education"]
  }'
```

**Summarize Bill**:
```bash
curl -X POST http://localhost:8000/api/analysis/bills/summarize/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "bill_id": 1,
    "languages": ["en", "hi"]
  }'
```

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=loksathi_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Analytics
MIXPANEL_TOKEN=your-token

# AI/LLM
OPENAI_API_KEY=your-api-key
LLM_PROVIDER=openai

# PostgresML
PGML_ENABLED=True
```

**Frontend**:
Update `lib/core/config/app_config.dart`:
```dart
static const String baseUrl = 'your-api-url';
static const String mixpanelToken = 'your-token';
```

## 🔐 Security Considerations

1. **JWT Authentication**: All protected endpoints require JWT tokens
2. **Password Hashing**: Using Django's built-in password hashing
3. **CORS**: Configure `CORS_ALLOWED_ORIGINS` for production
4. **Environment Variables**: Never commit `.env` files
5. **Input Validation**: All inputs validated via DRF serializers
6. **SQL Injection**: Protected via Django ORM

## 📊 Analytics Events

The following events are tracked via Mixpanel:

- `user_registered` - User signs up
- `user_logged_in` - User logs in
- `bill_viewed` - User views a bill
- `bill_summarized` - Bill summary generated
- `news_article_viewed` - User views news article
- `news_article_analyzed` - News article analyzed
- `content_recommended` - Recommendations shown
- `content_{interaction}` - User interactions (like, save, share)

## 🌐 Supported Languages

- English (en)
- Hindi (hi)
- Marathi (mr)
- Telugu (te)
- Tamil (ta)
- Bengali (bn)
- Gujarati (gu)
- Kannada (kn)

## 🚢 Deployment

### Production Checklist

1. **Backend**:
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Set strong `SECRET_KEY`
   - Configure CORS properly
   - Set up PostgreSQL with proper credentials
   - Configure LLM API keys
   - Set up Mixpanel token
   - Run `python manage.py collectstatic`

2. **Frontend**:
   - Update `baseUrl` to production API
   - Configure Mixpanel token
   - Build for production: `flutter build apk/web/ios`

3. **Database**:
   - Regular backups
   - PostgresML extension installed
   - Proper indexing for performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

This project is proprietary. All rights reserved.

## 👥 Team

- Backend Development
- Frontend Development
- AI/ML Integration
- DevOps & Infrastructure

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: support@loksathi.in

## 🙏 Acknowledgments

- Django REST Framework
- Flutter Team
- PostgresML
- OpenAI
- Mixpanel

---

**Built with ❤️ for Indian democracy**
