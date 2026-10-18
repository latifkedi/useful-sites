# -*- coding: utf-8 -*-
"""Kanonik etiket sozlugu.

357 serbest etiket, ~59 kanonik etikete indirgeniyor. Amac filtre cubugunun
kullanilabilir kalmasi: tek kullanimlik etiket filtre degil gurultu.

CANON  : nihai sozluk, eksenlere gore gruplanmis
ALIAS  : ham etiket -> kanonik etiket
Haritada olmayan ham etiketler dusuruluyor. An alias mapped to None is dropped on
purpose: it used to land on a wrong tag ('tip-güvenli' on python, 'hukuk' on
referans) and no canonical tag says the same thing. Old keys stay in the table,
repointed rather than deleted, so a submission or link that uses one still resolves.
"""

CANON = [
    # --- maliyet & lisans
    'ücretsiz', 'freemium', 'ücretli', 'açık-kaynak', 'açık-ağırlık',
    # --- content type
    'dokümantasyon', 'öğretici', 'video', 'kitap', 'kopya-kâğıdı',
    'awesome-liste', 'interaktif', 'müfredat', 'referans', 'araç',
    # --- level (learning records only; rubric in CONTRIBUTING.md)
    'başlangıç', 'orta', 'ileri',
    # --- platform & access
    'tarayıcı-içi', 'masaüstü', 'mobil', 'cli', 'eklenti', 'çevrimdışı', 'self-hosted',
    'hesap-gerekmez',
    # --- integration
    'api', 'sdk',
    # --- dil & platform
    'python', 'javascript', 'c-ailesi', 'rust', 'go', 'php', 'jvm', 'docker',
    # --- yapay zeka
    'llm', 'agent', 'rag', 'embedding', 'vektör-db', 'mcp',
    'guardrail', 'gözlemlenebilirlik', 'görsel-üretim', '3b', 'ses', 'otomasyon',
    'tasarım',
    # --- development areas
    'frontend', 'backend', 'veritabanı', 'devops', 'sistem-tasarımı',
    'algoritma', 'git', 'sunucu',
    # --- other areas
    'güvenlik', 'osint', 'gizlilik', 'ağ', 'donanım', 'gömülü', 'cad',
    'veri-bilimi', 'veri-seti', 'akademik', 'kuantum', 'kripto',
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
    'topluluk': 'awesome-liste', 'mentor': 'awesome-liste',
    'ödül-programı': 'güvenlik', 'yarışma': 'interaktif', 'etkinlik': 'interaktif',
    'yeni-başlayan': 'başlangıç', 'ara-seviye': 'orta', 'ileri-seviye': 'ileri',

    # distribution & interface
    'kendi sunucunda': 'self-hosted', 'yerel': 'self-hosted',
    'yerel-model': 'self-hosted', 'hesapsız': 'hesap-gerekmez', 'kayıtsız': 'hesap-gerekmez',
    'web-ui': 'tarayıcı-içi', 'web': 'tarayıcı-içi', 'proxy': 'api',
    'gateway': 'api', 'openapi': 'api', 'graphql': 'api', 'rest': 'api',
    'json-rpc': 'api', 'oauth': 'api', 'realtime': 'api', 'rss': 'api',
    'ide': 'masaüstü', 'editör': 'masaüstü', 'android': 'mobil',
    'ios': 'mobil', 'react-native': 'mobil', 'flutter': 'mobil',
    'araç-seti': 'araç', 'yardımcı': 'araç',

    # dil & platform
    'c': 'c-ailesi', 'c++': 'c-ailesi', 'dart': 'mobil',
    'typescript': 'javascript', 'node': 'javascript', 'react': 'javascript',
    'java': 'jvm', 'kotlin': 'jvm', 'scala': 'jvm', 'dotnet': 'c-ailesi', 'q#': 'kuantum', 'r': 'veri-bilimi',
    'fortran': 'c-ailesi', 'dil': 'referans', 'derleyici': 'c-ailesi',
    'assembly': 'c-ailesi', 'pytorch': 'python', 'async': 'python',
    'k8s': 'devops', 'kubernetes': 'devops', 'ci': 'devops', 'edge': 'gömülü',

    # yapay zeka
    'asistan': 'llm', 'sohbet': 'llm', 'arama': 'rag', 'çatı': 'agent',
    'çoklu-agent': 'agent', 'durum-makinesi': 'agent', 'bellek': 'agent',
    'spec-driven': 'agent', 'metodoloji': 'agent', 'bağlam': 'agent',
    'yapılandırma': 'agent', 'prompt-injection': 'guardrail',
    'pii': 'gizlilik', 'tracing': 'gözlemlenebilirlik', 'eval': 'gözlemlenebilirlik',
    'değerlendirme': 'gözlemlenebilirlik', 'hata-izleme': 'gözlemlenebilirlik',
    'pano': 'gözlemlenebilirlik', 'maliyet': 'gözlemlenebilirlik',
    'difüzyon': 'görsel-üretim', 'görsel': 'görsel-üretim', 'vektör': 'tasarım',
    'ilham': 'tasarım', 'şablon': 'tasarım', 'ikon': 'tasarım',
    'tipografi': 'tasarım', 'doku': 'tasarım', 'düzenleme': 'görsel-üretim',
    'tuval': 'tasarım', 'text-to-3d': '3b', 'nerf': '3b', 'blender': '3b',
    'video': 'video', 'altyazı': 'video', 'tts': 'ses', 'stt': 'ses',
    'podcast': 'ses', 'ocr': 'araç', 'görü': 'llm', 'akıl-yürütme': 'llm',
    'rerank': 'embedding', 'bilgi-grafiği': 'rag', 'ayrıştırma': 'rag',
    'optimizasyon': 'llm', 'nicemleme': 'llm', 'sunum': 'llm',
    'llama.cpp': 'self-hosted', 'gguf': 'self-hosted', 'gpu': 'self-hosted',
    'oyun-alanı': 'interaktif', 'tespit': 'araç', 'alan-özel': 'embedding',
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
    'veri': 'veri-bilimi', 'veri-kümesi': 'veri-seti', 'analiz': 'veri-bilimi',
    'dataset': 'veri-seti', 'datasets': 'veri-seti', 'açık-veri': 'veri-seti',
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
    'diyagram': 'tasarım', 'metin': 'referans', 'markdown': 'referans',
    'dönüştürücü': 'araç', 'regex': 'araç', 'kazıma': 'otomasyon',
    'erişilebilirlik': 'frontend', 'arşivleme': 'referans',

    # security
    'sızma-testi': 'güvenlik', 'ctf': 'güvenlik', 'kriptografi': 'güvenlik',
    'steganografi': 'güvenlik', 'keşif': 'osint', 'tersine-mühendislik': 'güvenlik',
    'tedarik-zinciri': 'güvenlik', 'kurumsal': 'güvenlik', 'netsec': 'ağ',
    'doğrulama': 'guardrail', 'tip-güvenli': None,

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
    'medya': 'video', 'karakter': 'tasarım', 'şema': 'sistem-tasarımı',
    'hukuk': None, 'pazarlama': 'referans', 'sosyal-medya': 'referans',
    'iç-mekan': 'cad', 'blockchain': 'kripto', 'bitcoin': 'kripto', 'ethereum': 'kripto',
    'defi': 'kripto', 'deneysel': 'referans',
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
    'araç':                ('Araç', 'Tool'),
    'başlangıç':           ('Başlangıç', 'Beginner'),
    'orta':                ('Orta Seviye', 'Intermediate'),
    'ileri':               ('İleri Seviye', 'Advanced'),
    'self-hosted':         ('Kendi Sunucunda', 'Self-Hosted'),
    'cli':                 ('CLI', 'CLI'),
    'api':                 ('API', 'API'),
    'sdk':                 ('SDK', 'SDK'),
    'tarayıcı-içi':        ('Tarayıcıda', 'In Browser'),
    'masaüstü':            ('Masaüstü', 'Desktop'),
    'mobil':               ('Mobil', 'Mobile'),
    'çevrimdışı':          ('Çevrimdışı', 'Offline'),
    'hesap-gerekmez':      ('Hesap Gerekmez', 'No Account Needed'),
    'eklenti':             ('Eklenti', 'Plugin'),
    'python':              ('Python', 'Python'),
    'javascript':          ('JavaScript', 'JavaScript'),
    'c-ailesi':            ('C Ailesi', 'C Family'),
    'rust':                ('Rust', 'Rust'),
    'go':                  ('Go', 'Go'),
    'php':                 ('PHP', 'PHP'),
    'jvm':                 ('JVM (Java, Kotlin, Scala)', 'JVM (Java, Kotlin, Scala)'),
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
    'tasarım':             ('Tasarım', 'Design'),
    'frontend':           ('Frontend', 'Frontend'),
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
    'veri-seti':           ('Veri Seti', 'Dataset'),
    'akademik':            ('Akademik', 'Academic'),
    'kuantum':             ('Kuantum', 'Quantum'),
    'kripto':              ('Kripto', 'Crypto'),
    'türkçe':             ('Türkçe', 'Turkish'),
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
# and clobbered the then 'k8s' -> 'docker' entry, which quietly changed the
# tags on two records. Both spellings of Kubernetes now go to devops in ALIAS
# itself, so the two tables agree.
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
    'no-account': 'hesap-gerekmez', 'no-signup': 'hesap-gerekmez', 'android': 'mobil',
    'ios': 'mobil', 'web': 'tarayıcı-içi', 'browser': 'tarayıcı-içi', 'desktop-app': 'masaüstü',
    'intro': 'başlangıç', 'introductory': 'başlangıç', 'blockchain': 'kripto',
    'cryptocurrency': 'kripto', 'tools': 'araç', 'utility': 'araç', 'ui-design': 'tasarım',
}.items():
    ALIAS.setdefault(_en, _tr)


# Filter facets. The tag bar was one flat row of 63 chips mixing price,
# content type, platform and topic, so "ücretsiz" sat next to "kuantum" as if
# they answered the same question. Each canonical tag lives in exactly one facet;
# whatever the heads do not claim is a topic. The three cost tags are one
# question with one answer per record (test_build enforces it): "ücretsiz" is on
# four records in five now that it is set wherever nothing is sold, which is why
# the cards do not repeat it -- the filter keeps it.
# key, Turkish label, English label, tags.
#
# 'Interface & Language' used to hold where a thing runs (browser, desktop, CLI)
# next to what it is written in and how you call it (Python, API, SDK). Those
# are two questions. Platform & Access now answers "where do I use it, and do I
# need an account"; Language & Integration answers "which stack, and is there an
# API/SDK to build on". self-hosted moved out of Price & Licence into Platform:
# it says where the thing runs, not what it costs.
_FACET_HEADS = [
    ('fiyat', 'Fiyat & Lisans', 'Price & Licence',
     ['ücretsiz', 'freemium', 'ücretli', 'açık-kaynak', 'açık-ağırlık']),
    ('tur', 'Tür', 'Type',
     ['referans', 'araç', 'öğretici', 'müfredat', 'kitap', 'video', 'kopya-kâğıdı', 'dokümantasyon',
      'awesome-liste', 'interaktif', 'akademik', 'sertifika', 'mülakat', 'arşivlenmiş']),
    # Set only on learning records (the learning, practice, books, languages and
    # security lab/career categories); the rubric is in CONTRIBUTING.md.
    ('seviye', 'Seviye', 'Level', ['başlangıç', 'orta', 'ileri']),
    # The language the resource itself is written in -- its own question, not a
    # kind of content. 'türkçe' sat in Type beside 'video' and 'kitap'.
    ('dil', 'İçerik Dili', 'Content Language', ['türkçe']),
    ('platform', 'Platform & Erişim', 'Platform & Access',
     ['tarayıcı-içi', 'masaüstü', 'mobil', 'cli', 'eklenti', 'çevrimdışı', 'self-hosted',
      'hesap-gerekmez']),
    ('teknoloji', 'Dil & Entegrasyon', 'Language & Integration',
     ['python', 'javascript', 'c-ailesi', 'rust', 'go', 'php', 'jvm', 'docker', 'api', 'sdk']),
]
_claimed = {t for _, _, _, ts in _FACET_HEADS for t in ts}

# Tag density. Price & licence answer one question every record answers, so they
# do not count; everything else does. Fewer than two leaves a record findable by
# one chip at most; more than four turns the card's tag row back into noise.
# test_build.py enforces both (the floor as a ratchet, see THIN_MAX there).
UNCOUNTED = ('ücretsiz', 'freemium', 'ücretli', 'açık-kaynak', 'açık-ağırlık')
MIN_TAGS, MAX_TAGS = 2, 4
LEVELS = ('başlangıç', 'orta', 'ileri')
# Only these categories carry a level: elsewhere "beginner" would be a guess.
LEVEL_CATS = ('ogrenme', 'pratik', 'kitaplik', 'diller', 'guv_lab', 'guv_kariyer')
FACETS = _FACET_HEADS + [
    ('konu', 'Konu', 'Topic', [t for t in CANON if t not in _claimed]),
]
