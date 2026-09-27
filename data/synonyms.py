# -*- coding: utf-8 -*-
"""Search synonyms: groups of terms that mean the same thing.

build.py writes these into links.js as window.SYNONYMS and search.js reads
them. A query that names any member of a group also finds records that use
another member: "password manager" finds the entries described as "parola
yöneticisi", and "k8s" finds Kubernetes. Members match only at a word start,
so "book" does not pull in "facebook".

Keep each group to real equivalents. A loose group widens every query that
touches it. test_search.js checks three things: no term sits in two groups,
every group has at least two members, and every group has a member that
finds a record on its own.
"""

GROUPS = [
    # AI and data
    ['yapay zeka', 'yz', 'ai', 'artificial intelligence'],
    ['makine öğrenmesi', 'makine öğrenimi', 'machine learning', 'ml'],
    ['derin öğrenme', 'deep learning'],
    ['büyük dil modeli', 'dil modeli', 'llm', 'large language model'],
    ['doğal dil işleme', 'natural language processing', 'nlp'],
    ['veri seti', 'veri kümesi', 'dataset'],
    ['veritabanı', 'database', 'db'],
    ['istatistik', 'statistics'],
    ['ekonomik veri', 'ekonomi verisi', 'economic data'],
    # languages and tools
    ['js', 'javascript'],
    ['ts', 'typescript'],
    ['py', 'python'],
    ['golang', 'go'],
    ['regex', 'regexp', 'düzenli ifade', 'regular expression'],
    ['k8s', 'kubernetes'],
    ['konteyner', 'container'],
    ['sanal makine', 'virtual machine', 'vm'],
    ['terminal', 'komut satırı', 'command line', 'cli'],
    ['sunucu', 'server'],
    ['barındırma', 'hosting'],
    ['alan adı', 'domain'],
    ['bulut', 'cloud'],
    ['ağ', 'network', 'networking'],
    ['tarayıcı', 'browser'],
    ['eklenti', 'extension', 'plugin', 'addon'],
    ['arama motoru', 'search engine'],
    ['açık kaynak', 'open source', 'oss'],
    ['kütüphane', 'library'],
    ['yedekleme', 'backup'],
    # security and privacy
    ['şifre yöneticisi', 'parola yöneticisi', 'password manager'],
    ['güvenlik', 'security'],
    ['gizlilik', 'privacy'],
    # design and media
    ['renk paleti', 'color palette', 'colour palette'],
    ['yazı tipi', 'font', 'typeface'],
    ['ikon', 'icon', 'simge'],
    ['diyagram', 'diagram'],
    ['fotoğraf', 'photo', 'photography'],
    ['harita', 'map', 'maps'],
    ['müzik', 'music'],
    ['oyun', 'game'],
    # learning and reference
    ['öğretici', 'tutorial'],
    ['alıştırma', 'egzersiz', 'exercise'],
    ['yarışma', 'competition', 'contest'],
    ['dokümantasyon', 'belgelendirme', 'documentation', 'docs'],
    ['kopya kağıdı', 'cheat sheet', 'cheatsheet'],
    ['yol haritası', 'roadmap'],
    ['kitap', 'book', 'ebook'],
    ['sözlük', 'dictionary'],
    ['arşiv', 'archive'],
    ['haber', 'news'],
    ['ücretsiz', 'bedava', 'free'],
    ['çeviri', 'tercüme', 'translation', 'translate'],
    # science, hardware, finance, everyday
    ['matematik', 'mathematics', 'math'],
    ['fizik', 'physics'],
    ['kuantum', 'quantum'],
    ['elektronik', 'electronics'],
    ['donanım', 'hardware'],
    ['akıllı gözlük', 'smart glasses'],
    ['borsa', 'hisse senedi', 'stock market'],
    ['kripto para', 'kripto', 'cryptocurrency', 'crypto'],
    ['e-posta', 'eposta', 'email'],
    ['görev yönetimi', 'yapılacaklar', 'task management', 'todo'],
]
