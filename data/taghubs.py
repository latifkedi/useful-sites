# -*- coding: utf-8 -*-
"""Tag hubs: one static page per tag that is on enough records to be a list.

The app filters by tag (?tag=python), but a crawler never sees that view, and
"every Python resource in the directory" is exactly the kind of page someone
searches for. emit.write_tag_hubs() renders, for each tag on at least MIN_N
records:
  k/t/<slug>.html        Turkish
  k/en/tag/<slug>.html   English

Price tags are left out: "free" sits on four records in five, so its page would
be most of the directory again, and "paid" or "freemium" say nothing about what
a thing is for. 'arşivlenmiş' is left out too -- a page of archived projects is
not a page anyone should land on.

The slug is the tag folded to ASCII (açık-kaynak -> acik-kaynak), so the
address survives being typed, pasted and percent-encoded; test_build checks
that no two tags fold to the same slug.

INTROS holds one hand-written line per tag in each language. Every canonical
tag that could reach MIN_N has one, so a tag crossing the threshold after an
intake gets a page without anyone having to remember to write it.
"""

MIN_N = 12
SKIP = ('ücretsiz', 'freemium', 'ücretli', 'arşivlenmiş', 'açık-kaynak', 'referans')

_FOLD = str.maketrans({'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                       'â': 'a', 'î': 'i', 'û': 'u'})


def slug(tag):
    return tag.translate(_FOLD)


INTROS = {
    'açık-kaynak': ('Kaynak kodu açık, lisansı incelenebilir kayıtlar: kendin çalıştırabilir, '
                    'çatallayabilir ya da katkı verebilirsin.',
                    'Entries whose source is open and whose licence you can read: run them '
                    'yourself, fork them or contribute.'),
    'açık-ağırlık': ('Ağırlıkları indirilebilen modeller ve onları dağıtan yerler; kendi '
                     'donanımında çalıştırmak için.',
                     'Models whose weights you can download, and the places that host them, '
                     'for running on your own hardware.'),
    'dokümantasyon': ('Projelerin resmî belgeleri: bir aracı öğrenirken ilk açılacak, en güncel kaynak.',
                      "Projects' official documentation: the first and most current source when "
                      'learning a tool.'),
    'öğretici': ('Adım adım öğreten yazılar ve rehberler; okuyup yanında uygulamak için.',
                 'Step-by-step tutorials and guides, written to be followed along.'),
    'video': ('İzleyerek öğrenilenler: ders kanalları, konferans kayıtları ve video dersler.',
              'Learning by watching: course channels, conference recordings and video lessons.'),
    'kitap': ('Ücretsiz okunabilen kitaplar ve kitap uzunluğunda metinler.',
              'Books you can read for free, and texts of book length.'),
    'kopya-kâğıdı': ('Tek sayfada özet: komutlar, sözdizimi ve kısayollar, hızlıca bakmak için.',
                     'One-page summaries of commands, syntax and shortcuts, for a quick look.'),
    'awesome-liste': ('Bir konunun derlenmiş listeleri; dizinden sonra bir adım daha derine '
                      'inmek için.',
                      'Curated lists for a single subject, for going one level deeper than '
                      'this directory.'),
    'interaktif': ('Okumak yerine yaparak öğrenilenler: tarayıcıda alıştırma, oyun ve simülasyon.',
                   'Learning by doing rather than reading: exercises, games and simulations '
                   'in the browser.'),
    'müfredat': ('Baştan sona bir yol çizen kurslar, programlar ve yol haritaları.',
                 'Courses, programmes and roadmaps that lay out a route from start to finish.'),
    'referans': ('Okunmaktan çok başvurulan kaynaklar: sözlükler, standartlar, kataloglar ve arşivler.',
                 'Sources you consult rather than read through: glossaries, standards, '
                 'catalogues and archives.'),
    'araç': ('Bir işi gören araçlar: açıp kullandığın, bir şey ürettiğin ya da dönüştürdüğün yerler.',
             'Tools that do a job: things you open and use to make or convert something.'),
    'başlangıç': ('Ön bilgi istemeyen öğrenme kaynakları; bir alana ilk adım için.',
                  'Learning resources that assume nothing; a first step into a field.'),
    'orta': ('Temeli bilen için: bir dili ya da aracı kullanabildikten sonraki adım.',
             'For someone past the basics: the step after you can already use the language '
             'or tool.'),
    'ileri': ('Derinlemesine kaynaklar: iç işleyiş, performans ve uzman konuları.',
              'In-depth resources: internals, performance and expert topics.'),
    'tarayıcı-içi': ('Kurulum gerektirmeyenler: sekmeyi açıp hemen kullanılanlar.',
                     'Nothing to install: open the tab and use it.'),
    'masaüstü': ('Bilgisayara kurulan uygulamalar: düzenleyiciler, istemciler ve araçlar.',
                 'Applications you install on your computer: editors, clients and utilities.'),
    'mobil': ('Telefonda çalışan uygulamalar ve mobil geliştirme kaynakları.',
              'Apps that run on a phone, and resources for building them.'),
    'cli': ('Komut satırında çalışan araçlar; betiklenebilir ve hafif.',
            'Tools that run on the command line; scriptable and light.'),
    'eklenti': ('Tarayıcıya, düzenleyiciye ya da başka bir uygulamaya eklenenler.',
                'Add-ons for a browser, an editor or another application.'),
    'çevrimdışı': ('İnternet bağlantısı olmadan da çalışanlar.',
                   'Things that keep working without an internet connection.'),
    'self-hosted': ('Kendi sunucunda ya da bilgisayarında çalıştırabileceklerin; veri sende kalır.',
                    'Things you can run on your own server or computer; the data stays with you.'),
    'hesap-gerekmez': ('Kayıt olmadan kullanılabilenler: e-posta yok, giriş yok.',
                       'Usable without signing up: no email, no login.'),
    'api': ('Programla erişilebilen hizmetler ve API tasarımı, testi ve belgelenmesi üzerine kaynaklar.',
            'Services you can reach from code, and resources on designing, testing and '
            'documenting APIs.'),
    'sdk': ('Bir hizmeti kendi kodundan kullanmak için resmî geliştirme kitleri.',
            'Official development kits for using a service from your own code.'),
    'python': ('Python ile yazılmış, Python öğreten ya da Python ekosistemine ait kayıtlar.',
               'Entries written in Python, teaching it, or belonging to its ecosystem.'),
    'javascript': ('JavaScript ve TypeScript: dil, çalışma zamanları, çatılar ve araçlar.',
                   'JavaScript and TypeScript: the language, runtimes, frameworks and tooling.'),
    'c-ailesi': ('C, C++ ve C#; sistem programlama, derleyiciler ve düşük seviye kaynaklar.',
                 'C, C++ and C#: systems programming, compilers and low-level resources.'),
    'rust': ('Rust dili, kitapları ve Rust ile yazılmış araçlar.',
             'The Rust language, its books, and tools written in Rust.'),
    'go': ('Go dili, öğrenme kaynakları ve Go ile yazılmış araçlar.',
           'The Go language, resources for learning it, and tools written in Go.'),
    'php': ('PHP dili, çatıları ve ekosistemi.', 'The PHP language, its frameworks and ecosystem.'),
    'jvm': ('Java, Kotlin ve Scala: JVM dilleri, çatıları ve araçları.',
            'Java, Kotlin and Scala: the JVM languages, frameworks and tools.'),
    'docker': ('Konteynerle gelenler ve konteyner dünyasının araçları.',
               'Things shipped as containers, and the tooling of the container world.'),
    'llm': ('Büyük dil modelleri: sohbet asistanları, model sağlayıcılar ve onları kullanan araçlar.',
            'Large language models: chat assistants, model providers and the tools built on them.'),
    'agent': ('Kendi başına adım atan yapay zekâ ajanları: çatılar, bellek ve orkestrasyon.',
              'AI agents that take steps on their own: frameworks, memory and orchestration.'),
    'rag': ('Modeli kendi verine bağlamak: geri getirme, ayrıştırma ve bilgi grafikleri.',
            'Connecting a model to your own data: retrieval, parsing and knowledge graphs.'),
    'embedding': ('Metni vektöre çeviren modeller ve yeniden sıralama.',
                  'Models that turn text into vectors, and rerankers.'),
    'vektör-db': ('Vektörleri saklayıp benzerlikle arayan veritabanları.',
                  'Databases that store vectors and search them by similarity.'),
    'mcp': ('Model Context Protocol: sunucular, kayıt defterleri ve SDK\'lar.',
            'The Model Context Protocol: servers, registries and SDKs.'),
    'guardrail': ('Model çıktısını ve girdisini denetleyen güvenlik katmanları.',
                  'Safety layers that check what goes into and comes out of a model.'),
    'gözlemlenebilirlik': ('İzleme, iz sürme ve değerlendirme: üretimde neyin olup bittiğini görmek.',
                           'Monitoring, tracing and evaluation: seeing what happens in production.'),
    'görsel-üretim': ('Metinden ya da görselden görüntü üreten ve düzenleyen yapay zekâ araçları.',
                      'AI tools that generate or edit images from text or other images.'),
    '3b': ('Üç boyutlu modelleme, tarama ve metinden 3B üretim.',
           'Three-dimensional modelling, scanning and text-to-3D generation.'),
    'ses': ('Konuşmadan metne, metinden konuşmaya ve ses düzenleme.',
            'Speech-to-text, text-to-speech and audio editing.'),
    'otomasyon': ('Tekrarlayan işi makineye bırakmak: iş akışları, kuyruklar ve veri boru hatları.',
                  'Handing repetitive work to a machine: workflows, queues and data pipelines.'),
    'tasarım': ('Renk, yazı tipi, ikon ve arayüz: görsel tasarımın araçları ve ilham kaynakları.',
                'Colour, type, icons and interfaces: the tools and inspiration of visual design.'),
    'frontend': ('Tarayıcıda çalışan taraf: HTML, CSS, bileşenler ve erişilebilirlik.',
                 'The side that runs in the browser: HTML, CSS, components and accessibility.'),
    'backend': ('Sunucu tarafı: çatılar, ORM\'ler, ödeme ve kimlik doğrulama.',
                'The server side: frameworks, ORMs, payments and authentication.'),
    'veritabanı': ('İlişkisel ve ilişkisel olmayan veritabanları, SQL ve veri modelleme.',
                   'Relational and non-relational databases, SQL and data modelling.'),
    'devops': ('Derleme, dağıtım ve altyapı: CI, konteyner düzenleme ve altyapının kodu.',
               'Build, deploy and infrastructure: CI, container orchestration and '
               'infrastructure as code.'),
    'sistem-tasarımı': ('Ölçeklenme, mimari ve tasarım desenleri: sistemi kodun ötesinde düşünmek.',
                        'Scaling, architecture and design patterns: thinking about the system '
                        'beyond the code.'),
    'algoritma': ('Algoritmalar ve veri yapıları: öğrenmek, görselleştirmek ve alıştırma yapmak için.',
                  'Algorithms and data structures, to learn, visualise and practise.'),
    'git': ('Git ve sürüm denetimi: öğreticiler, kopya kâğıtları ve araçlar.',
            'Git and version control: tutorials, cheat sheets and tools.'),
    'sunucu': ('Barındırma, sanal sunucu ve bulut sağlayıcılar.',
               'Hosting, virtual servers and cloud providers.'),
    'güvenlik': ('Saldırı ve savunma, kriptografi, CTF ve güvenlik araçları.',
                 'Offence and defence, cryptography, CTFs and security tooling.'),
    'osint': ('Açık kaynak istihbarat: kişi, alan adı ve görsel üzerine keşif araçları.',
              'Open-source intelligence: reconnaissance tools for people, domains and images.'),
    'gizlilik': ('Kişisel verini korumak: şifreleme, VPN, takma kimlik ve izleyici engelleme.',
                 'Protecting your personal data: encryption, VPNs, aliases and tracker blocking.'),
    'ağ': ('Ağ, Linux ve sistem yönetimi: protokoller, kabuk ve sorun giderme.',
           'Networking, Linux and system administration: protocols, the shell and troubleshooting.'),
    'donanım': ('Elektronik, robotik ve donanım: parçalar, kartlar ve yapım rehberleri.',
                'Electronics, robotics and hardware: parts, boards and build guides.'),
    'gömülü': ('Mikrodenetleyiciler, firmware ve nesnelerin interneti.',
               'Microcontrollers, firmware and the internet of things.'),
    'cad': ('Bilgisayar destekli tasarım: mekanik parça, PCB ve mekân çizimi.',
            'Computer-aided design: mechanical parts, PCBs and floor plans.'),
    'veri-bilimi': ('Veri analizi, istatistik ve makine öğrenmesi: kütüphaneler, kurslar ve platformlar.',
                    'Data analysis, statistics and machine learning: libraries, courses and platforms.'),
    'veri-seti': ('İndirilebilir ya da sorgulanabilir açık veri setleri ve onları bulduğun yerler.',
                  'Open datasets you can download or query, and the places that index them.'),
    'akademik': ('Makale, ön baskı ve bilimsel veri: araştırmanın kaynakları ve arama motorları.',
                 'Papers, preprints and scientific data: the sources and search engines of research.'),
    'kuantum': ('Kuantum bilişim: SDK\'lar, simülatörler ve dersler.',
                'Quantum computing: SDKs, simulators and courses.'),
    'kripto': ('Blokzincir ve kripto paralar: kaşifler, veri ve geliştirme.',
               'Blockchains and cryptocurrencies: explorers, data and development.'),
    'türkçe': ('İçeriği Türkçe olan kaynaklar: belgeler, dersler ve topluluklar.',
               'Resources whose content is in Turkish: documentation, courses and communities.'),
    'mülakat': ('İş görüşmesine hazırlık: kodlama soruları, sistem tasarımı ve kariyer.',
                'Interview preparation: coding questions, system design and career.'),
    'sertifika': ('Sertifika veren kurumlar, sınav hazırlığı ve öğrenci programları.',
                  'Certification bodies, exam preparation and student programmes.'),
}
