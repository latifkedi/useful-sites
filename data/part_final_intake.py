# -*- coding: utf-8 -*-
"""Kalan alanlara son toplu ekleme: araçlar, pratik, backend, ağ, veritabanı,
mobil, devops, yz-araç. Çeşitli listelerden, mevcut kategorilere.
"""

AL = 'awesomelist'
AP = 'awesomeproj'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, cat, src):
        add(url, name, tags, tr, en, cat, src)

    # ---------------------------------------------------------- ARAÇLAR
    a('https://www.caniemail.com/', 'Can I email…', ['referans', 'ücretsiz', 'frontend'],
      'Bir HTML/CSS özelliğinin hangi e-posta istemcisinde çalıştığını gösteren tablo. Web’in Can I '
      'use’undan farkı e-posta istemcilerinin kendine has, kısıtlı desteğine bakması.',
      'A table showing which email client supports an HTML/CSS feature. Unlike the web’s Can I use it '
      'looks at the quirky, limited support of email clients.', 'araclar', AP),
    a('https://cmder.app/', 'Cmder', ['araclar', 'cli', 'açık-kaynak', 'masaüstü'],
      'Windows için taşınabilir, güzel bir konsol paketi; bash ve unix komutlarıyla gelir. Yerleşik '
      'cmd’den farkı sekme, tema ve unix araçlarını bir arada sunması.',
      'A portable, pleasant console package for Windows that ships with bash and unix commands. Unlike '
      'the built-in cmd it offers tabs, themes and unix tools together.', 'araclar', AP),
    a('https://jsoneditoronline.org/', 'JSON Editor Online', ['araclar', 'tarayıcı-içi', 'ücretsiz'],
      'JSON’u ağaç ve metin görünümünde inceleyip düzenleyen tarayıcı aracı. Düz metin '
      'editöründen farkı yapıyı katlayıp doğrulayarak büyük JSON’da gezinmeyi kolaylaştırması.',
      'A browser tool to inspect and edit JSON in tree and text views. Unlike a plain editor it folds '
      'and validates the structure, making large JSON easy to navigate.', 'araclar', AP),
    a('https://www.generatedata.com/', 'generatedata', ['araclar', 'açık-kaynak', 'ücretsiz'],
      'İstenen şemaya göre gerçekçi sahte test verisi üreten araç (CSV, JSON, SQL). Elle veri '
      'uydurmaktan farkı isim, adres gibi alanları tutarlı ve toplu üretmesi.',
      'A tool generating realistic fake test data to a given schema (CSV, JSON, SQL). Unlike making data '
      'up by hand it produces fields like names and addresses consistently and in bulk.', 'araclar', AP),
    a('https://www.connectionstrings.com/', 'ConnectionStrings.com', ['araclar', 'referans', 'veritabanı'],
      'Her veritabanı ve sürücü için doğru bağlantı dizesi biçimini veren başvuru. Dokümanı '
      'aramaktan farkı onlarca sürücünün sözdizimini tek yerde toplaması.',
      'A reference giving the correct connection-string format for every database and driver. Unlike '
      'hunting the docs it gathers the syntax of dozens of drivers in one place.', 'araclar', AP),
    a('https://docsify.js.org/', 'docsify', ['araclar', 'açık-kaynak', 'dokümantasyon', 'javascript'],
      'Markdown dosyalarını derleme olmadan, tarayıcıda dokümantasyon sitesine çeviren araç. Statik '
      'üreticilerden farkı build adımı olmaması — sayfaları anında sunması.',
      'A tool turning Markdown files into a documentation site in the browser, with no build. Unlike '
      'static generators it has no build step — it serves the pages on the fly.', 'araclar', AP),
    a('https://mermaid.js.org/', 'Mermaid', ['araclar', 'açık-kaynak', 'görsel-üretim', 'dokümantasyon'],
      'Akış şeması ve diyagramları metinden üreten araç — “diyagramların Markdown’ı”. Çizim '
      'programlarından farkı diyagramı koda gömüp sürüm kontrolünde tutabilmen.',
      'A tool generating flowcharts and diagrams from text — “Markdown for diagrams”. Unlike drawing '
      'programs you embed the diagram as code and keep it in version control.', 'araclar', K),

    # ---------------------------------------------------------- PRATİK
    a('https://www.theodinproject.com/', 'The Odin Project', ['pratik', 'müfredat', 'ücretsiz', 'açık-kaynak'],
      'Web geliştirmeyi projeler üzerinden, tam bir açık müfredatla öğreten platform. Video kurslardan '
      'farkı kendi ortamını kurdurup gerçek proje inşa ettirmesi.',
      'A platform teaching web development through projects, with a full open curriculum. Unlike video '
      'courses it has you set up your own environment and build real projects.', 'pratik', AP),
    a('https://www.geeksforgeeks.org/', 'GeeksforGeeks', ['pratik', 'referans', 'ücretsiz', 'algoritma'],
      'Algoritma, veri yapısı ve mülakat sorularının çok geniş yazı arşivi. Tek konulu sitelerden farkı '
      'neredeyse her CS konusuna çözümlü örnek bulundurması.',
      'A very broad article archive of algorithms, data structures and interview questions. Unlike '
      'single-topic sites it has a worked example for almost every CS topic.', 'pratik', AP),
    a('https://rosettacode.org/', 'Rosetta Code', ['pratik', 'referans', 'ücretsiz'],
      'Aynı küçük problemi yüzlerce dilde çözülmüş hâlde gösteren wiki. Tek dilli örneklerden farkı bir '
      'görevin dillerde nasıl farklılaştığını yan yana göstermesi.',
      'A wiki showing the same small problem solved in hundreds of languages. Unlike single-language '
      'examples it shows side by side how a task differs across languages.', 'pratik', AP),
    a('https://edabit.com/', 'Edabit', ['pratik', 'interaktif', 'freemium'],
      'Küçük, ısırıklık kodlama bulmacalarıyla dil pratiği yaptıran site. Büyük problem setlerinden farkı '
      'zorluğu kademelendirip hızlı geri bildirim vermesi.',
      'A site for practising a language with small, bite-sized coding puzzles. Unlike large problem sets '
      'it grades difficulty and gives fast feedback.', 'pratik', AP),
    a('https://devchallenges.io/', 'devChallenges.io', ['pratik', 'frontend', 'ücretsiz'],
      'Gerçekçi tasarım ve gereksinimlerle web projeleri kurduran meydan okuma sitesi. Rastgele '
      'projelerden farkı çözümleri topluluğun değerlendirmesi.',
      'A challenge site that has you build web projects with realistic designs and requirements. Unlike '
      'random projects the community reviews the solutions.', 'pratik', AP),

    # ---------------------------------------------------------- BACKEND
    a('https://any-api.com/', 'Any API', ['backend', 'api', 'referans', 'ücretsiz'],
      'Yüzlerce herkese açık API’nin belge ve konsolunu tek yerde toplayan dizin. Tek tek API '
      'sitelerinden farkı hepsini ortak bir arayüzde deneyebilmen.',
      'A directory gathering the docs and console of hundreds of public APIs in one place. Unlike '
      'individual API sites you can try them all in a common interface.', 'backend', AP),
    a('https://github.com/mjhea0/awesome-fastapi', 'Awesome FastAPI', ['awesome-liste', 'github', 'python', 'api'],
      'Python’un hızlı web çatısı FastAPI için eklenti, örnek ve öğretici listesi. Resmî dokümandan farkı '
      'topluluk kütüphanelerini ve üretim örneklerini toplaması.',
      'A list of plugins, examples and tutorials for FastAPI, Python’s fast web framework. Unlike the '
      'official docs it gathers community libraries and production examples.', 'backend', AL),

    # ---------------------------------------------------------- AĞ & SİSTEM
    a('https://linuxjourney.com/', 'Linux Journey', ['ag', 'öğretici', 'ücretsiz'],
      'Linux’u sıfırdan, sıralı ve alıştırmalı biçimde öğreten ücretsiz site. Man sayfalarından farkı '
      'kavramları yeni başlayana göre, mantık sırasıyla anlatması.',
      'A free site teaching Linux from scratch, in order and with exercises. Unlike man pages it explains '
      'concepts for a beginner, in a logical sequence.', 'ag', AP),
    a('https://www.brendangregg.com/', 'Brendan Gregg', ['ag', 'referans', 'ücretsiz', 'gözlemlenebilirlik'],
      'Linux performans ve gözlemlenebilirliğinde başvurulan uzmanın blogu ve araçları. Genel '
      'kılavuzlardan farkı çekirdek düzeyinde ölçüm ve alev grafiği (flame graph) yöntemlerini vermesi.',
      'The blog and tools of the go-to expert on Linux performance and observability. Unlike general '
      'guides it gives kernel-level measurement and flame-graph methods.', 'ag', K),
    a('https://github.com/secdev/awesome-scapy', 'Awesome Scapy', ['awesome-liste', 'github', 'ag', 'python'],
      'Python paket işleme kütüphanesi Scapy için araç ve örnek listesi. Genel ağ listelerinden farkı '
      'paketi elle kurup gönderme (packet crafting) etrafında toplanması.',
      'A list of tools and examples for Scapy, the Python packet-manipulation library. Unlike general '
      'network lists it centres on crafting and sending packets by hand.', 'ag', AL),

    # ---------------------------------------------------------- VERİTABANI
    a('https://github.com/dhamaniasad/awesome-postgres', 'Awesome Postgres', ['awesome-liste', 'github', 'veritabanı'],
      'PostgreSQL için eklenti, araç ve kaynak listesi. Resmî dokümandan farkı ekosistemin '
      'uzantılarını ve yönetim araçlarını bir arada göstermesi.',
      'A list of extensions, tools and resources for PostgreSQL. Unlike the official docs it shows the '
      'ecosystem’s extensions and management tools together.', 'veritabani', AL),
    a('https://github.com/ramnes/awesome-mongodb', 'Awesome MongoDB', ['awesome-liste', 'github', 'veritabanı'],
      'Belge tabanlı NoSQL veritabanı MongoDB için kütüphane ve araç listesi. Genel NoSQL '
      'listelerinden farkı tek ürünün sürücü ve ODM ekosistemine odaklanması.',
      'A list of libraries and tools for MongoDB, the document-based NoSQL database. Unlike general NoSQL '
      'lists it focuses on one product’s driver and ODM ecosystem.', 'veritabani', AL),
    a('https://github.com/mgramin/awesome-db-tools', 'Awesome DB Tools', ['awesome-liste', 'github', 'veritabanı'],
      'Veritabanıyla çalışmayı kolaylaştıran araçların (istemci, göç, şema) listesi. Tek veritabanına '
      'bağlı listelerden farkı motor-bağımsız yardımcı araçlara bakması.',
      'A list of tools that make working with databases easier (clients, migration, schema). Unlike '
      'single-database lists it looks at engine-agnostic helper tools.', 'veritabani', AL),
    a('https://supabase.com/', 'Supabase', ['veritabanı', 'backend', 'açık-kaynak', 'freemium'],
      'Postgres üstüne kimlik doğrulama, API ve depolama ekleyen açık kaynak Firebase alternatifi. '
      'Firebase’den farkı ilişkisel Postgres üstünde durması ve kendini barındırabilmen.',
      'An open-source Firebase alternative adding auth, APIs and storage on top of Postgres. Unlike '
      'Firebase it stands on relational Postgres and can be self-hosted.', 'veritabani', K),
    a('https://pocketbase.io/', 'PocketBase', ['veritabanı', 'backend', 'açık-kaynak', 'go'],
      'Tek Go dosyasında gelen; SQLite, kimlik doğrulama ve gerçek zamanlı API sunan backend. Ağır '
      'yığınlardan farkı sunucuyu tek çalıştırılabilir dosyaya indirmesi.',
      'A backend shipping as one Go file, providing SQLite, auth and a real-time API. Unlike heavy stacks '
      'it reduces the server to a single executable.', 'veritabani', K),

    # ---------------------------------------------------------- MOBİL
    a('https://github.com/vsouza/awesome-ios', 'Awesome iOS', ['awesome-liste', 'github', 'masaüstü'],
      'iOS geliştirme için kütüphane, araç ve öğrenme kaynağı listesi. Genel Apple listelerinden farkı '
      'yalnız iOS uygulama katmanına ve Swift/Obj-C ekosistemine odaklanması.',
      'A list of libraries, tools and learning resources for iOS development. Unlike general Apple lists '
      'it focuses on the iOS app layer and the Swift/Obj-C ecosystem.', 'mobil', AL),
    a('https://xdaforums.com/', 'XDA Forums', ['mobil', 'referans', 'ücretsiz'],
      'Android cihaz modlama, ROM ve root topluluğunun en büyük forumu. Genel forumlardan farkı cihaz '
      'model model, derinlemesine teknik konulara bölünmüş olması.',
      'The largest community forum for Android device modding, ROMs and root. Unlike general forums it is '
      'split device by device into deep technical threads.', 'mobil', AP),

    # ---------------------------------------------------------- DEVOPS
    a('https://www.cloudflare.com/', 'Cloudflare', ['devops', 'ag', 'güvenlik', 'freemium'],
      'CDN, DNS, DDoS koruması ve kenar hesaplamayı tek platformda sunan altyapı. Ayrı hizmetlerden '
      'farkı bunları tek panelde birleştirip cömert bir ücretsiz katman vermesi.',
      'Infrastructure offering CDN, DNS, DDoS protection and edge computing in one platform. Unlike '
      'separate services it unites them in one dashboard with a generous free tier.', 'devops', AP),
    a('https://github.com/ramitsurana/awesome-kubernetes', 'Awesome Kubernetes', ['awesome-liste', 'github', 'devops', 'docker'],
      'Kubernetes ekosistemi için araç, öğretici ve üretim deneyimi listesi. Resmî dokümandan farkı '
      'topluluk araçlarını ve gerçek dünya kalıplarını bir arada toplaması.',
      'A list of tools, tutorials and production experience for the Kubernetes ecosystem. Unlike the '
      'official docs it gathers community tools and real-world patterns together.', 'devops', AL),

    # ---------------------------------------------------------- YZ ARAÇ (awesome)
    a('https://github.com/steven2358/awesome-generative-ai', 'Awesome Generative AI', ['awesome-liste', 'github', 'llm', 'görsel-üretim'],
      'Metin, görsel ve sesi üreten yapay zekâ araç ve projelerinin listesi. Tek ürün sayfalarından '
      'farkı alanı kategori kategori haritalayıp hızlı gelişmeyi takip etmesi.',
      'A list of AI tools and projects that generate text, images and audio. Unlike single product pages '
      'it maps the field category by category and tracks its fast movement.', 'yz_arac', AL),
    a('https://github.com/altamiracorp/awesome-xai', 'Awesome XAI', ['awesome-liste', 'github', 'llm', 'veri-bilimi'],
      'Açıklanabilir yapay zekâ (XAI) — modelin neden öyle karar verdiğini gösteren yöntemler listesi. '
      'Genel ML listelerinden farkı yalnız yorumlanabilirliğe odaklanması.',
      'A list of methods for explainable AI (XAI) — showing why a model decided as it did. Unlike '
      'general ML lists it focuses only on interpretability.', 'yz_arac', AL),
