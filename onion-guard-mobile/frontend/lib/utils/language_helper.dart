class LanguageHelper {
  static const Map<String, String> languages = {
    'en': 'English',
    'tw': 'Twi',
    'dg': 'Dagbani',
    'ee': 'Ewe',
    'ha': 'Hausa',
  };

  static const Map<String, Map<String, String>> translations = {
    'app_title': {
      'en': 'OnionGuard',
      'tw': 'OnionGuard',
      'dg': 'OnionGuard',
      'ee': 'OnionGuard',
      'ha': 'OnionGuard',
    },
    'scan_disease': {
      'en': 'Scan Disease',
      'tw': 'Hwehwɛ Nyarewa',
      'dg': 'Daliri Bɛhigu',
      'ee': 'Dɔlele Didi',
      'ha': 'Bincika Cuta',
    },
    'healthy': {
      'en': 'Healthy',
      'tw': 'Apɔmuden',
      'dg': 'Alaafee',
      'ee': 'Lãme nyui',
      'ha': 'Lafiya',
    },
    'treatment': {
      'en': 'Treatment',
      'tw': 'Ayaresa',
      'dg': 'Tiba',
      'ee': 'Atike',
      'ha': 'Magani',
    },
    'history': {
      'en': 'History',
      'tw': 'Abakɔsɛm',
      'dg': 'Tarihi',
      'ee': 'Nutinya',
      'ha': 'Tarihi',
    },
    'settings': {
      'en': 'Settings',
      'tw': 'Nhyehyɛe',
      'dg': 'Zaŋli',
      'ee': 'Ɖoɖo',
      'ha': 'Saiti',
    },
    'welcome': {
      'en': 'Welcome',
      'tw': 'Akwaaba',
      'dg': 'Anlaibiisim',
      'ee': 'Woezon',
      'ha': 'Sannu',
    },
    'login': {
      'en': 'Login',
      'tw': 'Wura mu',
      'dg': 'Kpe niŋ',
      'ee': 'Ge eme',
      'ha': 'Shiga',
    },
    'register': {
      'en': 'Register',
      'tw': 'Kyerɛw din',
      'dg': 'Sabi din',
      'ee': 'Ŋlɔ ŋkɔ',
      'ha': 'Yi rajista',
    },
    'listen': {
      'en': 'Listen',
      'tw': 'Tie',
      'dg': 'Wumbu',
      'ee': 'Se',
      'ha': 'Saurara',
    },
  };

  static String translate(String key, String langCode) {
    return translations[key]?[langCode] ?? translations[key]?['en'] ?? key;
  }
}
