# -*- coding: utf-8 -*-
"""The registry of curator notes.

The notes themselves live in the part_*.py files; each exposes load(add).
The key is a normalised URL (scheme, www and trailing slash removed).

What the tr/en fields aim at: "what this is for" plus "where it parts ways
with its neighbours". Not a marketing line -- a line that helps you choose.
"""
import re

# key, Turkish label, English label.
# Ordered to follow GROUPS below: records sort field by field, and the app
# derives its category order from this sequence.
CATS = [
    # -- Yazılım
    ('diller',     'Programlama Dilleri',           'Programming Languages'),
    ('web',        'Web & Frontend',                'Web & Frontend'),
    ('backend',    'Backend, API & Sistem Tasarımı', 'Backend, API & System Design'),
    ('mobil',      'Mobil & Masaüstü',              'Mobile & Desktop'),
    ('veritabani', 'Veritabanı',                    'Databases'),
    ('pratik',     'Pratik & Alıştırma',            'Practice & Challenges'),
    ('test',       'Test & Kalite',                 'Testing & QA'),
    ('oyun',       'Oyun Geliştirme',               'Game Development'),
    # -- Yapay Zeka
    ('yz_model',   'YZ · Modeller & Asistanlar',    'AI · Models & Assistants'),
    ('yz_altyapi', 'YZ · Agent & Altyapı',          'AI · Agents & Infrastructure'),
    ('yz_rag',     'YZ · RAG, Gömme & Vektör',      'AI · RAG, Embeddings & Vectors'),
    ('yz_arac',    'YZ · Uygulama Araçları',        'AI · Applied Tools'),
    ('yz_uretim',  'YZ · Üretken Medya',            'AI · Generative Media'),
    # -- Altyapı & Sistem
    ('devops',     'DevOps & Altyapı',              'DevOps & Infrastructure'),
    ('ag',         'Ağ & Sistem Yönetimi',          'Networking & Sysadmin'),
    ('barindirma', 'Öz-Barındırma & Kişisel Bulut', 'Self-Hosting & Personal Cloud'),
    ('donanim',    'Donanım, CAD & Gömülü',         'Hardware, CAD & Embedded'),
    ('elektronik', 'Elektrik & Elektronik',         'Electrical & Electronics'),
    ('gozluk',     'Akıllı Gözlük & Giyilebilir',   'Smart Glasses & Wearables'),
    # -- Güvenlik
    ('guvenlik',   'Güvenlik & Gizlilik',           'Security & Privacy'),
    # -- Veri
    ('veri',       'Veri Bilimi & Makine Öğrenmesi', 'Data Science & ML'),
    ('veri_muh',   'Veri Mühendisliği',             'Data Engineering'),
    # -- Bilim & Matematik
    ('bilim',      'Bilim & Akademik',              'Science & Academia'),
    ('matematik',  'Matematik',                     'Mathematics'),
    ('kuantum',    'Kuantum Bilişim',               'Quantum Computing'),
    # -- Ekonomi & Finans
    ('ekonomi',    'Ekonomi & Finans',              'Economics & Finance'),
    # -- Tasarım & Medya
    ('medya',      'Medya, Tasarım & Dosya',        'Media, Design & Files'),
    ('mimari',     'Mimari & Yapı',                 'Architecture & Building'),
    # -- Öğrenme & Referans
    ('ogrenme',    'Öğrenme & Yol Haritaları',      'Learning & Roadmaps'),
    ('referans',   'Referans & Koleksiyonlar',      'Reference & Collections'),
    ('araclar',    'Araçlar & Yardımcılar',         'Tools & Utilities'),
    # -- Korsan & Arşiv
    ('korsan',     'Korsan & FMHY',                 'Piracy & FMHY'),
]

# Top-level fields (üst-alan): each groups a run of categories. The homepage
# and the text hub render category cards under these headings; feeds and
# per-category pages are unchanged. key, Turkish label, English label, cats.
GROUPS = [
    ('yazilim',     'Yazılım',            'Software',
     ['diller', 'web', 'backend', 'mobil', 'veritabani', 'pratik', 'test', 'oyun']),
    ('yapayzeka',   'Yapay Zeka',         'Artificial Intelligence',
     ['yz_model', 'yz_altyapi', 'yz_rag', 'yz_arac', 'yz_uretim']),
    ('sistem',      'Altyapı & Sistem',   'Infrastructure & Systems',
     ['devops', 'ag', 'barindirma', 'donanim', 'elektronik', 'gozluk']),
    ('guvenlikalan', 'Güvenlik',          'Security',
     ['guvenlik']),
    ('verialan',    'Veri',               'Data',
     ['veri', 'veri_muh']),
    ('bilimmat',    'Bilim & Matematik',  'Science & Mathematics',
     ['bilim', 'matematik', 'kuantum']),
    ('ekonomialan', 'Ekonomi & Finans',   'Economics & Finance',
     ['ekonomi']),
    ('tasarim',     'Tasarım & Medya',    'Design & Media',
     ['medya', 'mimari']),
    ('ogrenmealan', 'Öğrenme & Referans', 'Learning & Reference',
     ['ogrenme', 'referans', 'araclar']),
    ('korsanalan',  'Korsan & Arşiv',     'Piracy & Archive',
     ['korsan']),
]

NOTES = {}


def add(url, name, tags, tr, en, cat=None, src='kedi'):
    k = re.sub(r'^https?://', '', url.strip().lower())
    k = re.sub(r'^www\.', '', k).rstrip('/')
    NOTES[k] = {'name': name, 'tags': tags, 'tr': tr, 'en': en,
                'cat': cat, 'src': src, 'url': url}


PARTS = [
    'part_ai_model', 'part_ai_infra', 'part_ai_tools',
    'part_dev', 'part_ops', 'part_infra', 'part_sec',
    'part_hw', 'part_misc', 'part_extra',
    'part_new', 'part_ext1', 'part_ext2',
    'part_cdcruz', 'part_awesome', 'part_invesp', 'part_ext3',
    'part_seccert', 'part_lowkwiki',
    'part_econ', 'part_math',
]

import importlib  # noqa: E402

for _name in PARTS:
    importlib.import_module(_name).load(add)
