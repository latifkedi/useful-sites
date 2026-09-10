# -*- coding: utf-8 -*-
"""The registry of curator notes.

The notes themselves live in the part_*.py files; each exposes load(add).
The key is a normalised URL (scheme, www and trailing slash removed).

What the tr/en fields aim at: "what this is for" plus "where it parts ways
with its neighbours". Not a marketing line -- a line that helps you choose.
"""
import re

# key, Turkish label, English label
CATS = [
    ('ogrenme',    'Öğrenme & Yol Haritaları',      'Learning & Roadmaps'),
    ('pratik',     'Pratik & Alıştırma',            'Practice & Challenges'),
    ('diller',     'Programlama Dilleri',           'Programming Languages'),
    ('web',        'Web & Frontend',                'Web & Frontend'),
    ('backend',    'Backend, API & Sistem Tasarımı', 'Backend, API & System Design'),
    ('mobil',      'Mobil & Masaüstü',              'Mobile & Desktop'),
    ('veritabani', 'Veritabanı',                    'Databases'),
    ('devops',     'DevOps & Altyapı',              'DevOps & Infrastructure'),
    ('ag',         'Ağ & Sistem Yönetimi',          'Networking & Sysadmin'),
    ('barindirma', 'Öz-Barındırma & Kişisel Bulut', 'Self-Hosting & Personal Cloud'),
    ('guvenlik',   'Güvenlik & Gizlilik',           'Security & Privacy'),
    ('veri',       'Veri Bilimi & Makine Öğrenmesi', 'Data Science & ML'),
    ('yz_model',   'YZ · Modeller & Asistanlar',    'AI · Models & Assistants'),
    ('yz_altyapi', 'YZ · Agent & Altyapı',          'AI · Agents & Infrastructure'),
    ('yz_rag',     'YZ · RAG, Gömme & Vektör',      'AI · RAG, Embeddings & Vectors'),
    ('yz_arac',    'YZ · Uygulama Araçları',        'AI · Applied Tools'),
    ('yz_uretim',  'YZ · Üretken Medya',            'AI · Generative Media'),
    ('donanim',    'Donanım, CAD & Gömülü',         'Hardware, CAD & Embedded'),
    ('gozluk',     'Akıllı Gözlük & Giyilebilir',   'Smart Glasses & Wearables'),
    ('kuantum',    'Kuantum Bilişim',               'Quantum Computing'),
    ('araclar',    'Araçlar & Yardımcılar',         'Tools & Utilities'),
    ('medya',      'Medya, Tasarım & Dosya',        'Media, Design & Files'),
    ('referans',   'Referans & Koleksiyonlar',      'Reference & Collections'),
    ('bilim',      'Bilim & Akademik',              'Science & Academia'),
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
]

import importlib  # noqa: E402

for _name in PARTS:
    importlib.import_module(_name).load(add)
