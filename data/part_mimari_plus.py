# -*- coding: utf-8 -*-
"""Kalan alanları tamamlar: Mimari (yapı), Backend (yazılım mimarisi),
Donanım, Kuantum, Bilim.

Mimari alanı kaynak repolarda neredeyse boştu (gelenler yazılım mimarisiydi;
onlar Backend'e kondu). Yapı mimarisi tarafı burada kanonik kaynaklarla elle
kürelendi. Diğer üç alana harvest'ten iyi listeler ve birkaç kanonik eklendi.
"""

K = 'kedi'
AL = 'awesomelist'


def load(add):
    def a(url, name, tags, tr, en, cat, src=K):
        add(url, name, tags, tr, en, cat, src)

    # ==================================================== MİMARİ & YAPI (bina)
    a('https://www.archdaily.com/', 'ArchDaily', ['referans', 'görsel-üretim', 'ücretsiz'],
      'Dünyanın en büyük mimari yayını — günlük proje, çizim ve malzeme haberi. Pinterest tarzı '
      'panolardan farkı her projeyi plan, kesit ve mimarın açıklamasıyla vermesi.',
      'The world’s largest architecture publication — daily projects, drawings and material news. '
      'Unlike Pinterest-style boards it presents each project with plans, sections and the architect’s '
      'statement.', 'mimari'),
    a('https://www.dezeen.com/', 'Dezeen', ['referans', 'görsel-üretim', 'ücretsiz'],
      'Mimari ve tasarımı gazetecilik diliyle işleyen dergi. ArchDaily’nin proje arşivinden farkı '
      'habere, söyleşiye ve eleştiriye ağırlık vermesi.',
      'A magazine covering architecture and design with a journalistic voice. Unlike ArchDaily’s project '
      'archive it leans on news, interviews and criticism.', 'mimari'),
    a('https://architizer.com/', 'Architizer', ['referans', 'görsel-üretim', 'freemium'],
      'Mimari projeleri ve yapı ürünlerini birlikte dizinleyen platform. Salt ilham sitelerinden farkı '
      'projede kullanılan gerçek ürün ve üreticiyi de bağlaması.',
      'A platform indexing architecture projects alongside building products. Unlike pure inspiration '
      'sites it also links the real products and manufacturers used in a project.', 'mimari'),
    a('https://divisare.com/', 'Divisare', ['referans', 'görsel-üretim', 'freemium'],
      'Mimariyi yalnız fotoğraf üzerinden, yavaş ve seçici sunan arşiv. Hızlı akışlardan farkı '
      'projeyi bir fotoğraf serisi gibi, dikkatle küre edip sunması.',
      'An archive presenting architecture through photography alone, slow and selective. Unlike fast '
      'feeds it curates each project like a careful photo series.', 'mimari'),
    a('https://www.arch2o.com/', 'Arch2O', ['referans', 'öğretici', 'ücretsiz'],
      'Proje haberiyle birlikte yarışma, yazılım ve öğrenme içeriği veren mimari site. Salt proje '
      'arşivinden farkı öğrenci ve genç mimara yönelik rehber içeriğe de yer vermesi.',
      'An architecture site giving competitions, software and learning content alongside project news. '
      'Unlike a pure project archive it also carries guides aimed at students and young architects.', 'mimari'),
    a('https://www.pritzkerprize.com/', 'Pritzker Prize', ['referans', 'ücretsiz'],
      'Mimarlığın en yüksek ödülü olan Pritzker’in resmî sitesi — laurealar ve gerekçeleri. Genel '
      'listelerden farkı alanın kanonunu, jüri değerlendirmesiyle yıl yıl vermesi.',
      'The official site of the Pritzker Prize, architecture’s highest honour — laureates and citations. '
      'Unlike general lists it gives the field’s canon year by year, with the jury’s reasoning.', 'mimari'),
    a('https://www.architecture.com/', 'RIBA', ['referans', 'akademik', 'freemium'],
      'Kraliyet Britanya Mimarlar Enstitüsü’nün sitesi — meslek standartları, eğitim ve kaynaklar. '
      'Yayın sitelerinden farkı mesleğin kurumsal, resmî tarafını temsil etmesi.',
      'The Royal Institute of British Architects’ site — professional standards, education and '
      'resources. Unlike publication sites it represents the institutional, official side of the '
      'profession.', 'mimari'),
    a('https://www.detail.de/', 'DETAIL', ['referans', 'akademik', 'ücretli'],
      'Yapı detayına ve inşaat çözümüne odaklanan referans dergi. İlham sitelerinden farkı “nasıl '
      'yapıldığına” — birleşim, katman, malzeme detayına — inmesi.',
      'A reference magazine focused on construction detail and building solutions. Unlike inspiration '
      'sites it goes into “how it is built” — junctions, layers and material detail.', 'mimari'),
    a('https://www.sketchup.com/', 'SketchUp', ['3b', 'cad', 'freemium', 'masaüstü'],
      'Mimari ve iç mekân için hızlı 3B modelleme aracı. Ağır CAD/BIM programlarından farkı öğrenmesi '
      'kolay olması — fikri dakikalar içinde kütleye dökmek için.',
      'A fast 3D modelling tool for architecture and interiors. Unlike heavy CAD/BIM programs it is easy '
      'to learn — for turning an idea into massing in minutes.', 'mimari'),
    a('https://www.rhino3d.com/', 'Rhinoceros 3D', ['3b', 'cad', 'ücretli', 'masaüstü'],
      'Serbest form (NURBS) modelleme aracı; Grasshopper eklentisiyle algoritmik tasarımın merkezi. '
      'Kutu modelleyicilerden farkı karmaşık eğrisel geometriyi ve parametrik kurguyu kaldırması.',
      'A free-form (NURBS) modelling tool; with the Grasshopper plugin, the hub of algorithmic design. '
      'Unlike box modellers it handles complex curved geometry and parametric setups.', 'mimari'),
    a('https://www.autodesk.com/products/revit/overview', 'Autodesk Revit', ['cad', '3b', 'ücretli', 'masaüstü'],
      'Yapı bilgi modellemesinin (BIM) endüstri standardı — model, çizim ve veri tek dosyada. Salt '
      'çizim araçlarından farkı plana attığın duvarın kesitte ve metrajda otomatik güncellenmesi.',
      'The industry standard for Building Information Modelling (BIM) — model, drawings and data in one '
      'file. Unlike pure drafting tools, a wall you place in plan updates automatically in section and '
      'the schedule.', 'mimari'),
    a('https://graphisoft.com/solutions/archicad', 'Archicad', ['cad', '3b', 'ücretli', 'masaüstü'],
      'Revit’e rakip, mimar odaklı BIM yazılımı. Revit’ten farkı arayüzünün doğrudan mimari tasarım '
      'akışına göre kurgulanmış olması — mühendislik modüllerinden çok tasarıma eğilir.',
      'An architect-focused BIM software rivalling Revit. Unlike Revit its interface is built around the '
      'architectural design flow — leaning to design more than engineering modules.', 'mimari'),
    a('https://www.enscape3d.com/', 'Enscape', ['3b', 'görsel-üretim', 'ücretli'],
      'Revit, Rhino ve SketchUp içine gömülen gerçek zamanlı görselleştirme aracı. Ayrı render '
      'programlarından farkı modeli dışa aktarmadan, tasarlarken anında foto-gerçekçi görüntü vermesi.',
      'A real-time visualisation tool embedded inside Revit, Rhino and SketchUp. Unlike separate render '
      'programs it gives a photorealistic view instantly while you design, with no export.', 'mimari'),
    a('https://ocw.mit.edu/courses/architecture/', 'MIT OCW · Mimarlık', ['müfredat', 'ücretsiz', 'akademik'],
      'MIT mimarlık bölümünün açık ders malzemesi — tasarım stüdyosundan yapı teknolojisine. Yayın '
      'sitelerinden farkı mesleği akademik müfredat olarak, ders ders vermesi.',
      'The open courseware of MIT’s architecture department — from design studio to building technology. '
      'Unlike publication sites it gives the profession as an academic curriculum, course by course.', 'mimari'),

    # ==================================================== BACKEND (yazılım mimarisi)
    a('https://martinfowler.com/architecture/', 'Martin Fowler · Architecture', ['sistem-tasarımı', 'referans', 'ücretsiz', 'backend'],
      'Yazılım mimarisi üzerine Martin Fowler’ın kanonik makale ve kalıp derlemesi. Dağınık bloglardan '
      'farkı mikroservis, event sourcing gibi kavramların en çok atıf alan tanımını vermesi.',
      'Martin Fowler’s canonical collection of essays and patterns on software architecture. Unlike '
      'scattered blogs it gives the most-cited definition of concepts like microservices and event '
      'sourcing.', 'backend'),
    a('https://github.com/simskij/awesome-software-architecture', 'Awesome Software Architecture',
      ['awesome-liste', 'github', 'sistem-tasarımı', 'backend'],
      'Yazılım mimarisini tasarlama ve belgeleme kaynaklarının listesi. Tek kitaptan farkı kalıp, '
      'örnek olay ve araçları bir arada, konu konu toplaması.',
      'A list of resources for designing and documenting software architecture. Unlike a single book it '
      'gathers patterns, case studies and tools together, topic by topic.', 'backend', AL),
    a('https://github.com/lutzh/awesome-event-driven', 'Awesome Event-Driven Architecture',
      ['awesome-liste', 'github', 'sistem-tasarımı', 'backend'],
      'Olay güdümlü mimari için kaynak, araç ve makale listesi. Genel mimari listelerinden farkı '
      'yalnız asenkron, olay temelli tasarıma odaklanması.',
      'A list of resources, tools and articles for event-driven architecture. Unlike general '
      'architecture lists it focuses only on asynchronous, event-based design.', 'backend', AL),

    # ==================================================== DONANIM
    a('https://github.com/Kiloreux/awesome-robotics', 'Awesome Robotics', ['awesome-liste', 'github', 'donanım', 'gömülü'],
      'Robotik için kütüphane, simülatör ve öğrenme kaynağı listesi. Tek platforma bağlı listelerden '
      'farkı ROS’tan kontrol teorisine kadar alanın bütününü haritalaması.',
      'A list of libraries, simulators and learning resources for robotics. Unlike single-platform lists '
      'it maps the whole field from ROS to control theory.', 'donanim', AL),
    a('https://github.com/HQarroum/awesome-iot', 'Awesome IoT', ['awesome-liste', 'github', 'donanım', 'gömülü'],
      'Nesnelerin İnterneti için donanım, protokol ve platform listesi. Genel gömülü listelerden farkı '
      'bağlantı ve bulut tarafına — MQTT, LoRa, cihaz yönetimine — ağırlık vermesi.',
      'A list of hardware, protocols and platforms for the Internet of Things. Unlike general embedded '
      'lists it weights the connectivity and cloud side — MQTT, LoRa, device management.', 'donanim', AL),
    a('https://github.com/delftopenhardware/awesome-open-hardware', 'Awesome Open Hardware',
      ['awesome-liste', 'github', 'donanım', 'açık-kaynak'],
      'Tasarımı açık lisanslı donanım projelerinin listesi. Ürün kataloglarından farkı şemasını ve '
      'PCB’sini okuyup üstüne inşa edebileceğin projelere götürmesi.',
      'A list of hardware projects with openly licensed designs. Unlike product catalogs it points to '
      'projects whose schematics and PCBs you can read and build on.', 'donanim', AL),
    a('https://github.com/protontypes/awesome-robotic-tooling', 'Awesome Robotic Tooling',
      ['awesome-liste', 'github', 'donanım'],
      'Profesyonel robotik geliştirme için ücretsiz ve açık araçların listesi. Genel robotik '
      'listelerinden farkı üretim kalitesinde araç zincirine — test, kayıt, görselleştirmeye — odaklanması.',
      'A list of free and open tools for professional robotics development. Unlike general robotics lists '
      'it focuses on a production-grade toolchain — testing, logging, visualisation.', 'donanim', AL),

    # ==================================================== KUANTUM
    a('https://github.com/desireevl/awesome-quantum-computing', 'Awesome Quantum Computing',
      ['awesome-liste', 'github', 'kuantum'],
      'Kuantum hesaplama için çerçeve, ders ve makale listesi. Dağınık akademik kaynaklardan farkı '
      'yeni başlayana giriş yolu ile araştırmacıya derinliği bir arada sunması.',
      'A list of frameworks, courses and papers for quantum computing. Unlike scattered academic sources '
      'it offers both a beginner’s entry path and depth for the researcher.', 'kuantum', AL),
    a('https://www.ibm.com/quantum/qiskit', 'Qiskit', ['kuantum', 'açık-kaynak', 'python', 'öğretici'],
      'IBM’in açık kaynak kuantum programlama çerçevesi; gerçek kuantum donanımına erişim verir. Salt '
      'simülatörlerden farkı yazdığın devreyi bulut üzerinden gerçek bir kuantum işlemcide çalıştırması.',
      'IBM’s open-source quantum programming framework, giving access to real quantum hardware. Unlike '
      'pure simulators it runs the circuit you write on a real quantum processor over the cloud.', 'kuantum'),
    a('https://quantum.country/', 'Quantum Country', ['kuantum', 'öğretici', 'ücretsiz', 'interaktif'],
      'Kuantum hesaplamayı, hatırlatmalı tekrar (spaced repetition) gömülü bir “kitap” olarak öğreten '
      'site. Klasik metinlerden farkı okuduğunu unutmamak için araya soru serpiştirmesi.',
      'A site teaching quantum computing as a “book” with spaced-repetition built in. Unlike classic '
      'texts it interleaves questions so you do not forget what you read.', 'kuantum'),

    # ==================================================== BİLİM & AKADEMİK
    a('https://arxiv.org/', 'arXiv', ['akademik', 'ücretsiz', 'referans'],
      'Fizik, matematik ve bilgisayar biliminde makalelerin erken-baskı arşivi. Dergilerden farkı '
      'araştırmayı hakem sürecini beklemeden, herkese açık ve ücretsiz yayımlaması.',
      'A preprint archive of papers in physics, mathematics and computer science. Unlike journals it '
      'publishes research openly and free, without waiting for peer review.', 'bilim'),
    a('https://www.semanticscholar.org/', 'Semantic Scholar', ['akademik', 'ücretsiz', 'veri-bilimi'],
      'Yapay zekâ destekli akademik arama motoru. Google Scholar’dan farkı makaleyi özetlemesi, etkili '
      'atıfları ayırması ve bağlantıları anlamsal olarak çıkarması.',
      'An AI-powered academic search engine. Unlike Google Scholar it summarises a paper, distinguishes '
      'influential citations and extracts links semantically.', 'bilim'),
    a('https://www.connectedpapers.com/', 'Connected Papers', ['akademik', 'interaktif', 'freemium'],
      'Bir makaleden yola çıkıp ilgili çalışmaların görsel bir grafiğini çıkaran araç. Atıf listesinden '
      'farkı bir alanın “harita”sını çizip komşu çalışmaları göstermesi.',
      'A tool that starts from one paper and builds a visual graph of related work. Unlike a citation '
      'list it draws a “map” of a field and shows neighbouring work.', 'bilim'),
    a('https://phet.colorado.edu/', 'PhET Simulations', ['interaktif', 'ücretsiz', 'öğretici'],
      'Colorado Üniversitesi’nin fizik, kimya ve matematik için etkileşimli simülasyonları. Ders '
      'anlatımından farkı kavramı parametreleri elle oynatarak deneyimletmesi.',
      'The University of Colorado’s interactive simulations for physics, chemistry and maths. Unlike a '
      'lecture it lets you experience a concept by tweaking its parameters by hand.', 'bilim'),
    a('https://openstax.org/', 'OpenStax', ['kitap', 'ücretsiz', 'akademik', 'müfredat'],
      'Üniversite ders kitaplarını ücretsiz ve açık lisansla sunan Rice Üniversitesi projesi. Ticari '
      'kitaplardan farkı bedava, hakemli ve düzenli güncellenen tam metinler vermesi.',
      'A Rice University project offering university textbooks free and openly licensed. Unlike '
      'commercial texts it gives full, peer-reviewed volumes that are free and regularly updated.', 'bilim'),
    a('https://www.nature.com/', 'Nature', ['akademik', 'referans', 'freemium'],
      'Bilimin en prestijli hakemli dergilerinden; haber ve araştırmayı bir arada verir. Erken-baskı '
      'arşivlerinden farkı katı hakem süreci — yayımlanan bulgunun ağırlığını taşıması.',
      'One of science’s most prestigious peer-reviewed journals, carrying news and research together. '
      'Unlike preprint archives its strict peer review gives published findings their weight.', 'bilim'),
