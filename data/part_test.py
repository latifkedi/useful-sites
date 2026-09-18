# -*- coding: utf-8 -*-
"""Test & Kalite — awesome-sites-to-test-on ve testin awesome listeleri.

Kaynakta 60’tan fazla neredeyse aynı “otomasyon pratiği için demo mağaza”
vardı; hepsini listelemek tekrar olurdu. Buraya kanonik pratik hedefleri,
araçları, sahte API’leri ve konu listeleri alındı — geri kalanı awesome-testing
üzerinden bulunur. Kasıtlı-zafiyetli uygulamalar Güvenlik altında.
"""

T = 'testsites'
A = 'awesomelist'


def load(add):
    def a(url, name, tags, tr, en, cat='test', src=T):
        add(url, name, tags, tr, en, cat, src)

    # ---------------------------------------------------------- araçlar
    a('https://www.postman.com/', 'Postman', ['api', 'freemium', 'otomasyon'],
      'API isteklerini oluşturup koleksiyon hâlinde saklayan ve test eden masaüstü/bulut aracı. '
      'curl’den farkı isteği kaydetme, ortam değişkeni ve otomatik test dizisi çalıştırma.',
      'A desktop/cloud tool to build, store as collections and test API requests. Unlike curl it saves '
      'requests, holds environment variables and runs automated test sequences.'),
    a('https://insomnia.rest/', 'Insomnia', ['api', 'açık-kaynak', 'otomasyon'],
      'REST, GraphQL ve gRPC istekleri için sade bir API istemcisi. Postman’den farkı daha hafif ve '
      'açık kaynak olması, git ile sürümlenebilmesi.',
      'A clean API client for REST, GraphQL and gRPC requests. Unlike Postman it is lighter and open '
      'source, and can be versioned with git.'),
    a('https://www.webpagetest.org/', 'WebPageTest', ['ücretsiz', 'referans'],
      'Bir sayfanın yükleme performansını gerçek cihaz ve konumlardan ölçen test. Lighthouse’tan farkı '
      'şelale, film şeridi ve çoklu lokasyon karşılaştırması vermesi.',
      'A test measuring a page’s load performance from real devices and locations. Unlike Lighthouse it '
      'gives a waterfall, filmstrip and multi-location comparison.'),
    a('https://www.ssllabs.com/ssltest/', 'SSL Labs Server Test', ['güvenlik', 'ücretsiz', 'referans'],
      'Bir sitenin TLS yapılandırmasını tarayıp A–F notu veren test. Tarayıcı kilidinden farkı sertifika '
      'zinciri, protokol ve şifre takımı düzeyinde ayrıntı vermesi.',
      'A test that scans a site’s TLS configuration and grades it A–F. Unlike the browser padlock it '
      'gives detail at the level of certificate chain, protocols and cipher suites.'),

    # ---------------------------------------------------------- pratik hedefleri
    a('https://www.saucedemo.com/', 'Sauce Demo', ['ücretsiz', 'otomasyon', 'öğretici'],
      'Otomasyon öğrenmek için hazır giriş bilgileriyle gelen örnek alışveriş sitesi; bazı kullanıcılar '
      'kasıtlı olarak bozuk davranır. Rastgele demolardan farkı senaryonun kararlı ve tekrarlanabilir olması.',
      'A sample shopping site with ready logins for learning automation; some users deliberately '
      'misbehave. Unlike random demos its scenarios are stable and repeatable.'),
    a('http://the-internet.herokuapp.com/', 'The Internet (Herokuapp)', ['ücretsiz', 'otomasyon', 'referans'],
      'Otomasyonu zorlayan ortak senaryoları (iframe, dosya yükleme, kayan menü) tek tek toplayan klasik '
      'alıştırma sitesi. Demo mağazalardan farkı her sayfanın tek bir zorluğu öğretmesi.',
      'A classic practice site collecting the common scenarios that challenge automation (iframes, file '
      'upload, hovering menus) one by one. Unlike demo shops each page teaches a single difficulty.'),
    a('https://demoqa.com/', 'DemoQA', ['ücretsiz', 'otomasyon'],
      'Form, pencere öğesi, etkileşim ve kitap uygulamasıyla geniş bir otomasyon alıştırma seti. Tek '
      'sayfalık sitelerden farkı bir framework’ü baştan sona denemene yetecek çeşitlilik.',
      'A broad automation practice set with forms, widgets, interactions and a bookstore app. Unlike '
      'single-page sites it has enough variety to exercise a whole framework end to end.'),
    a('http://www.uitestingplayground.com/', 'UI Test Automation Playground', ['ücretsiz', 'otomasyon', 'öğretici'],
      'Modern web’de otomasyonu tökezleten tuzakları (gecikmeli yükleme, gizli öğe, dinamik id) sergileyen '
      'site. Genel demolardan farkı doğrudan “neden testim kırılıyor” sorusuna odaklanması.',
      'A site exposing the traps that trip up automation on the modern web (delayed load, hidden elements, '
      'dynamic ids). Unlike general demos it targets exactly “why is my test flaky”.'),
    a('https://practicesoftwaretesting.com/', 'Practice Software Testing', ['ücretsiz', 'otomasyon', 'api'],
      'Hem UI hem REST API’si olan, gerçekçi bir alet dükkânı demosu; uçtan uca test için tasarlanmış. '
      'Eski demolardan farkı modern yığın (React + API + Swagger) üzerinde olması.',
      'A realistic tool-shop demo with both a UI and a REST API, designed for end-to-end testing. Unlike '
      'older demos it runs on a modern stack (React + API + Swagger).'),
    a('https://parabank.parasoft.com/parabank/index.htm', 'ParaBank', ['ücretsiz', 'api', 'otomasyon'],
      'SOAP/REST servisleriyle birlikte gelen örnek bankacılık test sitesi. Basit demolardan farkı web '
      'servisi, WSDL ve iş akışı test etmeye elverişli olması.',
      'A sample banking test site that ships with SOAP/REST services. Unlike simple demos it is suited to '
      'testing web services, WSDL and workflows.'),
    a('https://demo.applitools.com/', 'Applitools Demo', ['ücretsiz', 'otomasyon'],
      'Görsel test için tasarlanmış, ikinci bir sürümüyle karşılaştırılabilen demo. İşlevsel testten farkı '
      'ekranın nasıl göründüğündeki değişimi yakalamaya odaklanması.',
      'A demo designed for visual testing, comparable against a second version. Unlike functional testing '
      'it targets catching changes in how the screen looks.'),
    a('https://selectorshub.com/xpath-practice-page/', 'SelectorsHub · XPath Practice', ['ücretsiz', 'öğretici'],
      'Karmaşık XPath ve CSS seçicileri yazmayı denemek için özel olarak zorlaştırılmış sayfa. Genel '
      'demolardan farkı iç içe iframe ve shadow DOM gibi seçici cehennemlerini barındırması.',
      'A page deliberately hardened for practising complex XPath and CSS selectors. Unlike general demos '
      'it contains selector hells like nested iframes and shadow DOM.'),
    a('https://restful-booker.herokuapp.com/', 'Restful-Booker', ['api', 'ücretsiz', 'otomasyon'],
      'Oda rezervasyonunu taklit eden, kimlik doğrulamalı ve iyi belgelenmiş bir test API’si. Sahte '
      'API’lerden farkı yazma işlemleri ve auth içermesi — tam bir CRUD akışı denenebiliyor.',
      'A test API emulating room booking, with authentication and good docs. Unlike fake APIs it includes '
      'writes and auth — a full CRUD flow can be exercised.'),
    a('https://coffee-cart.app/', 'Coffee Cart', ['ücretsiz', 'otomasyon'],
      'Kahve siparişi üzerinden temel etkileşimleri denemek için sade bir uygulama. Büyük demolardan farkı '
      'beş dakikada kavranacak kadar küçük ama sepet/mantık testine yetecek kadar dolu.',
      'A simple app for practising basic interactions through ordering coffee. Unlike large demos it is '
      'small enough to grasp in five minutes yet full enough for cart/logic testing.'),

    # ---------------------------------------------------------- sahte / test API'leri
    a('https://jsonplaceholder.typicode.com/', 'JSONPlaceholder', ['api', 'ücretsiz', 'öğretici'],
      'İstek atınca gerçekçi sahte JSON döndüren, kurulum istemeyen test API’si. Kendi mock sunucunu '
      'kurmaktan farkı hemen hazır olması — prototip ve öğretici için standart.',
      'A zero-setup test API that returns realistic fake JSON on request. Unlike running your own mock it '
      'is instantly available — the standard for prototypes and tutorials.'),
    a('https://reqres.in/', 'Reqres', ['api', 'ücretsiz'],
      'AJAX isteklerine gerçek yanıt veren barındırılmış REST API’si; sayfalama ve gecikme simülasyonu var. '
      'JSONPlaceholder’dan farkı yanıt gecikmesi ve hata durumlarını da taklit edebilmesi.',
      'A hosted REST API that answers AJAX requests, with pagination and delay simulation. Unlike '
      'JSONPlaceholder it can also emulate response delays and error states.'),
    a('https://pokeapi.co/', 'PokéAPI', ['api', 'ücretsiz', 'öğretici'],
      'Pokémon verisi sunan, geniş ve iç içe bir REST API’si — test ve öğretici için popüler. Basit '
      'sahte API’lerden farkı derin, ilişkili veri modeliyle gerçekçi sorguları denetmesi.',
      'A large, deeply nested REST API serving Pokémon data — popular for tests and tutorials. Unlike '
      'simple fake APIs its rich, related data model lets you exercise realistic queries.'),
    a('https://rickandmortyapi.com/', 'Rick and Morty API', ['api', 'ücretsiz'],
      'Karakter, bölüm ve mekân verisi veren, hem REST hem GraphQL sunan ücretsiz API. Tek protokollü '
      'API’lerden farkı aynı veriyi iki arayüzle sunup ikisini de denetmesi.',
      'A free API serving character, episode and location data over both REST and GraphQL. Unlike '
      'single-protocol APIs it exposes the same data two ways, letting you test both.'),
    a('https://gorest.co.in/', 'GoREST', ['api', 'ücretsiz', 'otomasyon'],
      'OAuth2 kimlik doğrulamalı, yazma destekli, REST ve GraphQL sunan test API’si. Salt-okunur sahte '
      'API’lerden farkı kayıt oluşturma/güncelleme akışını gerçekten denetmesi.',
      'A test API with OAuth2 authentication and write support, over REST and GraphQL. Unlike read-only '
      'fake APIs it truly lets you exercise create/update flows.'),
    a('https://petstore.swagger.io/', 'Swagger Petstore', ['api', 'ücretsiz', 'referans'],
      'Swagger UI önyüzüyle gelen kanonik örnek API — OpenAPI öğrenmenin standart yeri. Diğer sahte '
      'API’lerden farkı arayüzün doğrudan spesifikasyondan üretilmiş olması.',
      'The canonical sample API with a Swagger UI front end — the standard place to learn OpenAPI. Unlike '
      'other fake APIs its interface is generated straight from the spec.'),
    a('https://randomuser.me/', 'randomuser.me', ['api', 'ücretsiz'],
      'İstenen sayıda sahte kullanıcı (ad, adres, foto) üreten API. Sabit fikstürlerden farkı her çağrıda '
      'çeşitli ve gerçekçi veri vermesi — form ve liste testleri için.',
      'An API generating any number of fake users (name, address, photo). Unlike fixed fixtures it returns '
      'varied, realistic data on each call — for form and list tests.'),

    # ---------------------------------------------------------- konu listeleri
    a('https://github.com/TheJambo/awesome-testing', 'Awesome Testing', ['awesome-liste', 'github', 'referans'],
      'Yazılım testinin her dalını — birim, uçtan uca, performans, sözleşme — kaynaklarıyla toplayan liste. '
      'Bu dizideki pratik sitelerin geri kalanını da buradan bulabilirsin.',
      'A list gathering every branch of software testing — unit, end-to-end, performance, contract — with '
      'resources. You can also find the rest of this field’s practice sites here.', 'test', A),
    a('https://github.com/mxschmitt/awesome-playwright', 'Awesome Playwright', ['awesome-liste', 'github', 'otomasyon'],
      'Playwright ekosistemi için araç, eklenti ve örneklerin listesi. Resmî dokümandan farkı topluluk '
      'araçlarını ve gerçek proje örneklerini bir araya getirmesi.',
      'A list of tools, plugins and examples for the Playwright ecosystem. Unlike the official docs it '
      'brings together community tooling and real project examples.', 'test', A),
    a('https://github.com/christian-bromann/awesome-selenium', 'Awesome Selenium', ['awesome-liste', 'github', 'otomasyon'],
      'Selenium tarayıcı otomasyon çatısı ve çevresindeki araçların derlemesi. Dağınık aramadan farkı '
      'dil bağlayıcıları, ızgara ve eklentileri tek yerde toplaması.',
      'A collection of the Selenium browser-automation framework and its surrounding tools. Unlike '
      'scattered search it gathers language bindings, grid and plugins in one place.', 'test', A),
    a('https://github.com/grafana/awesome-k6', 'Awesome k6', ['awesome-liste', 'github', 'otomasyon'],
      'Geliştirici odaklı yük ve performans testi aracı k6 için kaynak listesi. Genel performans '
      'listelerinden farkı tek araca ve onun betik ekosistemine odaklanması.',
      'A resource list for k6, the developer-centric load and performance testing tool. Unlike general '
      'performance lists it focuses on one tool and its scripting ecosystem.', 'test', A),
    a('https://github.com/fityanos/awesome-quality-assurance', 'Awesome QA Roadmap', ['awesome-liste', 'github', 'ogrenme'],
      'Yazılım testinde kariyere nasıl başlanacağını ve nasıl ilerleneceğini toplayan yol haritası. Araç '
      'listelerinden farkı sıralı bir öğrenme patikası çizmesi.',
      'A roadmap gathering how to start and grow a career in software testing. Unlike tool lists it draws '
      'an ordered learning path.', 'test', A),
