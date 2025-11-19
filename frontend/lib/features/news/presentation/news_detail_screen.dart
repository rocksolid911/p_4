import 'package:flutter/material.dart';
import '../../../data/api/api_client.dart';
import '../../../data/models/news_model.dart';

class NewsDetailScreen extends StatefulWidget {
  final int newsId;

  const NewsDetailScreen({super.key, required this.newsId});

  @override
  State<NewsDetailScreen> createState() => _NewsDetailScreenState();
}

class _NewsDetailScreenState extends State<NewsDetailScreen> {
  Future<NewsArticleModel> _loadArticle() async {
    final response = await ApiClient().getNewsArticle(widget.newsId);
    return NewsArticleModel.fromJson(response.data);
  }

  Future<void> _analyzeArticle() async {
    try {
      await ApiClient().analyzeNews({
        'article_id': widget.newsId,
        'language': 'en',
      });

      if (mounted) {
        setState(() {});
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Analysis completed successfully')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${e.toString()}')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('News Article'),
      ),
      body: FutureBuilder<NewsArticleModel>(
        future: _loadArticle(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final article = snapshot.data!;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  article.title,
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  article.sourceName,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
                const SizedBox(height: 24),
                Text(article.content),
                const SizedBox(height: 24),
                if (article.analyses.isEmpty) ...[
                  ElevatedButton(
                    onPressed: _analyzeArticle,
                    child: const Text('Analyze This Article'),
                  ),
                ] else ...[
                  const Divider(),
                  const SizedBox(height: 16),
                  Text(
                    'Analysis',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 16),
                  _buildAnalysis(article.analyses.first),
                ],
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildAnalysis(NewsAnalysisModel analysis) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildAnalysisRow(
              'Sentiment',
              analysis.sentimentDisplay,
              _getSentimentColor(analysis.sentiment),
            ),
            const SizedBox(height: 12),
            _buildAnalysisRow(
              'Political Leaning',
              analysis.leaningDisplay,
              Colors.blue,
            ),
            const SizedBox(height: 12),
            _buildPropagandaScore(analysis.propagandaScore),
            const SizedBox(height: 16),
            Text(
              'Explanation',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            Text(analysis.explanation),
            if (analysis.emotionalLanguageDetected &&
                analysis.emotionalPhrases.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Emotional Phrases Detected',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              ...analysis.emotionalPhrases.map((phrase) => Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: Text('• $phrase'),
                  )),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildAnalysisRow(String label, String value, Color color) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: color.withOpacity(0.2),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Text(
            value,
            style: TextStyle(color: color, fontWeight: FontWeight.bold),
          ),
        ),
      ],
    );
  }

  Widget _buildPropagandaScore(double score) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Propaganda Score',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            Text(
              '${(score * 100).toStringAsFixed(0)}%',
              style: TextStyle(
                color: score > 0.7
                    ? Colors.red
                    : score > 0.4
                        ? Colors.orange
                        : Colors.green,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        LinearProgressIndicator(
          value: score,
          backgroundColor: Colors.grey[300],
          color: score > 0.7
              ? Colors.red
              : score > 0.4
                  ? Colors.orange
                  : Colors.green,
        ),
      ],
    );
  }

  Color _getSentimentColor(String sentiment) {
    switch (sentiment) {
      case 'positive':
        return Colors.green;
      case 'negative':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }
}
