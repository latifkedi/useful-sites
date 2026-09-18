# -*- coding: utf-8 -*-
"""Rust — ctjhoa/rust-learning'den kanonik olanlar + birkaç eksik.

Kaynak listede yüzlerce tek tek blog yazısı ve konuşma vardı; buraya dilin
kalıcı, resmî ve en çok atıf alan kaynakları alındı.
"""

R = 'rustlearn'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, src=R):
        add(url, name, tags, tr, en, 'diller', src)

    a('https://doc.rust-lang.org/book/', 'The Rust Programming Language', ['rust', 'kitap', 'ücretsiz', 'öğretici'],
      'Rust’ı sıfırdan öğreten resmî kitap (“the book”). Üçüncü parti öğreticilerden farkı sahiplik ve '
      'ödünç alma modelini adım adım, dilin kendi ekibinin ağzından kurması.',
      'The official book teaching Rust from scratch (“the book”). Unlike third-party tutorials it builds '
      'the ownership and borrowing model step by step, from the language team itself.'),
    a('https://doc.rust-lang.org/rust-by-example/', 'Rust by Example', ['rust', 'interaktif', 'ücretsiz'],
      'Her kavramı çalıştırılabilir, düzenlenebilir kod örneğiyle veren resmî kaynak. Kitaptan farkı '
      'anlatıyı kısıp örneği öne alması — deneyerek öğrenenler için.',
      'The official resource giving each concept as a runnable, editable code example. Unlike the book it '
      'cuts the prose and leads with the example — for those who learn by trying.'),
    a('https://doc.rust-lang.org/std/', 'Rust Standard Library', ['rust', 'dokümantasyon', 'referans', 'ücretsiz'],
      'Rust standart kütüphanesinin resmî referansı — tip, trait ve makrolar. Öğreticilerden farkı '
      'öğretmeye değil, tam ve kesin başvuruya yönelmesi.',
      'The official reference for the Rust standard library — types, traits and macros. Unlike tutorials '
      'it aims not to teach but to be the complete, exact reference.', K),
    a('https://doc.rust-lang.org/reference/', 'The Rust Reference', ['rust', 'dokümantasyon', 'referans'],
      'Dilin dilbilgisini ve anlamını tanımlayan resmî başvuru. Kitaptan farkı öğretici değil, '
      '“Rust tam olarak nasıl davranır” sorusunun yetkili cevabı olması.',
      'The official reference defining the language’s grammar and semantics. Unlike the book it is not a '
      'tutorial but the authoritative answer to “exactly how does Rust behave”.'),
    a('https://doc.rust-lang.org/nomicon/', 'The Rustonomicon', ['rust', 'kitap', 'ücretsiz', 'referans'],
      'Güvensiz (unsafe) Rust’ın kurallarını anlatan ileri düzey kitap. Ana kitaptan farkı ödünç '
      'denetçisinin dışına çıkıldığında nelere dikkat edileceğini kapsaması.',
      'An advanced book on the rules of unsafe Rust. Unlike the main book it covers what to watch for '
      'when you step outside the borrow checker.'),
    a('https://rust-lang.github.io/async-book/', 'The Async Book', ['rust', 'kitap', 'ücretsiz', 'öğretici'],
      'Rust’ta async/await ve Future modelini anlatan resmî kitap. Genel eşzamanlılık anlatımından farkı '
      'Rust’ın kendine özgü, ayrıştırılmış çalışma zamanı yaklaşımını açması.',
      'The official book on async/await and the Future model in Rust. Unlike general concurrency material '
      'it explains Rust’s distinctive, decoupled runtime approach.'),
    a('https://doc.rust-lang.org/cargo/', 'The Cargo Book', ['rust', 'dokümantasyon', 'ücretsiz'],
      'Rust’ın paket yöneticisi ve derleme aracı Cargo’nun resmî kılavuzu. Dağınık bloglardan farkı '
      'bağımlılık, çalışma alanı ve yayımlamayı tek yetkili yerde toplaması.',
      'The official guide to Cargo, Rust’s package manager and build tool. Unlike scattered blogs it '
      'gathers dependencies, workspaces and publishing in one authoritative place.'),
    a('https://github.com/rust-lang/rustlings', 'Rustlings', ['rust', 'interaktif', 'açık-kaynak', 'github'],
      'Küçük, kırık kod parçalarını düzelterek Rust öğreten alıştırma seti. Okuma temelli kaynaklardan '
      'farkı derleyici hatalarını okuyup düzeltmeyi elle deneyimletmesi.',
      'An exercise set teaching Rust by fixing small, broken snippets. Unlike reading-based resources it '
      'has you read and fix compiler errors by hand.'),
    a('https://play.rust-lang.org/', 'Rust Playground', ['rust', 'tarayıcı-içi', 'ücretsiz', 'interaktif'],
      'Rust kodunu kurulum olmadan tarayıcıda derleyip çalıştıran resmî alan. Yerel kurulumdan farkı '
      'derleyici çıktısını ve ASM/MIR’i paylaşılabilir bağlantıyla vermesi.',
      'The official space to compile and run Rust code in the browser with no install. Unlike a local '
      'setup it gives compiler output and ASM/MIR via a shareable link.'),
    a('https://crates.io/', 'crates.io', ['rust', 'referans', 'açık-kaynak'],
      'Rust’ın resmî paket kayıt defteri — kütüphaneleri yayımlayıp bağımlılık olarak çekmenin merkezi. '
      'Genel kod aramalarından farkı sürüm ve indirme verisiyle güvenilir kaynağı göstermesi.',
      'Rust’s official package registry — the hub for publishing libraries and pulling them as '
      'dependencies. Unlike general code search it shows the trustworthy source with version and '
      'download data.', K),
    a('https://docs.rs/', 'docs.rs', ['rust', 'dokümantasyon', 'referans', 'ücretsiz'],
      'crates.io’daki her paketin belgelerini otomatik derleyip yayımlayan servis. Her projenin kendi '
      'sitesinden farkı tüm ekosistemin dokümanını tek biçim ve tek adreste toplaması.',
      'A service that automatically builds and publishes the docs for every package on crates.io. Unlike '
      'each project’s own site it gathers the whole ecosystem’s docs in one format at one address.', K),
    a('https://this-week-in-rust.org/', 'This Week in Rust', ['rust', 'ücretsiz', 'referans'],
      'Rust dünyasındaki gelişmeleri, yeni sürüm ve yazıları haftalık derleyen bülten. Dağınık '
      'takipten farkı ekosistemi tek, düzenli akışta izlemeni sağlaması.',
      'A newsletter rounding up developments, releases and posts in the Rust world weekly. Unlike '
      'scattered following it lets you track the ecosystem in one regular stream.', K),
    a('https://github.com/rust-unofficial/awesome-rust', 'Awesome Rust', ['rust', 'awesome-liste', 'github', 'referans'],
      'Rust kütüphane ve uygulamalarını konuya göre düzenleyen liste. crates.io aramasından farkı '
      'seçilmiş, kategorilenmiş ve bakımı yapılan bir başlangıç haritası olması.',
      'A list organising Rust libraries and applications by topic. Unlike a crates.io search it is a '
      'curated, categorised and maintained starting map.'),
    a('https://google.github.io/comprehensive-rust/', 'Comprehensive Rust', ['rust', 'müfredat', 'ücretsiz'],
      'Google’ın dört günlük, slayt + alıştırma biçiminde açık Rust kursu. Kitaptan farkı sınıf ortamı '
      'için tempolu, gömülü ve eşzamanlılık modülleriyle gelmesi.',
      'Google’s open four-day Rust course as slides + exercises. Unlike the book it is paced for a '
      'classroom and comes with embedded and concurrency modules.', K),
    a('https://tokio.rs/', 'Tokio', ['rust', 'açık-kaynak', 'backend', 'dokümantasyon'],
      'Rust için en yaygın asenkron çalışma zamanı; ağ servisleri bunun üstüne kurulur. Standart '
      'kütüphaneden farkı yüksek eşzamanlı G/Ç için zamanlayıcı, görev ve araçları getirmesi.',
      'The most widely used asynchronous runtime for Rust; network services build on it. Unlike the '
      'standard library it brings a scheduler, tasks and tooling for highly concurrent I/O.', K),
