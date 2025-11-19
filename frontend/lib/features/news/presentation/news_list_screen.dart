import 'package:flutter/material.dart';
import '../../../core/router/app_router.dart';
import '../../../data/api/api_client.dart';
import '../../../data/models/news_model.dart';

class NewsListScreen extends StatefulWidget {
  const NewsListScreen({super.key});

  @override
  State<NewsListScreen> createState() => _NewsListScreenState();
}

class _NewsListScreenState extends State<NewsListScreen> {
  Future<List<NewsArticleModel>> _loadNews() async {
    try {
      final response = await ApiClient().getNews();
      return (response.data['results'] as List)
          .map((json) => NewsArticleModel.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('News Articles'),
      ),
      body: FutureBuilder<List<NewsArticleModel>>(
        future: _loadNews(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final news = snapshot.data ?? [];

          if (news.isEmpty) {
            return const Center(child: Text('No news articles available'));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: news.length,
            itemBuilder: (context, index) {
              final article = news[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                child: ListTile(
                  title: Text(article.title),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 4),
                      Text(article.sourceName),
                      if (article.topics.isNotEmpty) ...[
                        const SizedBox(height: 4),
                        Wrap(
                          spacing: 4,
                          children: article.topics
                              .take(3)
                              .map((topic) => Chip(
                                    label: Text(topic),
                                    materialTapTargetSize:
                                        MaterialTapTargetSize.shrinkWrap,
                                  ))
                              .toList(),
                        ),
                      ],
                    ],
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () {
                    Navigator.of(context).pushNamed(
                      AppRouter.newsDetail,
                      arguments: article.id,
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
