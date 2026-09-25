# -*- coding: utf-8 -*-
"""The registry of curator notes.

Every record lives in data/notes/<category>.json -- one file per category, a
JSON array of objects. The file a record sits in *is* its category, so
moving an entry is moving an object from one file to another.

    {
      "url":  "https://example.com",       required, http(s)
      "name": "Example",                   required
      "tags": ["açık-kaynak", "python"],   required, canonical (see tags.py)
      "tr":   "Ne işe yarar, farkı ne.",    required
      "en":   "What it does, how it differs.", required
      "src":  "kedi",                       required, a key of sources.py
      "added": 1763065356,                  optional, unix time it arrived
      "review": "..."                       optional, a note that the entry
                                            still needs a human pass
    }

What the tr/en fields aim at: "what this is for" plus "where it parts ways
with its neighbours". Not a marketing line -- a line that helps you choose.

This replaced 44 part_*.py files and 14 bulk_notes*.json files that held the
same data in two shapes. The old loader had a failure mode worth naming: a
record added twice silently overwrote the first, and a broken part file
dropped every record below the error without raising. load_records() raises
instead -- a malformed file, an unknown field, a duplicate URL or a record in
an undeclared category stops the build with the file and position named.
"""
import io
import json
import os
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

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notes')

REQUIRED = ('url', 'name', 'tags', 'tr', 'en', 'src')
OPTIONAL = ('added', 'review')


class NoteError(ValueError):
    """A note file cannot be used as it stands. The message names where."""


def key(u):
    """The identity of a URL: no scheme, no leading www, no trailing slash."""
    u = re.sub(r'^https?://', '', u.strip().lower())
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


def _text(v):
    return isinstance(v, str) and v.strip() != ''


def validate(rec, sources):
    """Structural problems with one record, as a list of short messages.

    Only shape is checked here -- what makes the build impossible. Quality
    rules (a tag on every record, no pending review, a description long
    enough to help) live in test_build.py, so a submission can still be
    built and opened as a pull request before a person has passed over it.
    """
    if not isinstance(rec, dict):
        return ['not an object']
    out = ['missing "%s"' % f for f in REQUIRED if f not in rec]
    extra = sorted(set(rec) - set(REQUIRED) - set(OPTIONAL))
    if extra:
        out.append('unknown field(s): %s' % ', '.join(extra))
    url = rec.get('url')
    if 'url' in rec and not (isinstance(url, str)
                             and re.match(r'^https?://[^\s<>"]+$', url)):
        out.append('url must be http(s) with no spaces: %r' % (url,))
    for f in ('name', 'tr', 'en'):
        if f in rec and not _text(rec[f]):
            out.append('"%s" must be non-empty text' % f)
    if 'tags' in rec and not (isinstance(rec['tags'], list)
                              and all(isinstance(t, str) for t in rec['tags'])):
        out.append('"tags" must be a list of strings')
    if 'src' in rec and rec['src'] not in sources:
        out.append('unknown source %r (declare it in sources.py)' % (rec['src'],))
    if 'added' in rec and not (isinstance(rec['added'], int)
                               and not isinstance(rec['added'], bool)):
        out.append('"added" must be an integer unix time')
    if 'review' in rec and not _text(rec['review']):
        out.append('"review" must be non-empty text')
    return out


def load_records(notes_dir=NOTES_DIR, sources=None):
    """Every record, in category order then file order, each with its cat.

    Raises NoteError listing every problem found, not just the first -- one
    run should show everything that needs fixing.
    """
    if sources is None:
        from sources import SOURCES as sources
    cats = [c[0] for c in CATS]
    errors = []
    files = sorted(f for f in os.listdir(notes_dir) if f.endswith('.json'))
    for f in files:
        if f[:-5] not in cats:
            errors.append('%s: no such category in notes.CATS' % f)

    records, seen = [], {}
    for cat in cats:
        path = os.path.join(notes_dir, cat + '.json')
        if not os.path.exists(path):
            continue
        try:
            data = json.load(io.open(path, encoding='utf-8'))
        except ValueError as e:
            errors.append('%s.json: not valid JSON (%s)' % (cat, e))
            continue
        if not isinstance(data, list):
            errors.append('%s.json: top level must be a list' % cat)
            continue
        for i, rec in enumerate(data):
            where = '%s.json #%d' % (cat, i + 1)
            errors.extend('%s: %s' % (where, p) for p in validate(rec, sources))
            if not isinstance(rec, dict) or not isinstance(rec.get('url'), str):
                continue
            k = key(rec['url'])
            if k in seen:
                errors.append('%s: duplicate URL, already at %s' % (where, seen[k]))
                continue
            seen[k] = where
            r = dict(rec)
            r['cat'] = cat
            records.append(r)

    if errors:
        shown = errors[:40]
        more = len(errors) - len(shown)
        raise NoteError('\n'.join(shown) + ('\n... and %d more' % more if more else ''))
    return records
