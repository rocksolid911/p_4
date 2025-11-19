import 'package:flutter/material.dart';
import '../../../core/router/app_router.dart';
import '../../../data/api/api_client.dart';
import '../../../data/models/bill_model.dart';

class BillsListScreen extends StatefulWidget {
  const BillsListScreen({super.key});

  @override
  State<BillsListScreen> createState() => _BillsListScreenState();
}

class _BillsListScreenState extends State<BillsListScreen> {
  Future<List<BillModel>> _loadBills() async {
    try {
      final response = await ApiClient().getBills();
      return (response.data['results'] as List)
          .map((json) => BillModel.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bills & Policies'),
      ),
      body: FutureBuilder<List<BillModel>>(
        future: _loadBills(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final bills = snapshot.data ?? [];

          if (bills.isEmpty) {
            return const Center(child: Text('No bills available'));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: bills.length,
            itemBuilder: (context, index) {
              final bill = bills[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                child: ListTile(
                  title: Text(bill.title),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 4),
                      Text('${bill.parliamentHouseDisplay} • ${bill.statusDisplay}'),
                      if (bill.topics.isNotEmpty) ...[
                        const SizedBox(height: 4),
                        Wrap(
                          spacing: 4,
                          children: bill.topics
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
                      AppRouter.billDetail,
                      arguments: bill.id,
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
