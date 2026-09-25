# -*- coding: utf-8 -*-
"""Kanonik etiket sozlugu.

357 serbest etiket, ~59 kanonik etikete indirgeniyor. Amac filtre cubugunun
kullanilabilir kalmasi: tek kullanimlik etiket filtre degil gurultu.

CANON  : nihai sozluk, eksenlere gore gruplanmis
ALIAS  : ham etiket -> kanonik etiket
Haritada olmayan ham etiketler dusuruluyor.
"""

CANON = [
    # --- maliyet & lisans
    'ücretsiz', 'freemium', 'ücretli', 'açık-kaynak', 'açık-ağırlık',
    # --- content type
    'dokümantasyon', 'öğretici', 'video', 'kitap', 'kopya-kâğıdı',
    'awesome-liste', 'interaktif', 'müfredat', 'referans',
    # --- distribution & interface
    'self-hosted', 'cli', 'api', 'sdk', 'tarayıcı-içi', 'masaüstü', 'eklenti',
    # --- dil & platform
    'python', 'javascript', 'c-ailesi', 'rust', 'go', 'php', 'github', 'docker',
    # --- yapay zeka
    'llm', 'agent', 'rag', 'embedding', 'vektör-db', 'mcp',
    'guardrail', 'gözlemlenebilirlik', 'görsel-üretim', '3b', 'ses', 'otomasyon',
    # --- development areas
    'frontend', 'backend', 'veritabanı', 'devops', 'sistem-tasarımı',
    'algoritma', 'git', 'sunucu',
    # --- other areas
    'güvenlik', 'osint', 'gizlilik', 'ağ', 'donanım', 'gömülü', 'cad',
    'veri-bilimi', 'akademik', 'kuantum',
    # --- context
    'türkçe', 'mülakat', 'sertifika', 'arşivlenmiş',
]

ALIAS = {
    # maliyet & lisans
    'saas': 'ücretli', 'ticari': 'ücretli',
    'mit': 'açık-kaynak', 'apache-2': 'açık-kaynak', 'lisans': 'açık-kaynak',
    'model': 'açık-ağırlık', 'model-arşivi': 'açık-ağırlık',

    # content type
    'rehber': 'öğretici', 'ders-notu': 'öğretici', 'örnek': 'öğretici',
    'giriş': 'öğretici', 'kurulum': 'öğretici', 'vaka': 'öğretici',
    'makale': 'referans', 'bülten': 'referans', 'sözlük': 'referans',
    'standart': 'referans', 'arşiv': 'referans', 'dizin': 'referans',
    'katalog': 'referans', 'inceleme': 'referans', 'format': 'referans',
    'pdf': 'referans', 'not': 'referans', 'teknik': 'referans',
    'mimari': 'sistem-tasarımı', 'koleksiyon': 'awesome-liste',
    'yol-haritası': 'müfredat', 'kurs': 'müfredat', 'okul': 'müfredat',
    'üniversite': 'müfredat', 'öğrenme': 'müfredat', 'eğitim': 'müfredat',
    'proje': 'müfredat', 'alıştırma': 'interaktif', 'oyun': 'interaktif',
    'oyunlaştırılmış': 'interaktif', 'lab': 'interaktif', 'simülasyon': 'interaktif',
    'simülatör': 'interaktif', 'görselleştirme': 'interaktif',
    'not-defteri': 'interaktif', 'colab': 'interaktif', 'test': 'interaktif',
    'sınav': 'sertifika', 'öğrenci': 'sertifika', 'kariyer': 'mülakat',
    'başlangıç': 'öğretici', 'topluluk': 'awesome-liste', 'mentor': 'awesome-liste',
    'ödül-programı': 'güvenlik', 'yarışma': 'veri-bilimi', 'etkinlik': 'interaktif',

    # distribution & interface
    'kendi sunucunda': 'self-hosted', 'yerel': 'self-hosted',
    'yerel-model': 'self-hosted', 'çevrimdışı': 'self-hosted',
    'web-ui': 'tarayıcı-içi', 'web': 'tarayıcı-içi', 'proxy': 'api',
    'gateway': 'api', 'openapi': 'api', 'graphql': 'api', 'rest': 'api',
    'json-rpc': 'api', 'oauth': 'api', 'realtime': 'api', 'rss': 'api',
    'ide': 'masaüstü', 'editör': 'masaüstü', 'android': 'mobil',
    'ios': 'mobil', 'react-native': 'mobil', 'mobil': 'masaüstü',
    'araç': 'referans', 'araç-seti': 'referans', 'yardımcı': 'referans',

    # dil & platform
    'c': 'c-ailesi', 'c++': 'c-ailesi', 'dart': 'c-ailesi',
    'typescript': 'javascript', 'node': 'javascript', 'react': 'javascript',
    'java': 'c-ailesi', 'dotnet': 'c-ailesi', 'q#': 'kuantum', 'r': 'veri-bilimi',
    'fortran': 'c-ailesi', 'dil': 'referans', 'derleyici': 'c-ailesi',
    'assembly': 'c-ailesi', 'pytorch': 'python', 'async': 'python',
    'k8s': 'docker', 'ci': 'devops', 'edge': 'gömülü',

    # yapay zeka
    'asistan': 'llm', 'sohbet': 'llm', 'arama': 'rag', 'çatı': 'agent',
    'çoklu-agent': 'agent', 'durum-makinesi': 'agent', 'bellek': 'agent',
    'spec-driven': 'agent', 'metodoloji': 'agent', 'bağlam': 'agent',
    'yapılandırma': 'agent', 'prompt-injection': 'guardrail',
    'pii': 'gizlilik', 'tracing': 'gözlemlenebilirlik', 'eval': 'gözlemlenebilirlik',
    'değerlendirme': 'gözlemlenebilirlik', 'hata-izleme': 'gözlemlenebilirlik',
    'pano': 'gözlemlenebilirlik', 'maliyet': 'gözlemlenebilirlik',
    'difüzyon': 'görsel-üretim', 'görsel': 'görsel-üretim', 'vektör': 'görsel-üretim',
    'tasarım': 'görsel-üretim', 'ilham': 'görsel-üretim', 'şablon': 'görsel-üretim',
    'tipografi': 'görsel-üretim', 'doku': 'görsel-üretim', 'düzenleme': 'görsel-üretim',
    'tuval': 'görsel-üretim', 'text-to-3d': '3b', 'nerf': '3b', 'blender': '3b',
    'video': 'video', 'altyazı': 'video', 'tts': 'ses', 'stt': 'ses',
    'podcast': 'ses', 'ocr': 'referans', 'görü': 'llm', 'akıl-yürütme': 'llm',
    'rerank': 'embedding', 'bilgi-grafiği': 'rag', 'ayrıştırma': 'rag',
    'optimizasyon': 'llm', 'nicemleme': 'llm', 'sunum': 'llm',
    'llama.cpp': 'self-hosted', 'gguf': 'self-hosted', 'gpu': 'self-hosted',
    'oyun-alanı': 'interaktif', 'tespit': 'referans', 'alan-özel': 'embedding',
    'zapier': 'otomasyon', 'orkestrasyon': 'otomasyon', 'kuyruk': 'otomasyon',
    'olay-akışı': 'otomasyon', 'amqp': 'otomasyon', 'dijital-ikiz': 'gömülü',
    'entegrasyon': 'otomasyon', 'dünya-modeli': 'llm', 'araştırma': 'akademik',

    # development
    'css': 'frontend', 'ui': 'frontend', 'hypermedia': 'frontend',
    'bileşen': 'frontend', 'tel-kafes': 'frontend', 'seo': 'frontend',
    'e-ticaret': 'frontend', 'webcontainer': 'frontend', 'tam-yığın': 'frontend',
    'mikro-çatı': 'backend', 'orm': 'backend', 'batteries-included': 'backend',
    'ödeme': 'backend', 'sql': 'veritabanı', 'nosql': 'veritabanı',
    'postgres': 'veritabanı', 'mysql': 'veritabanı', 'graf-db': 'veritabanı',
    'cypher': 'veritabanı', 'önbellek': 'veritabanı', 'veri-yapısı': 'veritabanı',
    'modelleme': 'veritabanı', 'spark': 'veri-bilimi', 'etl': 'veri-bilimi',
    'automl': 'veri-bilimi', 'ml': 'veri-bilimi', 'düşük-kod': 'veri-bilimi',
    'veri': 'veri-bilimi', 'veri-kümesi': 'veri-bilimi', 'analiz': 'veri-bilimi',
    'zaman-serisi': 'veri-bilimi', 'finans': 'veri-bilimi', 'backtest': 'veri-bilimi',
    'veri-görselleştirme': 'veri-bilimi', 'istatistik': 'veri-bilimi',
    'barındırma': 'sunucu', 'vps': 'sunucu', 'bulut': 'sunucu', 'aws': 'sunucu',
    'azure': 'sunucu', 'gcp': 'sunucu', 'google': 'sunucu', 'microsoft': 'sunucu',
    'reverse-proxy': 'sunucu', 'edge-network': 'sunucu', 'ölçek': 'sistem-tasarımı',
    'performans': 'sistem-tasarımı', 'tasarım-deseni': 'sistem-tasarımı',
    'refactoring': 'sistem-tasarımı', 'teknik-borç': 'sistem-tasarımı',
    'analiz-aracı': 'sistem-tasarımı', 'kod': 'sistem-tasarımı',
    'hata-ayıklama': 'sistem-tasarımı', 'iç-mekanizma': 'sistem-tasarımı',
    'pipeline': 'devops', 'sysadmin': 'ağ', 'it-destek': 'ağ',
    'windows': 'ağ', 'linux': 'ağ', 'kurtarma': 'ağ', 'yedekleme': 'ağ',
    'wireshark': 'ağ', 'kablosuz': 'ağ', 'esim': 'gizlilik', 'sms': 'gizlilik',
    'pgp': 'gizlilik', 'alan-adı': 'gizlilik', 'yargı-bölgesi': 'gizlilik',
    'minimalizm': 'referans', 'webrtc': 'ağ', 'web-bluetooth': 'gömülü',
    'ble': 'gömülü', 'usb': 'gömülü', 'firmware': 'gömülü', 'iot': 'gömülü',
    'sbc': 'gömülü', 'risc-v': 'gömülü', 'soc': 'donanım', 'eda': 'cad',
    'kamera': 'gömülü', 'robotik': 'donanım', 'kontrol': 'donanım',
    'giyilebilir': 'donanım', 'ekran': 'donanım', 'ürün': 'donanım',
    'parça': 'cad', 'diy': 'donanım', 'işletim-sistemi': 'gömülü',
    'diyagram': 'görsel-üretim', 'metin': 'referans', 'markdown': 'referans',
    'dönüştürücü': 'referans', 'regex': 'referans', 'kazıma': 'referans',
    'erişilebilirlik': 'frontend', 'arşivleme': 'referans',

    # security
    'sızma-testi': 'güvenlik', 'ctf': 'güvenlik', 'kriptografi': 'güvenlik',
    'steganografi': 'güvenlik', 'keşif': 'osint', 'tersine-mühendislik': 'güvenlik',
    'tedarik-zinciri': 'güvenlik', 'kurumsal': 'güvenlik', 'netsec': 'ağ',
    'doğrulama': 'guardrail', 'tip-güvenli': 'python',

    # akademik & bilim
    'ön-baskı': 'akademik', 'dergi': 'akademik', 'akademik-arama': 'akademik',
    'tarama': 'akademik', 'özet': 'akademik', 'graf': 'akademik',
    'tıp': 'akademik', 'biyoloji': 'akademik', 'biyomedikal': 'akademik',
    'biyoinformatik': 'akademik', 'kemoinformatik': 'akademik', 'kimya': 'akademik',
    'sağlık': 'akademik', 'astronomi': 'akademik', 'bilim': 'akademik',
    'bilimsel': 'akademik', 'felsefe': 'akademik', 'dilbilim': 'akademik',
    'coğrafya': 'akademik', 'harita': 'akademik', 'tarih': 'akademik',
    'havacılık': 'akademik', 'vatandaş-bilimi': 'akademik', 'kurum': 'akademik',
    'resmî': 'akademik', 'hesaplama': 'akademik', 'matematik': 'akademik',
    'medya': 'referans', 'karakter': 'görsel-üretim', 'şema': 'sistem-tasarımı',
    'hukuk': 'referans', 'pazarlama': 'referans', 'sosyal-medya': 'referans',
    'iç-mekan': 'cad', 'blockchain': 'referans', 'deneysel': 'referans',
    'klavye': 'interaktif', 'animasyon': 'görsel-üretim', 'ekip': 'referans',
    'yaml': 'devops', 'rapor': 'referans', 'hibrit': 'kuantum',
    'araştırma-aracı': 'akademik', 'dayanıklı': 'otomasyon',
}


def normalise(tags):
    """Ham etiket listesini kanonik listeye cevirir (sirasi korunur, tekrarsiz)."""
    out = []
    for t in tags:
        c = ALIAS.get(t, t)
        if c in CANON and c not in out:
            out.append(c)
    return out


# ------------------------------------------------------------------ gorunen adlar
# Tags stay lowercase and hyphenated in the data, so they remain stable as
# URL and filter keys. What the interface shows comes from here. The labels
# are written by hand because Turkish capitalisation (i uppercases to a
# dotted I, not I) is not reliable in JS, and because abbreviations need
# their own casing: API, MCP, GitHub, PHP, DevOps.
LABELS = {
    'ücretsiz':            ('Ücretsiz', 'Free'),
    'freemium':            ('Freemium', 'Freemium'),
    'ücretli':             ('Ücretli', 'Paid'),
    'açık-kaynak':         ('Açık Kaynak', 'Open Source'),
    'açık-ağırlık':        ('Açık Ağırlık', 'Open Weights'),
    'dokümantasyon':       ('Dokümantasyon', 'Docs'),
    'öğretici':            ('Öğretici', 'Tutorial'),
    'video':               ('Video', 'Video'),
    'kitap':               ('Kitap', 'Book'),
    'kopya-kâğıdı':        ('Kopya Kâğıdı', 'Cheat Sheet'),
    'awesome-liste':       ('Awesome Liste', 'Awesome List'),
    'interaktif':          ('İnteraktif', 'Interactive'),
    'müfredat':            ('Müfredat', 'Curriculum'),
    'referans':            ('Referans', 'Reference'),
    'self-hosted':         ('Kendi Sunucunda', 'Self-Hosted'),
    'cli':                 ('CLI', 'CLI'),
    'api':                 ('API', 'API'),
    'sdk':                 ('SDK', 'SDK'),
    'tarayıcı-içi':        ('Tarayıcıda', 'In Browser'),
    'masaüstü':            ('Masaüstü', 'Desktop'),
    'eklenti':             ('Eklenti', 'Plugin'),
    'python':              ('Python', 'Python'),
    'javascript':          ('JavaScript', 'JavaScript'),
    'c-ailesi':            ('C Ailesi', 'C Family'),
    'rust':                ('Rust', 'Rust'),
    'go':                  ('Go', 'Go'),
    'php':                 ('PHP', 'PHP'),
    'github':              ('GitHub', 'GitHub'),
    'docker':              ('Docker', 'Docker'),
    'llm':                 ('LLM', 'LLM'),
    'agent':               ('Agent', 'Agent'),
    'rag':                 ('RAG', 'RAG'),
    'embedding':           ('Embedding', 'Embedding'),
    'vektör-db':           ('Vektör VT', 'Vector DB'),
    'mcp':                 ('MCP', 'MCP'),
    'guardrail':           ('Guardrail', 'Guardrail'),
    'gözlemlenebilirlik':  ('Gözlemlenebilirlik', 'Observability'),
    'görsel-üretim':       ('Görsel Üretim', 'Image Gen'),
    '3b':                  ('3B', '3D'),
    'ses':                 ('Ses', 'Audio'),
    'otomasyon':           ('Otomasyon', 'Automation'),
    'frontend':            ('Frontend', 'Frontend'),
    'backend':             ('Backend', 'Backend'),
    'veritabanı':          ('Veritabanı', 'Database'),
    'devops':              ('DevOps', 'DevOps'),
    'sistem-tasarımı':     ('Sistem Tasarımı', 'System Design'),
    'algoritma':           ('Algoritma', 'Algorithms'),
    'git':                 ('Git', 'Git'),
    'sunucu':              ('Sunucu', 'Server'),
    'güvenlik':            ('Güvenlik', 'Security'),
    'osint':               ('OSINT', 'OSINT'),
    'gizlilik':            ('Gizlilik', 'Privacy'),
    'ağ':                  ('Ağ', 'Networking'),
    'donanım':             ('Donanım', 'Hardware'),
    'gömülü':              ('Gömülü', 'Embedded'),
    'cad':                 ('CAD', 'CAD'),
    'veri-bilimi':         ('Veri Bilimi', 'Data Science'),
    'akademik':            ('Akademik', 'Academic'),
    'kuantum':             ('Kuantum', 'Quantum'),
    'türkçe':              ('Türkçe', 'Turkish'),
    'mülakat':             ('Mülakat', 'Interview'),
    'sertifika':           ('Sertifika', 'Certification'),
    'arşivlenmiş':         ('Arşivlenmiş', 'Archived'),
}

_eksik = [t for t in CANON if t not in LABELS]
assert not _eksik, 'gorunen adi olmayan etiket: %s' % _eksik

# ------------------------------------------------------------- Ingilizce girisler
# The submission form is in English now, so people write "open-source" or
# "database". Neither was in ALIAS and both were silently dropped. Each
# canonical tag's English display label is bound to its own key -- derived
# from LABELS rather than typed out, so the two cannot drift apart.
for _k, _v in LABELS.items():
    _en = _v[1].lower().replace(' ', '-')
    if _en not in ALIAS and _en not in CANON:
        ALIAS[_en] = _k

# Other common ways of saying the same thing. setdefault, so this table
# never overwrites an existing mapping -- the first attempt used update()
# and clobbered the existing 'k8s' -> 'docker' entry, which quietly changed
# the tags on two records.
for _en, _tr in {
    'oss': 'açık-kaynak', 'opensource': 'açık-kaynak', 'foss': 'açık-kaynak',
    'db': 'veritabanı', 'databases': 'veritabanı',
    'documentation': 'dokümantasyon', 'guide': 'öğretici', 'course': 'müfredat',
    'learning': 'müfredat', 'roadmap': 'müfredat', 'infosec': 'güvenlik',
    'appsec': 'güvenlik', 'ml': 'veri-bilimi', 'machine-learning': 'veri-bilimi',
    'ai': 'llm', 'networking': 'ağ', 'sysadmin': 'ağ', 'js': 'javascript',
    'py': 'python', 'golang': 'go', 'k8s': 'devops', 'kubernetes': 'devops',
    'ci': 'devops', 'observability': 'gözlemlenebilirlik', 'no-cost': 'ücretsiz',
    'free-tier': 'freemium', 'paid': 'ücretli', 'book': 'kitap',
    'cheatsheet': 'kopya-kâğıdı', 'cheat-sheet': 'kopya-kâğıdı',
}.items():
    ALIAS.setdefault(_en, _tr)


# Filter facets. The tag bar was one flat row of 63 chips mixing price,
# content type, platform and topic, so "ücretsiz" (on 45% of records) sat next
# to "kuantum" as if they answered the same question. Each canonical tag lives
# in exactly one facet; whatever the first three do not claim is a topic.
# key, Turkish label, English label, tags.
_FACET_HEADS = [
    ('fiyat', 'Fiyat & Lisans', 'Price & Licence',
     ['ücretsiz', 'freemium', 'ücretli', 'açık-kaynak', 'açık-ağırlık', 'self-hosted']),
    ('tur', 'Tür', 'Type',
     ['referans', 'öğretici', 'müfredat', 'kitap', 'video', 'kopya-kâğıdı', 'dokümantasyon',
      'awesome-liste', 'interaktif', 'akademik', 'sertifika', 'mülakat', 'türkçe', 'arşivlenmiş']),
    ('arayuz', 'Arayüz & Dil', 'Interface & Language',
     ['tarayıcı-içi', 'masaüstü', 'cli', 'api', 'sdk', 'eklenti', 'github', 'docker',
      'python', 'javascript', 'c-ailesi', 'rust', 'go', 'php']),
]
_claimed = {t for _, _, _, ts in _FACET_HEADS for t in ts}
FACETS = _FACET_HEADS + [
    ('konu', 'Konu', 'Topic', [t for t in CANON if t not in _claimed]),
]
