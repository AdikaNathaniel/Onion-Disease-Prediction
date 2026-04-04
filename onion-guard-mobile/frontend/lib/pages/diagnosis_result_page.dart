import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/app_theme.dart';
import '../providers/language_provider.dart';
import 'treatment_page.dart';

class DiagnosisResultPage extends StatelessWidget {
  final String imagePath;
  final String diseaseName;
  final double confidence;
  final Map<String, dynamic> allPredictions;

  const DiagnosisResultPage({
    super.key,
    required this.imagePath,
    required this.diseaseName,
    required this.confidence,
    required this.allPredictions,
  });

  Color get _severityColor {
    if (diseaseName == 'Healthy') return Colors.green;
    if (confidence > 90) return Colors.red;
    if (confidence > 70) return Colors.orange;
    return Colors.yellow.shade700;
  }

  String get _severityLabel {
    if (diseaseName == 'Healthy') return 'No Disease Detected';
    if (confidence > 90) return 'High Confidence';
    if (confidence > 70) return 'Moderate Confidence';
    return 'Low Confidence';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Diagnosis Result'), backgroundColor: AppTheme.primaryGreen),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.file(File(imagePath), height: 250, width: double.infinity, fit: BoxFit.cover),
            ),
            const SizedBox(height: 20),

            // Disease Name
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: _severityColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: _severityColor, width: 2),
              ),
              child: Column(
                children: [
                  Icon(diseaseName == 'Healthy' ? Icons.check_circle : Icons.warning, size: 50, color: _severityColor),
                  const SizedBox(height: 12),
                  Text(diseaseName.replaceAll('_', ' '), style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: _severityColor)),
                  const SizedBox(height: 8),
                  Text('${confidence.toStringAsFixed(1)}% ${context.read<LanguageProvider>().t('confidence')}', style: const TextStyle(fontSize: 18, color: Colors.grey)),
                  const SizedBox(height: 4),
                  Text(_severityLabel, style: TextStyle(fontSize: 14, color: _severityColor, fontWeight: FontWeight.w600)),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Confidence Bar
            const Text('All Predictions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ...allPredictions.entries.map((e) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(e.key.toString().replaceAll('_', ' '), style: const TextStyle(fontSize: 13)),
                      Text('${(e.value as num).toStringAsFixed(1)}%', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 4),
                  LinearProgressIndicator(
                    value: (e.value as num) / 100,
                    backgroundColor: Colors.grey.shade200,
                    valueColor: AlwaysStoppedAnimation(e.key == diseaseName ? _severityColor : Colors.grey),
                    minHeight: 8,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ],
              ),
            )),
            const SizedBox(height: 24),

            // Treatment Button
            if (diseaseName != 'Healthy')
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(
                    builder: (_) => TreatmentPage(diseaseName: diseaseName),
                  )),
                  icon: const Icon(Icons.medical_services),
                  label: Text(context.read<LanguageProvider>().t('view_treatment'), style: const TextStyle(fontSize: 18)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
