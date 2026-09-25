# -*- coding: utf-8 -*-
"""Category introductions.

A sentence or two at the head of each category: what to look for in this
area, which distinction matters. The point is to turn a list into a guide
-- the reader gets the lay of the land before the entries.
"""

INTROS = {
    'mimari': (
        'Yapı mimarisi alanı: bir yanda projeyi gördüğün yayınlar (ArchDaily, Dezeen, Divisare), bir '
        'yanda onu çizdiğin araçlar. Araçlarda ayrım nettir — SketchUp hızlı kütle içindir, Rhino '
        'serbest formu kaldırır, Revit ve Archicad ise BIM ile çizimi ve veriyi tek modelde birleştirir.',
        'The building-architecture field: on one side the publications where you see the project '
        '(ArchDaily, Dezeen, Divisare), on the other the tools you draw it with. Among the tools the '
        'split is clear — SketchUp is for fast massing, Rhino handles free form, and Revit and Archicad '
        'unite drawings and data in one BIM model.'),
    'korsan': (
        "Bu alan tek tek içerik sitelerini değil, iki şeyi toplar: nereye bakılacağını gösteren "
        "meta-merkezler (FMHY, topluluk wiki’leri) ve otomasyon araç zinciri — *arr düzenler, "
        "qBittorrent ve SABnzbd indirir. Buradaki kaynakların hukuki durumu ülkeden ülkeye değişir; "
        "indirdiğin içeriğin telif durumunu bilmek senin sorumluluğunda.",
        "This field gathers not individual content sites but two things: meta-hubs that show where to "
        "look (FMHY, community wikis) and the automation toolchain — the *arr suite organises, "
        "qBittorrent and SABnzbd download. The legal standing of these varies by country; knowing the "
        "copyright status of what you fetch is your responsibility."),
    'veri_muh': (
        'Veri mühendisliği veriyi taşımak, dönüştürmek ve güvenilir kılmakla ilgilenir — analizden önceki '
        'katman. Spark ve Flink işler, Kafka taşır, dbt dönüştürür, Airflow ve Dagster orkestra eder; '
        'ambar tarafında DuckDB ve Iceberg yeni dengeyi kurar.',
        'Data engineering is about moving, transforming and making data reliable — the layer before '
        'analysis. Spark and Flink process, Kafka carries, dbt transforms, Airflow and Dagster '
        'orchestrate; on the warehouse side DuckDB and Iceberg set the new balance.'),
    'oyun': (
        'Oyun geliştirmede iki yol ayrımı var: hazır bir motor kullanmak (Unity, Godot) ya da motorun '
        'kendisini yazmak. Çoğu kişi birincisini ister; awesome-godot ve MagicTools araçları, '
        'Game Programming Patterns ise oyuna özgü kod tasarımını verir.',
        'Game development forks two ways: using a ready engine (Unity, Godot) or writing the engine '
        'itself. Most people want the first; awesome-godot and MagicTools give the tools, while Game '
        'Programming Patterns gives the game-specific code design.'),
    'elektronik': (
        'Elektronikte sezgi lehimden önce gelir: Falstad devreyi tarayıcıda canlandırıp akımı '
        'gösterirken All About Circuits teoriyi sıralı verir, Adafruit ve SparkFun ise parçayı çalışan '
        'bir projeye bağlar.',
        'In electronics, intuition comes before the soldering iron: Falstad animates a circuit in the '
        'browser and shows the current, All About Circuits gives the theory in order, and Adafruit and '
        'SparkFun connect a part to a working project.'),
    'test': (
        'İki ayrı ihtiyaç var: üzerinde otomasyon denenecek kararlı bir hedef ve isteklere gerçekçi '
        'cevap veren bir API. Sauce Demo ile The Internet birincisi, JSONPlaceholder ile Restful-Booker '
        'ikincisi için. Kasıtlı bozuk davranışlar bilerek konmuştur — testin kırılmasını değil, tuzağı '
        'öğrenmeni sağlar.',
        'Two separate needs: a stable target to practise automation against, and an API that answers '
        'requests realistically. Sauce Demo and The Internet serve the first, JSONPlaceholder and '
        'Restful-Booker the second. The deliberate misbehaviours are intentional — they teach you the '
        'trap, not that your test is broken.'),
    'matematik': (
        'Matematikte darboğaz genelde erişim değil, sezgi: aynı konuyu formülle veren ile resimle '
        'gösteren kaynak çok farklı işler. 3Blue1Brown ve Seeing Theory görseli, Paul’s Notes ve OpenIntro '
        'sıralı dersi, math-as-code ise notasyonu koda çevirmeyi üstlenir.',
        'In mathematics the bottleneck is usually intuition, not access: a source that gives the formula '
        'and one that shows the picture do very different jobs. 3Blue1Brown and Seeing Theory bring the '
        'visual, Paul’s Notes and OpenIntro the ordered course, and math-as-code turns notation into code.'),
    'ekonomi': (
        "İktisatta asıl mesele veri ile yorum arasındaki mesafe: World Bank, IMF ve FRED ham seriyi "
        "verir, RePEc ve NBER onları neyin nasıl açıkladığını tartışan çalışmayı. Bir grafiğe bakarken "
        "önce birimi ve dönemi kontrol et — nominal mi reel mi, kişi başı mı toplam mı.",
        "In economics the real distance is between data and interpretation: World Bank, IMF and FRED "
        "give the raw series, while RePEc and NBER give the work arguing what explains them. Before "
        "reading a chart, check the unit and the period — nominal or real, per capita or total."),
    'ogrenme': (
        'Yol haritaları neyi hangi sırayla öğreneceğini, müfredatlar bütün bir programı verir. '
        'Ücretsiz olan çoğu kaynak burada üniversite dersi kalitesinde; asıl darboğaz erişim değil, '
        'bir tanesini sonuna kadar bitirebilmek.',
        'Roadmaps tell you what to learn in which order; curricula give you a whole programme. Most of '
        'the free material here is university-grade — the bottleneck is not access but finishing one of them.'),
    'pratik': (
        'İki ayrı iş var: dil akıcılığı kazanmak ve algoritma çözmek. Codewars ve Exercism birincisi, '
        'LeetCode ve Codeforces ikincisi için. Mülakata hazırlanıyorsan rastgele soru çözmek yerine '
        'konu bağımlılığına göre sıralanmış bir yol izlemek belirgin şekilde daha verimli.',
        'These are two different jobs: gaining fluency in a language, and solving algorithms. Codewars and '
        'Exercism serve the first, LeetCode and Codeforces the second. If you are preparing for interviews, '
        'following a dependency-ordered path beats grinding random problems by a clear margin.'),
    'diller': (
        'Resmî dokümantasyon referanstır, öğretici değildir — ikisini karıştırmak en yaygın hata. '
        'Yeni bir dile geçiyorsan önce “Learn X in Y Minutes” tipi bir fark listesi, sonra resmî tur, '
        'en son referans işe yarar.',
        'Official documentation is a reference, not a tutorial, and confusing the two is the most common '
        'mistake. Moving to a new language, the useful order is a differences list, then the official tour, '
        'then the reference.'),
    'web': (
        'Tarayıcı uyumluluğu her kararın arkasında duruyor; MDN’in uyumluluk tabloları bu yüzden '
        'öğreticilerden daha değerli. CSS tarafında Grid ve Flexbox’ı oyunla öğrenmek, spesifikasyon '
        'okumaktan hem daha hızlı hem daha kalıcı.',
        'Browser compatibility sits behind every decision, which is why MDN’s support tables matter more '
        'than tutorials. On the CSS side, learning Grid and Flexbox through a game is both faster and '
        'more durable than reading the spec.'),
    'backend': (
        'Çatı seçimi çoğunlukla “ne kadarı hazır gelsin” sorusudur: Django her şeyi getirir, Flask hiçbir '
        'şeyi. Sistem tasarımı kaynaklarını yalnızca mülakat için okuma — ölçekleme kararlarının '
        'gerekçelerini bilmek günlük işte de karşılığını veriyor.',
        'Choosing a framework is mostly the question of how much should arrive ready-made: Django brings '
        'everything, Flask nothing. Do not read the system design material only for interviews — knowing '
        'why scaling decisions are made pays off in daily work too.'),
    'mobil': (
        'Temel ayrım, platformun kendi bileşenlerini mi kullandığın yoksa her pikseli kendin mi çizdiğin. '
        'Flutter ikincisini yapar ve her yerde birebir aynı görünür; React Native birincisini yapar ve '
        'her platformda yerli hisseder.',
        'The core split is whether you use the platform’s own widgets or draw every pixel yourself. Flutter '
        'does the latter and looks identical everywhere; React Native does the former and feels native '
        'on each platform.'),
    'veritabani': (
        'Sorgu yazmayı öğrenmek kolay, şemayı doğru kurmak zor — sonraki bütün performans sorunları '
        'genelde ilk gündeki modelleme kararlarından çıkar. İndeksleme konusuna ayrı vakit ayır; '
        'yavaşlığın sebebi neredeyse hiçbir zaman sorgunun kendisi değildir.',
        'Learning to write queries is easy; getting the schema right is hard — later performance problems '
        'usually trace back to modelling decisions made on day one. Spend separate time on indexing: '
        'the cause of slowness is almost never the query itself.'),
    'devops': (
        'Buradaki araçların çoğu tek başına anlamlı değil, bir yığının parçası. Sıra genelde şöyle kurulur: '
        'sürüm kontrolü, kapsayıcı, dağıtım, sonra izleme. Barındırma tarafında büyük bulutlarla '
        'Hetzner sınıfı sağlayıcılar arasındaki fark birkaç kat fiyat.',
        'Most of these tools mean little alone — they are parts of a stack, usually assembled in this order: '
        'version control, containers, deployment, then monitoring. On hosting, the gap between the big '
        'clouds and Hetzner-class providers is a multiple in price.'),
    'ag': (
        'Ağ öğrenirken teori tek başına yetmiyor; Packet Tracer ya da Wireshark ile paketi gerçekten '
        'görmeden kavramlar soyut kalıyor. Sistem yöneticiliği tarafındaki kaynaklar sertifika '
        'müfredatlarına göre düzenlenmiş, bu da onları sıralı bir plana çeviriyor.',
        'Theory alone does not carry networking — the concepts stay abstract until you actually see a packet '
        'in Packet Tracer or Wireshark. The sysadmin material here is organised around certification '
        'syllabi, which turns it into an ordered plan.'),
    'guvenlik': (
        "Gizlilik araçlarını seçerken önce “kimden korunuyorum” sorusunu cevapla — tehdit modeli "
        "olmadan araç listesi işe yaramaz. Bir reklam ağından saklanmakla bir devletten saklanmak "
        "farklı araçlar ister; çoğu kişi için parola yöneticisi ve iki adımlı doğrulama VPN’den önce "
        "gelir.",
        "For privacy tools, answer “who am I protecting against” first — without a threat model a tool "
        "list is useless. Hiding from an ad network and hiding from a state call for different tools; "
        "for most people a password manager and two-factor authentication come before a VPN."),
    'veri': (
        'Yığın oldukça durulmuş durumda: veri için pandas ya da Polars, klasik modeller için scikit-learn, '
        'derin öğrenme için PyTorch. Buradaki asıl beceri model seçmek değil, veriyi temizlemek — '
        'işin çoğu orada geçiyor.',
        'The stack has largely settled: pandas or Polars for data, scikit-learn for classical models, PyTorch '
        'for deep learning. The real skill here is not picking a model but cleaning the data, which is '
        'where most of the work goes.'),
    'yz_model': (
        'Üç ayrı karar var: hangi model, nereden çalıştırılıyor, veri nereye gidiyor. Kapalı API’ler en iyi '
        'başarımı verir ama istemin sunucularına gider; açık ağırlıklı modeller kendi donanımında çalışır, '
        'karşılığında kurulum ve VRAM derdi.',
        'Three separate decisions: which model, where it runs, and where the data goes. Closed APIs give the '
        'best performance but your prompt leaves your machine; open-weight models run on your own hardware '
        'at the cost of setup and VRAM.'),
    'yz_altyapi': (
        'Bu katman hızlı değişiyor; buradaki araçların bir kısmı iki yıl içinde ya birleşecek ya kaybolacak. '
        'Kalıcı olan kavramlar: alma (retrieval), araç çağırma, bellek ve izleme. Çatı seçerken '
        'soyutlamanın kalınlığına bak — hata ayıklarken en çok orası acıtıyor.',
        'This layer moves fast, and some of these tools will merge or disappear within two years. The durable '
        'concepts are retrieval, tool calling, memory and tracing. When picking a framework, watch the '
        'thickness of the abstraction — that is what hurts most when debugging.'),
    'yz_arac': (
        'Çoğu araç aynı birkaç modelin üstüne kurulu arayüz; fark modelde değil, iş akışına ne kadar '
        'oturduğunda. Bir aracı seçerken çıktının düzenlenebilir olup olmadığına bak: '
        'kapalı bir sonuç veren araç, iyi olsa bile hattın sonunu tıkar.',
        'Most of these are interfaces over the same few models — the difference is not the model but how well '
        'it fits your workflow. When choosing, check whether the output stays editable: a tool that hands '
        'back a closed result blocks the end of your pipeline however good it is.'),
    'donanim': (
        'Gömülü tarafta belge bulmak yazılımdakinden çok daha zor; üretici veri sayfası ile topluluk '
        'tersine mühendisliği arasında gidip geliyorsun. Bir yonga seçmeden önce açık kaynak '
        'destek durumuna bakmak, sonradan haftalar kazandırıyor.',
        'Documentation is far harder to come by on the embedded side — you move between vendor datasheets '
        'and community reverse engineering. Checking a chip’s open-source support before choosing it '
        'saves weeks later.'),
    'gozluk': (
        'Alanın açık kaynak tarafı olağandışı derecede canlı; kapalı ürünlerin yanında şeması ve yazılımı '
        'yayımlanan projeler var. Karar verirken kameralı mı kamerasız mı sorusu teknikten çok sosyal: '
        'kamerasız gözlükler günlük kullanımda kabul görüyor.',
        'The open-source side of this field is unusually alive — alongside closed products there are projects '
        'publishing schematics and software. The camera-or-no-camera decision is social more than technical: '
        'cameraless glasses get accepted in daily use.'),
    'kuantum': (
        'Bugün yapabildiklerinle vaat edilenler arasında büyük bir mesafe var; yol haritalarını bu gözle oku. '
        'Simülatörle başlamak yeterli — gerçek donanımda karşılaşacağın gürültü, öğrenme aşamasında '
        'işi zorlaştırmaktan başka bir şey yapmıyor.',
        'There is a wide gap between what is possible today and what is promised — read the roadmaps with '
        'that in mind. Starting on a simulator is enough; the noise you meet on real hardware only makes '
        'learning harder.'),
    'araclar': (
        'Buradakilerin çoğu tek bir işi iyi yapan küçük araçlar. Kurulum gerektirmeyenleri yer imine almak, '
        'kurulum gerektirenleri gerçekten ihtiyaç doğunca kurmak iyi bir ayrım. '
        'Hassas veri yapıştırdığın araçların nereye yüklediğini bir kez kontrol et.',
        'Most of these are small tools that do one thing well. A good rule is to bookmark the ones needing '
        'no installation and install the rest only when the need is real. Check once where a tool uploads '
        'anything sensitive you paste into it.'),
    'referans': (
        'Referans ile öğretici farklı işler görür: biri bildiğin bir şeyi hatırlamak, diğeri bilmediğin bir '
        'şeyi öğrenmek içindir. Kopya kâğıtları ilkine, kitaplar ikincisine hizmet eder. '
        'Derlenmiş listelerde son güncelleme tarihine bak — bu alanda çürüme hızlı.',
        'References and tutorials do different jobs: one is for recalling something you know, the other for '
        'learning something you do not. Cheat sheets serve the first, books the second. On curated lists, '
        'check the last update date — decay is fast here.'),
    'bilim': (
        'Ön baskı arşivleri en güncel çalışmayı verir ama hakem sürecinden geçmemiştir; ikisini karıştırmamak '
        'gerekiyor. Türkçe akademik kaynaklar dağınık, bu yüzden DergiPark ve Harman gibi toplayıcılar '
        'tek tek kurum aramaya göre ciddi zaman kazandırıyor.',
        'Preprint archives give you the newest work but it has not been refereed, and the two should not be '
        'conflated. Turkish academic material is scattered, so harvesters like DergiPark and Harman save '
        'real time against searching institution by institution.'),
    'barindirma': (
        "Öz-barındırma bir bedel takasıdır: aylık ücret yerine bakım yükü alıyorsun. Yedeğini kim "
        "alacak, güncellemeyi kim geçecek sorusunun cevabı sensen mantıklı; değilse bulut hizmeti daha "
        "ucuza gelir. Medya sunucuları (Plex, Jellyfin) da burada. Kayıtların çoğu Docker ile tek "
        "komutta kalkıyor; asıl iş kurulumda değil sürdürmekte.",
        "Self-hosting is a trade: you swap a monthly fee for upkeep. It makes sense when the answer to "
        "\"who backs it up, who applies the updates\" is you; otherwise a hosted service works out "
        "cheaper. Media servers (Plex, Jellyfin) live here too. Most entries come up with one Docker "
        "command; the real work is keeping them running, not installing them."),
    'yz_rag': (
        'Getirim (retrieval) tarafında asıl kararlar modelde değil hattın kendisinde: belgeyi nasıl '
        'parçalıyorsun, hangi gömme modelini kullanıyorsun, sonuçları yeniden sıralıyor musun. Vektör '
        'veritabanı seçimi çoğu projede en az önemli karar; küçük ölçekte pgvector işi görüyor, ayrı bir '
        'sistem işletmenin maliyeti ancak belli bir hacimden sonra karşılığını veriyor.',
        'On the retrieval side the decisions that matter are in the pipeline rather than the model: how you '
        'chunk documents, which embedding model you pick, whether you rerank. Choosing a vector database is '
        'usually the least consequential call — pgvector carries small projects, and running a separate '
        'system only pays for itself past a certain volume.'),
    'yz_uretim': (
        'Üretken araçlarda fark artık çıktı kalitesinden çok denetimde: aynı modeli çalıştıran iki arayüzden '
        'biri sana maske, katman ve tohum verirken diğeri tek bir metin kutusu veriyor. Ticari kullanım '
        'düşünüyorsan eğitim verisinin kaynağına ve çıktı lisansına bakmak gerekiyor, bu araçlar arasında '
        'ciddi farklılaşıyor.',
        'With generative tools the difference is less about output quality than about control: two '
        'interfaces running the same model, one handing you masks, layers and seeds, the other a single '
        'text box. If commercial use is on the table, check the training data provenance and the output '
        'licence — they vary sharply here.'),
    'medya': (
        'Bu alandaki araçların çoğu tek bir işi iyi yapıyor ve zincirlenmek üzere tasarlanmış. Tarayıcıda '
        'çalışanlar dosyayı yüklemiyor, yerelde çalışanlar toplu işi kaldırıyor: bir görsel için ilki, yüz '
        'görsel için ikincisi. Açık kaynak seçenekler burada ticari olanlarla fiilen başa baş, tek istisna '
        'renk yönetimi gerektiren profesyonel iş akışları.',
        'Most tools here do one thing well and are built to be chained. The browser-based ones never upload '
        'your file; the local ones handle batches — the first for one image, the second for a hundred. Open '
        'source is genuinely level with commercial software in this area, with colour-managed professional '
        'workflows the one exception.'),
    'guv_teknik': (
        "Uygulayıcı kaynakları: sızma testi tekniği, savunma ve tespit mühendisliği, açık kaynak "
        "istihbarat, CVE ve kavram kanıtı arşivleri. Burada izin her şeydir — yalnızca sahibi olduğun "
        "ya da yazılı izin aldığın sistemlerde dene; hata ödül programlarının kapsamı bu yüzden "
        "yazılıdır.",
        "Practitioner resources: penetration-testing technique, defence and detection engineering, "
        "open-source intelligence, CVE and proof-of-concept archives. Authorisation is everything here "
        "— test only systems you own or have written permission for, which is why bug-bounty programmes "
        "publish their scope."),
    'guv_lab': (
        "Laboratuvarlar iki gruba ayrılıyor: elinden tutanlar (TryHackMe) ve tutmayanlar (Hack The "
        "Box). İkincisine hazır olmadan geçmek genelde vakit kaybı. Kasıtlı-zafiyetli uygulamaları "
        "(Juice Shop, bWAPP) kendi makinende, internete açmadan çalıştır.",
        "The labs split into those that hold your hand (TryHackMe) and those that do not (Hack The "
        "Box); moving to the second before you are ready usually wastes time. Run the deliberately "
        "vulnerable apps (Juice Shop, bWAPP) on your own machine, never exposed to the internet."),
    'guv_kariyer': (
        "Sertifikalar ikiye ayrılıyor: pratik sınavlılar (OSCP, PNPT, CPTS) ne yapabildiğini, çoktan "
        "seçmeliler (CISSP, CEH) neyi bildiğini ölçer. İş ilanlarının istediğiyle alandakilerin saygı "
        "duyduğu her zaman aynı değil; yol haritası bu farkı görmek için iyi bir başlangıç.",
        "Certifications come in two kinds: practical exams (OSCP, PNPT, CPTS) measure what you can do, "
        "multiple-choice ones (CISSP, CEH) what you know. What job ads ask for and what practitioners "
        "respect are not always the same; the roadmap is a good place to see the difference."),
    'finans': (
        "Piyasa verisi, değerleme ve kripto araçları. Bunlar teknoloji ve veri kaynakları; yatırım "
        "tavsiyesi değil. Ücretsiz katmanlar çoğunlukla gecikmeli veri verir — gerçek zamanlı görünen "
        "her fiyatın kaynağına ve saatine bak.",
        "Market data, valuation and crypto tools. These are technology and data sources, not investment "
        "advice. Free tiers usually serve delayed data — check the source and timestamp of any price "
        "that looks real-time."),
    'acik_erisim': (
        "Yasal açık erişim ve koruma: telifi düşmüş kitaplar, açık lisanslı ders kitapları, hakemli "
        "açık dergiler ve web’in kendisini saklayan arşivler. Bir makale ödeme duvarında takıldığında "
        "önce Unpaywall’a bak; çoğu çalışmanın yazarın yüklediği yasal bir kopyası vardır.",
        "Legal open access and preservation: public-domain books, openly licensed textbooks, "
        "peer-reviewed open journals and the archives that keep the web itself. When a paper sits "
        "behind a paywall, try Unpaywall first — most work has a legal copy its author uploaded."),
}
