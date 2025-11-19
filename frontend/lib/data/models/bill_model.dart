class BillModel {
  final int id;
  final String title;
  final String fullText;
  final String? sourceUrl;
  final String parliamentHouse;
  final DateTime? introducedOn;
  final String status;
  final String? state;
  final List<String> topics;
  final List<BillSummaryModel> summaries;
  final DateTime createdAt;

  BillModel({
    required this.id,
    required this.title,
    required this.fullText,
    this.sourceUrl,
    required this.parliamentHouse,
    this.introducedOn,
    required this.status,
    this.state,
    required this.topics,
    required this.summaries,
    required this.createdAt,
  });

  factory BillModel.fromJson(Map<String, dynamic> json) {
    return BillModel(
      id: json['id'],
      title: json['title'],
      fullText: json['full_text'] ?? '',
      sourceUrl: json['source_url'],
      parliamentHouse: json['parliament_house'],
      introducedOn: json['introduced_on'] != null
          ? DateTime.parse(json['introduced_on'])
          : null,
      status: json['status'],
      state: json['state'],
      topics: List<String>.from(json['topics'] ?? []),
      summaries: (json['summaries'] as List?)
              ?.map((s) => BillSummaryModel.fromJson(s))
              .toList() ??
          [],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  String get parliamentHouseDisplay {
    switch (parliamentHouse) {
      case 'lok_sabha':
        return 'Lok Sabha';
      case 'rajya_sabha':
        return 'Rajya Sabha';
      case 'state_assembly':
        return 'State Assembly';
      default:
        return 'Other';
    }
  }

  String get statusDisplay {
    switch (status) {
      case 'introduced':
        return 'Introduced';
      case 'in_committee':
        return 'In Committee';
      case 'passed_lower':
        return 'Passed Lower House';
      case 'passed_upper':
        return 'Passed Upper House';
      case 'enacted':
        return 'Enacted';
      case 'rejected':
        return 'Rejected';
      case 'withdrawn':
        return 'Withdrawn';
      default:
        return status;
    }
  }
}

class BillSummaryModel {
  final int id;
  final String languageCode;
  final String summaryShort;
  final String summaryDetailed;
  final List<String> pros;
  final List<String> cons;
  final List<String> keyPoints;
  final DateTime createdAt;

  BillSummaryModel({
    required this.id,
    required this.languageCode,
    required this.summaryShort,
    required this.summaryDetailed,
    required this.pros,
    required this.cons,
    required this.keyPoints,
    required this.createdAt,
  });

  factory BillSummaryModel.fromJson(Map<String, dynamic> json) {
    return BillSummaryModel(
      id: json['id'],
      languageCode: json['language_code'],
      summaryShort: json['summary_short'],
      summaryDetailed: json['summary_detailed'],
      pros: List<String>.from(json['pros'] ?? []),
      cons: List<String>.from(json['cons'] ?? []),
      keyPoints: List<String>.from(json['key_points'] ?? []),
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
