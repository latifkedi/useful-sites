# -*- coding: utf-8 -*-
"""Where each record came from.

The directory holds records of several origins, and they are not equally
reliable:

  kedi   : From the owner's own bookmark archive, gone through one by one.
           Descriptions written against each project's own documentation.
  others : Surfaced by an outside compilation. The source list is named and
           linked; each entry was checked to be alive and in scope, and the
           description was written here rather than copied -- but it was not
           part of the original archive and carries less first-hand use.

Letting the reader see that difference is a matter of honesty. Not every
record was held to the same standard, and pretending otherwise would kill the
directory.

Every source also carries its terms, for the credits page:

  licence       : the upstream's SPDX id (MIT, CC0-1.0, CC-BY-4.0, ...), or
                  'unspecified' (no licence stated anywhere) or
                  'all-rights-reserved' (a page that says so, or a platform
                  whose default is that)
  copyright     : who holds it, as the upstream names them
  licence_note  : optional; how the licence was established when GitHub's
                  own detection was missing or wrong

Only names, addresses and the fact of inclusion are taken from a source; the
descriptions are written here. data/test_repo.py fails on a source without
licence and copyright.
"""

SOURCES = {
    'kedi': {
        'label_tr': 'Kedi',
        'label_en': 'Kedi',
        'note_tr': 'Kendi arşivinden, tek tek gözden geçirilmiş',
        'note_en': 'From the curator’s own archive, reviewed one by one',
        'url': None,
        'licence': 'CC-BY-4.0',
        'copyright': 'latifkedi',
    },
    'bwapsv': {
        'label_tr': 'Programcı Siteleri',
        'label_en': 'Programmer Sites',
        'note_tr': 'Best-websites-a-programmer-should-visit derlemesinden geldi (depo Kasım 2025’te arşivlendi)',
        'note_en': 'Surfaced by the Best-websites-a-programmer-should-visit collection (archived November 2025)',
        'url': 'https://github.com/sdmg15/Best-websites-a-programmer-should-visit',
        'licence': 'MIT',
        'copyright': '2017 Sonkeng Maldini',
    },
    'cdcruz': {
        'label_tr': 'CDcruz',
        'label_en': 'CDcruz',
        'note_tr': 'cdcruz.com/p/useful_sites.html derlemesinden geldi',
        'note_en': 'Surfaced by the cdcruz.com useful-sites collection',
        'url': 'https://www.cdcruz.com/p/useful_sites.html',
        'licence': 'unspecified',
        'copyright': 'CDcruz',
        'licence_note': 'The page states no licence; only names and addresses were taken, the descriptions are written here.',
    },
    'awesome-uw': {
        'label_tr': 'Awesome UW',
        'label_en': 'Awesome UW',
        'note_tr': 'awesome-useful-websites derlemesinden geldi',
        'note_en': 'Surfaced by the awesome-useful-websites collection',
        'url': 'https://github.com/atakanaltok/awesome-useful-websites',
        'licence': 'CC-BY-4.0',
        'copyright': 'atakanaltok and contributors',
        'licence_note': 'GitHub reports NOASSERTION; the LICENSE file is CC BY 4.0.',
    },
    'seccert': {
        'label_tr': 'Sertifika Yol Haritası',
        'label_en': 'Cert Roadmap',
        'note_tr': 'Paul Jerimy’nin güvenlik sertifikası yol haritasından geldi',
        'note_en': 'Surfaced by Paul Jerimy’s security certification roadmap',
        'url': 'https://pauljerimy.com/security-certification-roadmap/',
        'licence': 'unspecified',
        'copyright': 'Paul Jerimy',
        'licence_note': 'No licence is stated for the roadmap itself (the site theme is GPL-2.0, which covers code, not content).',
    },
    'secretknowledge': {
        'label_tr': 'The Book of Secret Knowledge',
        'label_en': 'The Book of Secret Knowledge',
        'note_tr': 'the-book-of-secret-knowledge derlemesinden geldi',
        'note_en': 'Surfaced by the-book-of-secret-knowledge collection',
        'url': 'https://github.com/trimstray/the-book-of-secret-knowledge',
        'licence': 'MIT',
        'copyright': '2017 trimstray',
    },
    'lowkwiki': {
        'label_tr': 'Lowkenuinely Wikis',
        'label_en': 'Lowkenuinely Wikis',
        'note_tr': 'awesome-lowkenuinely-wikis derlemesinden geldi',
        'note_en': 'Surfaced by the awesome-lowkenuinely-wikis collection',
        'url': 'https://github.com/Te1eG0esbrr/awesome-lowkenuinely-wikis',
        'licence': 'CC0-1.0',
        'copyright': 'Te1eG0esbrr and contributors',
    },
    'rustlearn': {
        'label_tr': 'Rust Learning',
        'label_en': 'Rust Learning',
        'note_tr': 'ctjhoa/rust-learning derlemesinden geldi',
        'note_en': 'Surfaced by the ctjhoa/rust-learning collection',
        'url': 'https://github.com/ctjhoa/rust-learning',
        'licence': 'unspecified',
        'copyright': 'ctjhoa and contributors',
        'licence_note': 'The repository has no licence file.',
    },
    'javalinks': {
        'label_tr': 'Faydalı Java',
        'label_en': 'Useful Java',
        'note_tr': 'Vedenin/useful-java-links derlemesinden geldi',
        'note_en': 'Surfaced by Vedenin/useful-java-links',
        'url': 'https://github.com/Vedenin/useful-java-links',
        'licence': 'CC-BY-SA-4.0',
        'copyright': 'Vedenin and contributors',
        'licence_note': 'GitHub reports NOASSERTION; license.md names CC BY-SA 4.0.',
    },
    'mathlinks': {
        'label_tr': 'Matematiği Anlamak',
        'label_en': 'Understanding Math',
        'note_tr': 'nbro/understanding-math derlemesinden geldi',
        'note_en': 'Surfaced by nbro/understanding-math',
        'url': 'https://github.com/nbro/understanding-math',
        'licence': 'unspecified',
        'copyright': 'nbro and contributors',
        'licence_note': 'The repository has no licence file.',
    },
    'econ': {
        'label_tr': 'Awesome Economics',
        'label_en': 'Awesome Economics',
        'note_tr': 'antontarasenko/awesome-economics derlemesinden geldi',
        'note_en': 'Surfaced by antontarasenko/awesome-economics',
        'url': 'https://github.com/antontarasenko/awesome-economics',
        'licence': 'CC0-1.0',
        'copyright': 'antontarasenko and contributors',
        'licence_note': 'No licence file; the README declares CC0.',
    },
    'dataeng': {
        'label_tr': 'Veri Mühendisi El Kitabı',
        'label_en': 'Data Engineer Handbook',
        'note_tr': 'DataExpert-io/data-engineer-handbook derlemesinden geldi',
        'note_en': 'Surfaced by DataExpert-io/data-engineer-handbook',
        'url': 'https://github.com/DataExpert-io/data-engineer-handbook',
        'licence': 'unspecified',
        'copyright': 'DataExpert-io and contributors',
        'licence_note': 'The repository has no licence file.',
    },
    'dsbest': {
        'label_tr': 'Veri Bilimi Kaynakları',
        'label_en': 'Data Science Best',
        'note_tr': 'tirthajyoti/Data-science-best-resources derlemesinden geldi',
        'note_en': 'Surfaced by tirthajyoti/Data-science-best-resources',
        'url': 'https://github.com/tirthajyoti/Data-science-best-resources',
        'licence': 'MIT',
        'copyright': '2018 Tirthajyoti Sarkar',
    },
    'testsites': {
        'label_tr': 'Test Siteleri',
        'label_en': 'Sites to Test On',
        'note_tr': 'BMayhew/awesome-sites-to-test-on derlemesinden geldi',
        'note_en': 'Surfaced by BMayhew/awesome-sites-to-test-on',
        'url': 'https://github.com/BMayhew/awesome-sites-to-test-on',
        'licence': 'unspecified',
        'copyright': 'BMayhew and contributors',
        'licence_note': 'The repository has no licence file.',
    },
    'piracy': {
        'label_tr': 'Awesome Piracy',
        'label_en': 'Awesome Piracy',
        'note_tr': 'Igglybuff/awesome-piracy derlemesinden geldi',
        'note_en': 'Surfaced by Igglybuff/awesome-piracy',
        'url': 'https://github.com/Igglybuff/awesome-piracy',
        'licence': 'CC0-1.0',
        'copyright': 'Igglybuff and contributors',
    },
    'awesomelist': {
        'label_tr': 'sindresorhus/awesome',
        'label_en': 'sindresorhus/awesome',
        'note_tr': 'sindresorhus/awesome derlemesinden geldi',
        'note_en': 'Surfaced by sindresorhus/awesome',
        'url': 'https://github.com/sindresorhus/awesome',
        'licence': 'CC0-1.0',
        'copyright': 'Sindre Sorhus and contributors',
    },
    'awesomeproj': {
        'label_tr': 'Awesome Project',
        'label_en': 'Awesome Project',
        'note_tr': 'gdcmarinho/awesome-project derlemesinden geldi',
        'note_en': 'Surfaced by gdcmarinho/awesome-project',
        'url': 'https://github.com/gdcmarinho/awesome-project',
        'licence': 'MIT',
        'copyright': '2022 Awesome Project',
    },
    'velvia': {
        'label_tr': 'velvia/links',
        'label_en': 'velvia/links',
        'note_tr': 'velvia/links derlemesinden geldi',
        'note_en': 'Surfaced by velvia/links',
        'url': 'https://github.com/velvia/links',
        'licence': 'unspecified',
        'copyright': 'velvia',
        'licence_note': 'The repository has no licence file.',
    },
    'trekhleb': {
        'label_tr': 'Girişimini Tanıt',
        'label_en': 'Promote Your Next Startup',
        'note_tr': 'trekhleb/promote-your-next-startup derlemesinden geldi',
        'note_en': 'Surfaced by trekhleb/promote-your-next-startup',
        'url': 'https://github.com/trekhleb/promote-your-next-startup',
        'licence': 'Unlicense',
        'copyright': 'trekhleb and contributors',
    },
    'littlelink': {
        'label_tr': 'LittleLink',
        'label_en': 'LittleLink',
        'note_tr': 'sethcottle/littlelink deposundan geldi',
        'note_en': 'Surfaced by sethcottle/littlelink',
        'url': 'https://github.com/sethcottle/littlelink',
        'licence': 'MIT',
        'copyright': '2019-2024 Seth Cottle',
    },
    'cryptolist': {
        'label_tr': 'CryptoList',
        'label_en': 'CryptoList',
        'note_tr': 'coinpride/CryptoList derlemesinden geldi',
        'note_en': 'Surfaced by coinpride/CryptoList',
        'url': 'https://github.com/coinpride/CryptoList',
        'licence': 'CC-BY-SA-4.0',
        'copyright': 'coinpride and contributors',
        'licence_note': 'No licence file; the README declares CC BY-SA 4.0.',
    },
    'pycrumbs': {
        'label_tr': 'Pycrumbs',
        'label_en': 'Pycrumbs',
        'note_tr': 'kirang89/pycrumbs derlemesinden geldi',
        'note_en': 'Surfaced by kirang89/pycrumbs',
        'url': 'https://github.com/kirang89/pycrumbs',
        'licence': 'Unlicense',
        'copyright': 'kirang89 and contributors',
    },
    'favlink': {
        'label_tr': 'Favorite Link',
        'label_en': 'Favorite Link',
        'note_tr': 'guanguans/favorite-link derlemesinden geldi',
        'note_en': 'Surfaced by guanguans/favorite-link',
        'url': 'https://github.com/guanguans/favorite-link',
        'licence': 'GPL-3.0',
        'copyright': 'guanguans and contributors',
        'licence_note': 'SPDX id as GitHub reports it; "only" or "or later" is not stated.',
    },
    'tafrali': {
        'label_tr': 'Veri Kaynakları (Tafralı)',
        'label_en': 'Data Sources (Tafralı)',
        'note_tr': 'Serdar Tafralı’nın "Veri Bilimi Projeleri için Veri Kaynakları" yazısından geldi',
        'note_en': 'Surfaced by Serdar Tafralı’s "Data Sources for Data Science Projects" post',
        'url': 'https://serdartafrali.medium.com/veri-bilimi-projeleri-i%C3%A7in-veri-kaynaklar%C4%B1-ceece4d0aeb8',
        'licence': 'all-rights-reserved',
        'copyright': 'Serdar Tafralı',
        'licence_note': 'A Medium post with no licence stated, so all rights reserved by default.',
    },
    'invesp': {
        'label_tr': 'Invesp',
        'label_en': 'Invesp',
        'note_tr': 'Invesp’in "109 useful websites" yazısından geldi',
        'note_en': 'Surfaced by Invesp’s "109 useful websites" post',
        'url': 'https://www.invespcro.com/blog/109-useful-websites-online-applications/',
        'licence': 'all-rights-reserved',
        'copyright': 'Invesp',
        'licence_note': 'The page footer reads "© 2006-2020 All rights reserved. Invesp".',
    },
    'bosluk': {
        'label_tr': 'Boşluk Taraması',
        'label_en': 'Gap Review',
        'note_tr': 'Ekim 2026 kapsam taramasında eklendi (Türkiye kamu verisi, LaTeX, CBS, WebAssembly, '
                   'erişilebilirlik, regex, araştırma araçları); her adres açılıp denetlendi',
        'note_en': 'Added in the October 2026 coverage review (Turkish public data, LaTeX, GIS, WebAssembly, '
                   'accessibility, regex, research tools); each address was opened and checked',
        'url': None,
        'licence': 'CC-BY-4.0',
        'copyright': 'latifkedi',
    },
    # Written by from_issue.py for a submission approved through the issue form.
    # The form's required consent box puts the submitted description text under
    # CC BY 4.0, the same terms as the rest of the directory.
    'community': {
        'label_tr': 'Topluluk Önerileri',
        'label_en': 'Community suggestions',
        'note_tr': 'Öneri formuyla gönderildi; açıklama yayından önce elden geçirildi',
        'note_en': 'Suggested through the issue form; the description was reviewed before publishing',
        'url': None,
        'licence': 'CC-BY-4.0',
        'copyright': 'the submitters (consent given in the issue form)',
    },
}

DEFAULT = 'kedi'
