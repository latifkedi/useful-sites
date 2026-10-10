# -*- coding: utf-8 -*-
"""The axes along which two records are compared.

A record may carry  "vs": [{"u": "<url of another record>", "a": "<axis>"}]  --
the entry it is most naturally weighed against, and the one thing on which the
two part ways. The axis is a closed list on purpose: a free-text reason would
be as unsearchable as the description it was copied from, and eight words are
enough to say what a reader is choosing between. key, Turkish label, English label.
"""

AXES = [
    ('lisans',     'Lisans',                 'Licence'),
    ('fiyat',      'Fiyat',                  'Price'),
    ('barindirma', 'Çalıştığı yer ve veri',  'Where it runs, where the data lives'),
    ('kapsam',     'Kapsam',                 'Scope'),
    ('yaklasim',   'Yaklaşım',               'Approach'),
    ('platform',   'Platform',               'Platform'),
    ('rehberlik',  'Rehberlik',              'Guidance'),
    ('olgunluk',   'Olgunluk',               'Maturity'),
]
AXIS_KEYS = [a[0] for a in AXES]
