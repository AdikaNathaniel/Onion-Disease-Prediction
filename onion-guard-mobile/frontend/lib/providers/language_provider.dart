import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageProvider extends ChangeNotifier {
  String _languageCode = 'en';

  String get code => _languageCode;

  LanguageProvider() {
    _loadLanguage();
  }

  Future<void> _loadLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    _languageCode = prefs.getString('language') ?? 'en';
    notifyListeners();
  }

  Future<void> setLanguage(String code) async {
    _languageCode = code;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language', code);
    notifyListeners();
  }

  /// Translate a key using the built-in dictionary.
  /// Falls back to English, then to the key itself.
  String t(String key) {
    return _translations[key]?[_languageCode] ?? _translations[key]?['en'] ?? key;
  }

  static const Map<String, Map<String, String>> _translations = {
    // App
    'app_title': {
      'en': 'OnionGuard', 'tw': 'OnionGuard', 'dg': 'OnionGuard', 'ee': 'OnionGuard', 'ha': 'OnionGuard',
    },

    // Navbar
    'home': {
      'en': 'Home', 'tw': 'Fie', 'dg': 'Yili', 'ee': 'Aƒe', 'ha': 'Gida',
    },
    'freshness': {
      'en': 'Freshness', 'tw': 'Foforɔ', 'dg': 'Palli', 'ee': 'Yeye', 'ha': 'Sabo',
    },
    'history': {
      'en': 'History', 'tw': 'Abakɔsɛm', 'dg': 'Tarihi', 'ee': 'Nutinya', 'ha': 'Tarihi',
    },
    'analytics': {
      'en': 'Analytics', 'tw': 'Nsɛm ahorow', 'dg': 'Yɛltɔɣa', 'ee': 'Numeɖeɖe', 'ha': 'Nazari',
    },

    // Home page
    'welcome': {
      'en': 'Welcome', 'tw': 'Akwaaba', 'dg': 'Anlaibiisim', 'ee': 'Woezon', 'ha': 'Sannu',
    },
    'protect_crops': {
      'en': 'Protect your onion crops with AI', 'tw': 'Bɔ wo gyeene nnɔbae ho ban de AI', 'dg': 'Di a gabuŋ alubosa din pam', 'ee': 'Dzɔ wo sabala numedodowo', 'ha': 'Kare albasa da AI',
    },
    'scan_disease': {
      'en': 'Scan Disease', 'tw': 'Hwehwɛ Nyarewa', 'dg': 'Daliri Bɛhigu', 'ee': 'Dɔlele Didi', 'ha': 'Bincika Cuta',
    },
    'take_photo': {
      'en': 'Take a photo of your onion plant', 'tw': 'Fa wo gyeene dua no foto', 'dg': 'Lahi a alubosa tihi foto', 'ee': 'Ɖe wo sabala fotoɖeka', 'ha': 'Ɗauki hoton albasa ka',
    },
    'gallery': {
      'en': 'Gallery', 'tw': 'Mfonini', 'dg': 'Foto doo', 'ee': 'Nufotowo', 'ha': 'Hoto',
    },
    'stats': {
      'en': 'Stats', 'tw': 'Akontaabu', 'dg': 'Yɛltɔɣa', 'ee': 'Akɔntawo', 'ha': 'Ƙididdiga',
    },
    'quick_actions': {
      'en': 'Quick Actions', 'tw': 'Dwumadie ntɛm', 'dg': 'Tuma salima', 'ee': 'Dɔwɔwɔ kabakaba', 'ha': 'Ayyuka cikin sauri',
    },

    // Freshness page
    'freshness_check': {
      'en': 'Freshness Check', 'tw': 'Foforɔ hwehwɛ', 'dg': 'Palli daliri', 'ee': 'Yeye kpɔkpɔ', 'ha': 'Binciken sabo',
    },
    'freshness_desc': {
      'en': 'Check if your onion is fresh, almost spoilt, or rotten', 'tw': 'Hwɛ sɛ wo gyeene no yɛ foforɔ, ɛrebɛsɛe, anaasɛ aporɔw', 'dg': 'Nyɛli ka a alubosa palli bee ka di bɔri', 'ee': 'Kpɔ ne wo sabala le yeye, ale adzɔ, alo adzɔ', 'ha': 'Duba ko albasa ka sabo ne, kusa ta lalace, ko ta lalace',
    },
    'camera': {
      'en': 'Camera', 'tw': 'Kamera', 'dg': 'Kamera', 'ee': 'Kamera', 'ha': 'Kyamara',
    },
    'analyzing': {
      'en': 'Analyzing freshness...', 'tw': 'Ɛrehwehwɛ foforɔ...', 'dg': 'Daliri palli...', 'ee': 'Le yeye kpɔm...', 'ha': 'Ana bincike...',
    },
    'analysis': {
      'en': 'Analysis', 'tw': 'Nhwehwɛmu', 'dg': 'Daliri', 'ee': 'Numeɖeɖe', 'ha': 'Bincike',
    },
    'tips': {
      'en': 'Tips', 'tw': 'Afotu', 'dg': 'Wuntarigu', 'ee': 'Aɖaŋuwo', 'ha': 'Shawarwari',
    },

    // Login / Register
    'login': {
      'en': 'Login', 'tw': 'Wura mu', 'dg': 'Kpe niŋ', 'ee': 'Ge eme', 'ha': 'Shiga',
    },
    'register': {
      'en': 'Register', 'tw': 'Kyerɛw din', 'dg': 'Sabi din', 'ee': 'Ŋlɔ ŋkɔ', 'ha': 'Yi rajista',
    },
    'create_account': {
      'en': 'Create Account', 'tw': 'Bue akawnt', 'dg': 'Mali akawnt', 'ee': 'Ŋlɔ ŋkɔ', 'ha': 'Buɗe asusu',
    },
    'email': {
      'en': 'Email', 'tw': 'Email', 'dg': 'Email', 'ee': 'Email', 'ha': 'Imel',
    },
    'password': {
      'en': 'Password', 'tw': 'Nsɛmfua', 'dg': 'Password', 'ee': 'Ŋkugbalẽ', 'ha': 'Kalmar wucewa',
    },
    'full_name': {
      'en': 'Full Name', 'tw': 'Din nyinaa', 'dg': 'Yulin yuuli', 'ee': 'Ŋkɔ blibo', 'ha': 'Suna cikakke',
    },
    'username': {
      'en': 'Username', 'tw': 'Din', 'dg': 'Yuuli', 'ee': 'Ŋkɔ', 'ha': 'Sunan mai amfani',
    },
    'phone': {
      'en': 'Phone Number', 'tw': 'Fon nɔma', 'dg': 'Tilifon nɔmba', 'ee': 'Fon dzia', 'ha': 'Lambar waya',
    },
    'user_type': {
      'en': 'User Type', 'tw': 'Dwumadie', 'dg': 'Tumda buɣili', 'ee': 'Dɔwɔla ƒomevi', 'ha': 'Irin mai amfani',
    },
    'language': {
      'en': 'Language', 'tw': 'Kasa', 'dg': 'Zili', 'ee': 'Gbe', 'ha': 'Harshe',
    },
    'no_account': {
      'en': "Don't have an account? Register here", 'tw': 'Wonni akawnt? Kyerɛw din wɔ ha', 'dg': 'Ka n nyɛ akawnt? Sabi din kani', 'ee': 'Mele akawnt aɖeke o? Ŋlɔ ŋkɔ le afisia', 'ha': 'Ba ka asusu ba? Yi rajista a nan',
    },
    'have_account': {
      'en': 'Already have an account? Login', 'tw': 'Wowɔ akawnt dada? Wura mu', 'dg': 'Ka nyɛla ni akawnt? Kpe niŋ', 'ee': 'Ele akawnt xoxo? Ge eme', 'ha': 'Kana da asusu? Shiga',
    },
    'forgot_password': {
      'en': 'Forgot Your Password?', 'tw': 'Wo werɛ afi wo nsɛmfua?', 'dg': 'Ka che yɛlimi a password?', 'ee': 'Ŋkugbalẽ ŋutɔ wò?', 'ha': 'Ka manta kalmar wucewa?',
    },
    'login_biometric': {
      'en': 'Login with Biometrics', 'tw': 'Fa nsateaa wura mu', 'dg': 'Kpe niŋ ni biometric', 'ee': 'Ge eme kple biometric', 'ha': 'Shiga da biometric',
    },

    // Settings
    'settings': {
      'en': 'Settings', 'tw': 'Nhyehyɛe', 'dg': 'Zaŋli', 'ee': 'Ɖoɖo', 'ha': 'Saiti',
    },
    'security': {
      'en': 'Security', 'tw': 'Ahobammɔ', 'dg': 'Soŋsim', 'ee': 'Deɖeɖe', 'ha': 'Tsaro',
    },
    'biometric_login': {
      'en': 'Biometric Login', 'tw': 'Nsateaa wura mu', 'dg': 'Biometric kpe niŋ', 'ee': 'Biometric ge eme', 'ha': 'Biometric shiga',
    },
    'biometric_desc': {
      'en': 'Use fingerprint or face to login', 'tw': 'Fa nsateaa anaa anim wura mu', 'dg': 'Tum ni biometric kpe niŋ', 'ee': 'Zã biometric ge eme', 'ha': 'Yi amfani da biometric don shiga',
    },
    'about': {
      'en': 'About', 'tw': 'Ɛfa ho', 'dg': 'Din pam', 'ee': 'Tɔtrɔ', 'ha': 'Game da',
    },
    'logout': {
      'en': 'Logout', 'tw': 'Fi mu', 'dg': 'Yi niŋ', 'ee': 'Do go eme', 'ha': 'Fita',
    },
    'do_you_want_logout': {
      'en': 'Do you want to logout?', 'tw': 'Wopɛ sɛ wofi mu?', 'dg': 'A bɔri ka yi niŋ?', 'ee': 'Dè di be nado go eme?', 'ha': 'Kana so ka fita?',
    },
    'yes': {
      'en': 'Yes', 'tw': 'Aane', 'dg': 'Ayi', 'ee': 'Ɛ', 'ha': 'Eh',
    },
    'no': {
      'en': 'No', 'tw': 'Dabi', 'dg': 'Ayi', 'ee': 'Ao', 'ha': 'A\'a',
    },

    // Treatment
    'treatment': {
      'en': 'Treatment', 'tw': 'Ayaresa', 'dg': 'Tiba', 'ee': 'Atike', 'ha': 'Magani',
    },
    'treatment_guide': {
      'en': 'Treatment Guide', 'tw': 'Ayaresa nkyerɛwde', 'dg': 'Tiba zaŋli', 'ee': 'Atike alesi', 'ha': 'Jagoran magani',
    },
    'symptoms': {
      'en': 'Symptoms', 'tw': 'Nsɛnkyerɛnne', 'dg': 'Bɛhigu wuhigu', 'ee': 'Dzesi', 'ha': 'Alamomi',
    },
    'treatment_steps': {
      'en': 'Treatment Steps', 'tw': 'Ayaresa anammɔn', 'dg': 'Tiba tuma', 'ee': 'Atike afɔɖeɖewo', 'ha': 'Matakai magani',
    },
    'prevention': {
      'en': 'Prevention', 'tw': 'Ɛho banbɔ', 'dg': 'Kpahigu', 'ee': 'Kpekpe', 'ha': 'Rigakafi',
    },
    'recommended_products': {
      'en': 'Recommended Products', 'tw': 'Nneɛma a wɔkamfo', 'dg': 'Bindi shɛli', 'ee': 'Nuɖoɖowo', 'ha': 'Kayayyakin da ake ba da shawara',
    },
    'listen': {
      'en': 'Listen', 'tw': 'Tie', 'dg': 'Wumbu', 'ee': 'Se', 'ha': 'Saurara',
    },
    'translating': {
      'en': 'Translating...', 'tw': 'Ɛrekyerɛ ase...', 'dg': 'Zaŋli...', 'ee': 'Le ɖeɖem...', 'ha': 'Ana fassara...',
    },

    // Diagnosis
    'scan_failed': {
      'en': 'Scan Failed', 'tw': 'Nhwehwɛ no ansi yie', 'dg': 'Daliri ka ti', 'ee': 'Didi me dzo o', 'ha': 'Bincike bai yi',
    },
    'confidence': {
      'en': 'confidence', 'tw': 'gyidi', 'dg': 'tɛɣili', 'ee': 'ŋuɖoɖo', 'ha': 'tabbaci',
    },
    'view_treatment': {
      'en': 'View Treatment', 'tw': 'Hwɛ ayaresa', 'dg': 'Nyɛli tiba', 'ee': 'Kpɔ atike', 'ha': 'Duba magani',
    },
    'scan_history_empty': {
      'en': 'Scan history will appear here', 'tw': 'Nhwehwɛ abakɔsɛm bɛba ha', 'dg': 'Daliri tarihi ni ti kani', 'ee': 'Didi nutinya ava afisia', 'ha': 'Tarihin bincike zai bayyana anan',
    },

    // Common
    'ok': {
      'en': 'OK', 'tw': 'OK', 'dg': 'OK', 'ee': 'OK', 'ha': 'OK',
    },
    'cancel': {
      'en': 'Cancel', 'tw': 'Gyae', 'dg': 'Chɛ', 'ee': 'Dzudzɔ', 'ha': 'Soke',
    },
    'send': {
      'en': 'Send', 'tw': 'Mena', 'dg': 'Tum', 'ee': 'Ɖo', 'ha': 'Aika',
    },
    'change_password': {
      'en': 'Change Password', 'tw': 'Sesa nsɛmfua', 'dg': 'Labi password', 'ee': 'Trɔ ŋkugbalẽ', 'ha': 'Canja kalmar wucewa',
    },
    'old_password': {
      'en': 'Old Password', 'tw': 'Nsɛmfua tete', 'dg': 'Password kpahili', 'ee': 'Ŋkugbalẽ xoxo', 'ha': 'Tsohuwar kalmar wucewa',
    },
    'new_password': {
      'en': 'New Password', 'tw': 'Nsɛmfua foforɔ', 'dg': 'Password palli', 'ee': 'Ŋkugbalẽ yeye', 'ha': 'Sabuwar kalmar wucewa',
    },
    'save': {
      'en': 'Save', 'tw': 'Kora', 'dg': 'Daliri', 'ee': 'Dzra', 'ha': 'Ajiye',
    },
    'reset_password': {
      'en': 'Reset Password', 'tw': 'Sesa nsɛmfua', 'dg': 'Labi password', 'ee': 'Trɔ ŋkugbalẽ', 'ha': 'Sake kalmar wucewa',
    },
  };

  static const Map<String, String> languages = {
    'en': 'English',
    'tw': 'Twi',
    'dg': 'Dagbani',
    'ee': 'Ewe',
    'ha': 'Hausa',
  };
}
