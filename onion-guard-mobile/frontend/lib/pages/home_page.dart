import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../config/app_theme.dart';
import '../providers/language_provider.dart';
import '../services/auth_service.dart';
import '../services/diagnosis_service.dart';
import '../models/user_model.dart';
import '../widgets/onion_dialog.dart';
import 'diagnosis_result_page.dart';
import 'analytics_page.dart';
import 'freshness_page.dart';
import 'settings_page.dart';
import 'login_page.dart';

class HomePage extends StatefulWidget {
  final String userEmail;
  const HomePage({super.key, required this.userEmail});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _authService = AuthService();
  final _diagnosisService = DiagnosisService();
  final _picker = ImagePicker();
  UserModel? _user;
  int _currentIndex = 0;
  bool _isScanning = false;

  @override
  void initState() {
    super.initState();
    _loadUser();
    _diagnosisService.loadModel().catchError((_) {});
  }

  Future<void> _loadUser() async {
    final user = await _authService.getSavedUser();
    if (mounted) setState(() => _user = user);
  }

  @override
  Widget build(BuildContext context) {
    final lang = context.watch<LanguageProvider>();
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        final shouldLogout = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            title: Text(lang.t('logout')),
            content: Text(lang.t('do_you_want_logout')),
            actions: [
              TextButton(onPressed: () => Navigator.pop(ctx, false), child: Text(lang.t('no'))),
              ElevatedButton(
                onPressed: () => Navigator.pop(ctx, true),
                style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
                child: Text(lang.t('yes')),
              ),
            ],
          ),
        );
        if (shouldLogout == true && mounted) {
          await _authService.logout();
          if (mounted) Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const LoginPage()));
        }
      },
      child: Scaffold(
      appBar: AppBar(
        title: Text(lang.t('app_title')),
        automaticallyImplyLeading: false,
        backgroundColor: AppTheme.primaryGreen,
        actions: [
          IconButton(icon: const Icon(Icons.settings), onPressed: () {
            Navigator.push(context, MaterialPageRoute(builder: (_) => SettingsPage(userEmail: widget.userEmail)));
          }),
        ],
      ),
      body: [_buildHome(), const FreshnessPage(), _buildHistory(), const AnalyticsPage()][_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        selectedItemColor: AppTheme.primaryGreen,
        unselectedItemColor: Colors.grey,
        type: BottomNavigationBarType.fixed,
        onTap: (i) => setState(() => _currentIndex = i),
        items: [
          BottomNavigationBarItem(icon: const Icon(Icons.home), label: lang.t('home')),
          BottomNavigationBarItem(icon: const Icon(Icons.spa), label: lang.t('freshness')),
          BottomNavigationBarItem(icon: const Icon(Icons.history), label: lang.t('history')),
          BottomNavigationBarItem(icon: const Icon(Icons.analytics), label: lang.t('analytics')),
        ],
      ),
    ));
  }

  Widget _buildHome() {
    final lang = context.read<LanguageProvider>();
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Welcome Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: AppTheme.backgroundGradient,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${lang.t('welcome')}, ${_user?.name ?? 'Farmer'}!',
                      style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 8),
                  Text(lang.t('protect_crops'), style: const TextStyle(color: Colors.white70, fontSize: 14)),
                ],
              ),
            ),
            const SizedBox(height: 40),

            // Big Scan Button
            SizedBox(
              width: double.infinity,
              height: 180,
              child: ElevatedButton(
                onPressed: _isScanning ? null : _scanDisease,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGreen,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  elevation: 6,
                ),
                child: _isScanning
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.camera_alt, size: 56),
                          const SizedBox(height: 12),
                          Text(lang.t('scan_disease'), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 6),
                          Text(lang.t('take_photo'), style: const TextStyle(fontSize: 14, color: Colors.white70)),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 20),

            // Gallery button
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: _isScanning ? null : _pickFromGallery,
                icon: const Icon(Icons.photo_library),
                label: Text(lang.t('gallery'), style: const TextStyle(fontSize: 16)),
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppTheme.primaryGreen,
                  side: const BorderSide(color: AppTheme.primaryGreen, width: 2),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHistory() {
    final lang = context.read<LanguageProvider>();
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.history, size: 80, color: Colors.grey),
          const SizedBox(height: 16),
          Text(lang.t('scan_history_empty'), style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ],
      ),
    );
  }

  Future<void> _scanDisease() async {
    final image = await _picker.pickImage(source: ImageSource.camera, imageQuality: 85);
    if (image == null) return;
    await _processImage(File(image.path));
  }

  Future<void> _pickFromGallery() async {
    final image = await _picker.pickImage(source: ImageSource.gallery, imageQuality: 85);
    if (image == null) return;
    await _processImage(File(image.path));
  }

  Future<void> _processImage(File imageFile) async {
    setState(() => _isScanning = true);
    try {
      final result = await _diagnosisService.classifyImage(imageFile);
      if (mounted) {
        Navigator.push(context, MaterialPageRoute(
          builder: (_) => DiagnosisResultPage(
            imagePath: imageFile.path,
            diseaseName: result['class_name'],
            confidence: result['confidence'],
            allPredictions: result['all_predictions'],
          ),
        ));
      }
    } catch (e) {
      if (mounted) OnionDialog.showError(context, title: 'Scan Failed', message: 'Could not analyze image: $e');
    } finally {
      if (mounted) setState(() => _isScanning = false);
    }
  }
}
