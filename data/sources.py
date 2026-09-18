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
"""

SOURCES = {
    'kedi': {
        'label_tr': 'Kedi',
        'label_en': 'Kedi',
        'note_tr': 'Kendi arşivinden, tek tek gözden geçirilmiş',
        'note_en': 'From the curator’s own archive, reviewed one by one',
        'url': None,
    },
    'bwapsv': {
        'label_tr': 'Programcı Siteleri',
        'label_en': 'Programmer Sites',
        'note_tr': 'Best-websites-a-programmer-should-visit derlemesinden geldi (depo Kasım 2025’te arşivlendi)',
        'note_en': 'Surfaced by the Best-websites-a-programmer-should-visit collection (archived November 2025)',
        'url': 'https://github.com/sdmg15/Best-websites-a-programmer-should-visit',
    },
    'cdcruz': {
        'label_tr': 'CDcruz',
        'label_en': 'CDcruz',
        'note_tr': 'cdcruz.com/p/useful_sites.html derlemesinden geldi',
        'note_en': 'Surfaced by the cdcruz.com useful-sites collection',
        'url': 'https://www.cdcruz.com/p/useful_sites.html',
    },
    'awesome-uw': {
        'label_tr': 'Awesome UW',
        'label_en': 'Awesome UW',
        'note_tr': 'awesome-useful-websites derlemesinden geldi',
        'note_en': 'Surfaced by the awesome-useful-websites collection',
        'url': 'https://github.com/atakanaltok/awesome-useful-websites',
    },
    'seccert': {
        'label_tr': 'Sertifika Yol Haritası',
        'label_en': 'Cert Roadmap',
        'note_tr': 'Paul Jerimy’nin güvenlik sertifikası yol haritasından geldi',
        'note_en': 'Surfaced by Paul Jerimy’s security certification roadmap',
        'url': 'https://pauljerimy.com/security-certification-roadmap/',
    },
    'lowkwiki': {
        'label_tr': 'Lowkenuinely Wikis',
        'label_en': 'Lowkenuinely Wikis',
        'note_tr': 'awesome-lowkenuinely-wikis derlemesinden geldi',
        'note_en': 'Surfaced by the awesome-lowkenuinely-wikis collection',
        'url': 'https://github.com/Te1eG0esbrr/awesome-lowkenuinely-wikis',
    },
    'rustlearn': {
        'label_tr': 'Rust Learning',
        'label_en': 'Rust Learning',
        'note_tr': 'ctjhoa/rust-learning derlemesinden geldi',
        'note_en': 'Surfaced by the ctjhoa/rust-learning collection',
        'url': 'https://github.com/ctjhoa/rust-learning',
    },
    'javalinks': {
        'label_tr': 'Faydalı Java',
        'label_en': 'Useful Java',
        'note_tr': 'Vedenin/useful-java-links derlemesinden geldi',
        'note_en': 'Surfaced by Vedenin/useful-java-links',
        'url': 'https://github.com/Vedenin/useful-java-links',
    },
    'mathlinks': {
        'label_tr': 'Matematiği Anlamak',
        'label_en': 'Understanding Math',
        'note_tr': 'nbro/understanding-math derlemesinden geldi',
        'note_en': 'Surfaced by nbro/understanding-math',
        'url': 'https://github.com/nbro/understanding-math',
    },
    'econ': {
        'label_tr': 'Awesome Economics',
        'label_en': 'Awesome Economics',
        'note_tr': 'antontarasenko/awesome-economics derlemesinden geldi',
        'note_en': 'Surfaced by antontarasenko/awesome-economics',
        'url': 'https://github.com/antontarasenko/awesome-economics',
    },
    'dataeng': {
        'label_tr': 'Veri Mühendisi El Kitabı',
        'label_en': 'Data Engineer Handbook',
        'note_tr': 'DataExpert-io/data-engineer-handbook derlemesinden geldi',
        'note_en': 'Surfaced by DataExpert-io/data-engineer-handbook',
        'url': 'https://github.com/DataExpert-io/data-engineer-handbook',
    },
    'dsbest': {
        'label_tr': 'Veri Bilimi Kaynakları',
        'label_en': 'Data Science Best',
        'note_tr': 'tirthajyoti/Data-science-best-resources derlemesinden geldi',
        'note_en': 'Surfaced by tirthajyoti/Data-science-best-resources',
        'url': 'https://github.com/tirthajyoti/Data-science-best-resources',
    },
    'testsites': {
        'label_tr': 'Test Siteleri',
        'label_en': 'Sites to Test On',
        'note_tr': 'BMayhew/awesome-sites-to-test-on derlemesinden geldi',
        'note_en': 'Surfaced by BMayhew/awesome-sites-to-test-on',
        'url': 'https://github.com/BMayhew/awesome-sites-to-test-on',
    },
    'piracy': {
        'label_tr': 'Awesome Piracy',
        'label_en': 'Awesome Piracy',
        'note_tr': 'Igglybuff/awesome-piracy derlemesinden geldi',
        'note_en': 'Surfaced by Igglybuff/awesome-piracy',
        'url': 'https://github.com/Igglybuff/awesome-piracy',
    },
    'awesomelist': {
        'label_tr': 'sindresorhus/awesome',
        'label_en': 'sindresorhus/awesome',
        'note_tr': 'sindresorhus/awesome derlemesinden geldi',
        'note_en': 'Surfaced by sindresorhus/awesome',
        'url': 'https://github.com/sindresorhus/awesome',
    },
    'awesomeproj': {
        'label_tr': 'Awesome Project',
        'label_en': 'Awesome Project',
        'note_tr': 'gdcmarinho/awesome-project derlemesinden geldi',
        'note_en': 'Surfaced by gdcmarinho/awesome-project',
        'url': 'https://github.com/gdcmarinho/awesome-project',
    },
    'quarbby': {
        'label_tr': 'Links & Resources',
        'label_en': 'Links & Resources',
        'note_tr': 'quarbby/links-and-resources derlemesinden geldi',
        'note_en': 'Surfaced by quarbby/links-and-resources',
        'url': 'https://github.com/quarbby/links-and-resources',
    },
    'gmartins': {
        'label_tr': 'gmartins/links',
        'label_en': 'gmartins/links',
        'note_tr': 'gmartins-dev/links derlemesinden geldi',
        'note_en': 'Surfaced by gmartins-dev/links',
        'url': 'https://github.com/gmartins-dev/links',
    },
    'velvia': {
        'label_tr': 'velvia/links',
        'label_en': 'velvia/links',
        'note_tr': 'velvia/links derlemesinden geldi',
        'note_en': 'Surfaced by velvia/links',
        'url': 'https://github.com/velvia/links',
    },
    'invesp': {
        'label_tr': 'Invesp',
        'label_en': 'Invesp',
        'note_tr': 'Invesp’in "109 useful websites" yazısından geldi',
        'note_en': 'Surfaced by Invesp’s "109 useful websites" post',
        'url': 'https://www.invespcro.com/blog/109-useful-websites-online-applications/',
    },
}

DEFAULT = 'kedi'
