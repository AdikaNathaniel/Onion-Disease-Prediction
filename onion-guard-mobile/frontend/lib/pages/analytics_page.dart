import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api_config.dart';
import '../config/app_theme.dart';

class AnalyticsPage extends StatefulWidget {
  const AnalyticsPage({super.key});

  @override
  State<AnalyticsPage> createState() => _AnalyticsPageState();
}

class _AnalyticsPageState extends State<AnalyticsPage> {
  Map<String, dynamic>? _summary;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAnalytics();
  }

  Future<void> _loadAnalytics() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final email = prefs.getString('user_email') ?? '';
      final resp = await http.get(Uri.parse(ApiConfig.analyticsSummary(email)));
      final data = json.decode(resp.body);
      if (data['success'] == true && mounted) {
        setState(() { _summary = data['summary']; _isLoading = false; });
      }
    } catch (_) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const Center(child: CircularProgressIndicator());
    if (_summary == null) {
      return const Center(child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.analytics, size: 80, color: Colors.grey),
          SizedBox(height: 16),
          Text('No analytics data yet', style: TextStyle(fontSize: 16, color: Colors.grey)),
          Text('Start scanning to see your stats', style: TextStyle(fontSize: 14, color: Colors.grey)),
        ],
      ));
    }

    final total = _summary!['total_scans'] ?? 0;
    final healthy = _summary!['healthy_count'] ?? 0;
    final diseased = _summary!['disease_count'] ?? 0;
    final distribution = (_summary!['disease_distribution'] as Map?) ?? {};

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Your Farm Analytics', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),

          // Stats Cards
          Row(children: [
            _statCard('Total Scans', '$total', Icons.qr_code_scanner, Colors.blue),
            const SizedBox(width: 12),
            _statCard('Healthy', '$healthy', Icons.check_circle, Colors.green),
            const SizedBox(width: 12),
            _statCard('Diseased', '$diseased', Icons.warning, Colors.red),
          ]),
          const SizedBox(height: 24),

          // Disease Distribution
          if (distribution.isNotEmpty) ...[
            const Text('Disease Distribution', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ...distribution.entries.map((e) {
              final count = e.value['count'] ?? 0;
              final pct = total > 0 ? count / total : 0.0;
              return Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                      Text(e.key.toString().replaceAll('_', ' '), style: const TextStyle(fontWeight: FontWeight.w500)),
                      Text('$count scans', style: const TextStyle(color: Colors.grey)),
                    ]),
                    const SizedBox(height: 4),
                    LinearProgressIndicator(
                      value: pct.toDouble(),
                      backgroundColor: Colors.grey.shade200,
                      valueColor: AlwaysStoppedAnimation(e.key == 'Healthy' ? Colors.green : Colors.orange),
                      minHeight: 10,
                      borderRadius: BorderRadius.circular(5),
                    ),
                  ],
                ),
              );
            }),
          ],
        ],
      ),
    );
  }

  Widget _statCard(String label, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 8),
          Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
          Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ]),
      ),
    );
  }
}
