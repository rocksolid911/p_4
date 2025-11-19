import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/router/app_router.dart';
import '../../../data/api/api_client.dart';
import '../../../data/models/recommendation_model.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const RecommendationsTab(),
    const BillsTab(),
    const NewsTab(),
    const ToolsTab(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LokSathi'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {
              Navigator.of(context).pushNamed(AppRouter.profile);
            },
          ),
        ],
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home),
            label: 'For You',
          ),
          NavigationDestination(
            icon: Icon(Icons.article),
            label: 'Bills',
          ),
          NavigationDestination(
            icon: Icon(Icons.newspaper),
            label: 'News',
          ),
          NavigationDestination(
            icon: Icon(Icons.tools),
            label: 'Tools',
          ),
        ],
      ),
    );
  }
}

class RecommendationsTab extends StatelessWidget {
  const RecommendationsTab({super.key});

  Future<List<RecommendationModel>> _loadRecommendations() async {
    try {
      final response = await ApiClient().getRecommendations();
      return (response.data as List)
          .map((json) => RecommendationModel.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<RecommendationModel>>(
      future: _loadRecommendations(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }

        if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        }

        final recommendations = snapshot.data ?? [];

        if (recommendations.isEmpty) {
          return const Center(child: Text('No recommendations yet'));
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: recommendations.length,
          itemBuilder: (context, index) {
            final rec = recommendations[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 16),
              child: ListTile(
                title: Text(rec.title),
                subtitle: Text(rec.reason),
                leading: Icon(
                  rec.isBill ? Icons.article : Icons.newspaper,
                  color: Theme.of(context).colorScheme.primary,
                ),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: () {
                  if (rec.isBill) {
                    Navigator.of(context).pushNamed(
                      AppRouter.billDetail,
                      arguments: rec.id,
                    );
                  } else {
                    Navigator.of(context).pushNamed(
                      AppRouter.newsDetail,
                      arguments: rec.id,
                    );
                  }
                },
              ),
            );
          },
        );
      },
    );
  }
}

class BillsTab extends StatelessWidget {
  const BillsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ElevatedButton(
        onPressed: () {
          Navigator.of(context).pushNamed(AppRouter.bills);
        },
        child: const Text('View All Bills'),
      ),
    );
  }
}

class NewsTab extends StatelessWidget {
  const NewsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ElevatedButton(
        onPressed: () {
          Navigator.of(context).pushNamed(AppRouter.news);
        },
        child: const Text('View All News'),
      ),
    );
  }
}

class ToolsTab extends StatelessWidget {
  const ToolsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: ListTile(
            leading: const Icon(Icons.summarize),
            title: const Text('Summarize Bill'),
            subtitle: const Text('Get simple summaries of complex bills'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              Navigator.of(context).pushNamed(AppRouter.bills);
            },
          ),
        ),
        const SizedBox(height: 16),
        Card(
          child: ListTile(
            leading: const Icon(Icons.analytics),
            title: const Text('Analyze News'),
            subtitle: const Text('Detect bias and sentiment in news articles'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              Navigator.of(context).pushNamed(AppRouter.news);
            },
          ),
        ),
      ],
    );
  }
}
