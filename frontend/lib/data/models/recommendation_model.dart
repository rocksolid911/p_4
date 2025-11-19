class RecommendationModel {
  final String type; // 'bill' or 'news'
  final int id;
  final String title;
  final double score;
  final String reason;
  final dynamic content; // BillModel or NewsArticleModel

  RecommendationModel({
    required this.type,
    required this.id,
    required this.title,
    required this.score,
    required this.reason,
    this.content,
  });

  factory RecommendationModel.fromJson(Map<String, dynamic> json) {
    return RecommendationModel(
      type: json['type'],
      id: json['id'],
      title: json['title'],
      score: (json['score'] as num).toDouble(),
      reason: json['reason'],
      content: json['content'],
    );
  }

  bool get isBill => type == 'bill';
  bool get isNews => type == 'news';
}
