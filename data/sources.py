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
    'invesp': {
        'label_tr': 'Invesp',
        'label_en': 'Invesp',
        'note_tr': 'Invesp’in "109 useful websites" yazısından geldi',
        'note_en': 'Surfaced by Invesp’s "109 useful websites" post',
        'url': 'https://www.invespcro.com/blog/109-useful-websites-online-applications/',
    },
}

DEFAULT = 'kedi'
