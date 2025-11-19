class NewsArticleModel {
  final int id;
  final String title;
  final String content;
  final String sourceUrl;
  final String sourceName;
  final DateTime? publishedAt;
  final List<String> topics;
  final String languageCode;
  final List<NewsAnalysisModel> analyses;
  final DateTime createdAt;

  NewsArticleModel({
    required this.id,
    required this.title,
    required this.content,
    required this.sourceUrl,
    required this.sourceName,
    this.publishedAt,
    required this.topics,
    required this.languageCode,
    required this.analyses,
    required this.createdAt,
  });

  factory NewsArticleModel.fromJson(Map<String, dynamic> json) {
    return NewsArticleModel(
      id: json['id'],
      title: json['title'],
      content: json['content'] ?? '',
      sourceUrl: json['source_url'],
      sourceName: json['source_name'],
      publishedAt: json['published_at'] != null
          ? DateTime.parse(json['published_at'])
          : null,
      topics: List<String>.from(json['topics'] ?? []),
      languageCode: json['language_code'] ?? 'en',
      analyses: (json['analyses'] as List?)
              ?.map((a) => NewsAnalysisModel.fromJson(a))
              .toList() ??
          [],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class NewsAnalysisModel {
  final int id;
  final String sentiment;
  final String leaning;
  final double propagandaScore;
  final String explanation;
  final bool emotionalLanguageDetected;
  final List<String> emotionalPhrases;
  final String languageCode;
  final DateTime createdAt;

  NewsAnalysisModel({
    required this.id,
    required this.sentiment,
    required this.leaning,
    required this.propagandaScore,
    required this.explanation,
    required this.emotionalLanguageDetected,
    required this.emotionalPhrases,
    required this.languageCode,
    required this.createdAt,
  });

  factory NewsAnalysisModel.fromJson(Map<String, dynamic> json) {
    return NewsAnalysisModel(
      id: json['id'],
      sentiment: json['sentiment'],
      leaning: json['leaning'],
      propagandaScore: (json['propaganda_score'] as num).toDouble(),
      explanation: json['explanation'],
      emotionalLanguageDetected: json['emotional_language_detected'] ?? false,
      emotionalPhrases: List<String>.from(json['emotional_phrases'] ?? []),
      languageCode: json['language_code'] ?? 'en',
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  String get sentimentDisplay {
    switch (sentiment) {
      case 'positive':
        return 'Positive';
      case 'negative':
        return 'Negative';
      default:
        return 'Neutral';
    }
  }

  String get leaningDisplay {
    switch (leaning) {
      case 'govt_leaning':
        return 'Government Leaning';
      case 'opposition_leaning':
        return 'Opposition Leaning';
      case 'neutral':
        return 'Neutral';
      default:
        return 'Unclear';
    }
  }
}
