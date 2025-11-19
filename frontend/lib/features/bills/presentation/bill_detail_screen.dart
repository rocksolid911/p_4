import 'package:flutter/material.dart';
import '../../../data/api/api_client.dart';
import '../../../data/models/bill_model.dart';

class BillDetailScreen extends StatefulWidget {
  final int billId;

  const BillDetailScreen({super.key, required this.billId});

  @override
  State<BillDetailScreen> createState() => _BillDetailScreenState();
}

class _BillDetailScreenState extends State<BillDetailScreen> {
  int _selectedTab = 0;

  Future<BillModel> _loadBill() async {
    final response = await ApiClient().getBill(widget.billId);
    return BillModel.fromJson(response.data);
  }

  Future<void> _summarizeBill() async {
    try {
      await ApiClient().summarizeBill({
        'bill_id': widget.billId,
        'languages': ['en', 'hi'],
      });

      if (mounted) {
        setState(() {});
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Summary generated successfully')),
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
        title: const Text('Bill Details'),
      ),
      body: FutureBuilder<BillModel>(
        future: _loadBill(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final bill = snapshot.data!;

          return Column(
            children: [
              // Tabs
              Container(
                color: Theme.of(context).colorScheme.surface,
                child: Row(
                  children: [
                    Expanded(
                      child: TextButton(
                        onPressed: () => setState(() => _selectedTab = 0),
                        child: Text(
                          'Summary',
                          style: TextStyle(
                            color: _selectedTab == 0
                                ? Theme.of(context).colorScheme.primary
                                : null,
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: TextButton(
                        onPressed: () => setState(() => _selectedTab = 1),
                        child: Text(
                          'Full Text',
                          style: TextStyle(
                            color: _selectedTab == 1
                                ? Theme.of(context).colorScheme.primary
                                : null,
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: TextButton(
                        onPressed: () => setState(() => _selectedTab = 2),
                        child: Text(
                          'Analysis',
                          style: TextStyle(
                            color: _selectedTab == 2
                                ? Theme.of(context).colorScheme.primary
                                : null,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              // Content
              Expanded(
                child: _selectedTab == 0
                    ? _buildSummaryTab(bill)
                    : _selectedTab == 1
                        ? _buildFullTextTab(bill)
                        : _buildAnalysisTab(bill),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSummaryTab(BillModel bill) {
    if (bill.summaries.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('No summary available yet'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _summarizeBill,
              child: const Text('Generate Summary'),
            ),
          ],
        ),
      );
    }

    final summary = bill.summaries.first;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Summary',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(summary.summaryDetailed),
          const SizedBox(height: 24),
          if (summary.pros.isNotEmpty) ...[
            Text(
              'Pros',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            ...summary.pros.map((pro) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.check_circle, color: Colors.green, size: 20),
                      const SizedBox(width: 8),
                      Expanded(child: Text(pro)),
                    ],
                  ),
                )),
            const SizedBox(height: 16),
          ],
          if (summary.cons.isNotEmpty) ...[
            Text(
              'Cons',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            ...summary.cons.map((con) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.cancel, color: Colors.red, size: 20),
                      const SizedBox(width: 8),
                      Expanded(child: Text(con)),
                    ],
                  ),
                )),
          ],
        ],
      ),
    );
  }

  Widget _buildFullTextTab(BillModel bill) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Text(bill.fullText),
    );
  }

  Widget _buildAnalysisTab(BillModel bill) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildInfoRow('Parliament House', bill.parliamentHouseDisplay),
          _buildInfoRow('Status', bill.statusDisplay),
          if (bill.state != null) _buildInfoRow('State', bill.state!),
          if (bill.introducedOn != null)
            _buildInfoRow('Introduced On', bill.introducedOn.toString()),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}
