# -*- coding: utf-8 -*-
"""Ekonomi & Finans — awesome-economics ve komşu listelerden.

Kaynak listede ekonomiye özel kaynaklarla (RePEc, NBER, IMF) yan yana genel
araştırma araçları (Git, LaTeX, Zotero) ve tek tek iktisatçı GitHub profilleri
de vardı. Buraya yalnız ekonomiye/finansa özgü, kayda değer ve canlı olanlar
alındı; genel araçlar zaten Yazılım/Referans altında.
"""

E = 'econ'
A = 'awesomelist'


def load(add):
    def a(url, name, tags, tr, en, cat='ekonomi', src=E):
        add(url, name, tags, tr, en, cat, src)

    # ---------------------------------------------------------- yayın & araştırma
    a('https://ideas.repec.org/', 'IDEAS / RePEc', ['akademik', 'referans', 'ücretsiz'],
      'İktisat yayınlarının en büyük veritabanı — iki milyondan fazla makale, çalışma kâğıdı ve '
      'yazılım kaydı. Google Scholar’dan farkı alana özel olması: yalnız iktisat kaynaklarını '
      'indeksliyor, yazar ve kurum sıralamaları çıkarıyor.',
      'The largest database of economics publications — over two million papers, working papers and '
      'software items. Unlike Google Scholar it is field-specific: it indexes economics alone and '
      'derives author and institution rankings.'),
    a('https://repec.org/', 'RePEc', ['akademik', 'referans', 'ücretsiz'],
      'İktisat araştırmacıları için hizmet ağı: kaynakça, çalışma kâğıdı akışı, blog toplayıcı. '
      'IDEAS onun arayüzü; repec.org ise ardındaki gönüllü altyapının kendisi.',
      'A network of services for economics researchers: bibliography, working-paper feeds, blog '
      'aggregator. IDEAS is its front end; repec.org is the volunteer infrastructure behind it.'),
    a('https://www.nber.org/papers', 'NBER Working Papers', ['akademik', 'ücretsiz', 'referans'],
      'ABD Ulusal Ekonomik Araştırmalar Bürosu’nun çalışma kâğıtları — çoğu daha sonra hakemli '
      'dergilerde yayımlanır. Dergileri beklemeden alanın öncü araştırmasını burada okursun.',
      'Working papers from the US National Bureau of Economic Research — most later appear in '
      'peer-reviewed journals. You read the field’s leading research here before the journals.'),
    a('https://www.ssrn.com/index.cfm/en/econ/', 'SSRN Economics', ['akademik', 'ücretsiz'],
      'İktisat çalışma kâğıtlarının erken-baskı arşivi. NBER’den farkı kuruma bağlı olmaması: '
      'herkes yükleyebiliyor, dolayısıyla daha geniş ama daha az süzülmüş.',
      'A preprint archive of economics working papers. Unlike NBER it is not tied to one institution: '
      'anyone can upload, so it is broader but less filtered.'),

    # ---------------------------------------------------------- veri kaynakları
    a('https://data.worldbank.org/', 'World Bank Data', ['veri-bilimi', 'ücretsiz', 'referans'],
      'Uluslararası makroekonomik zaman serileri, ülke ülke. Tek tek istatistik ofislerinden farkı '
      'karşılaştırılabilir olması: yüzlerce göstergeyi ortak tanımlarla tek yerde topluyor.',
      'International macroeconomic time series, country by country. Unlike individual statistics '
      'offices it is comparable: hundreds of indicators under common definitions in one place.'),
    a('https://www.imf.org/en/Data', 'IMF Data', ['veri-bilimi', 'ücretsiz', 'referans'],
      'Uluslararası Para Fonu’nun makro verisi — ödemeler dengesi, kur, borç için standart başvuru. '
      'Dünya Bankası’na göre daha çok parasal ve mali istatistiğe eğilir.',
      'The IMF’s macro data — the standard reference for balance of payments, exchange rates and debt. '
      'It leans more to monetary and fiscal statistics than the World Bank.'),
    a('https://data.nasdaq.com/', 'Nasdaq Data Link (Quandl)', ['veri-bilimi', 'api', 'freemium'],
      'Çok sayıda kaynaktan finansal ve ekonomik veriyi tek API altında toplayan servis (eski adı '
      'Quandl). Dağınık kaynakları tek tek çekmek yerine ortak bir arayüzden alıyorsun.',
      'A service aggregating financial and economic data from many sources under one API (formerly '
      'Quandl). Instead of pulling scattered sources one by one, you get them through a common interface.'),
    a('https://fred.stlouisfed.org/', 'FRED', ['veri-bilimi', 'ücretsiz', 'referans'],
      'St. Louis Fed’in ekonomik veri tabanı — 800 binden fazla ABD ve dünya serisi, grafik ve API. '
      'Ham istatistik yayınlarından farkı gez-çiz-indir akışının tek yerde olması.',
      'The St. Louis Fed’s economic database — 800,000+ US and world series, with charting and an API. '
      'Unlike raw statistical releases, the browse-plot-download flow lives in one place.'),

    # ---------------------------------------------------------- öğrenme
    a('https://ocw.mit.edu/courses/economics/', 'MIT OCW · İktisat', ['müfredat', 'ücretsiz', 'akademik'],
      'MIT’nin açık ders malzemesinde iktisadın tüm ana dallarını kapsayan 100’den fazla ders. '
      'YouTube derlemelerinden farkı önkoşul ve okuma listesiyle gelen tam ders yapısı.',
      'Over 100 courses across every major field of economics in MIT’s open courseware. Unlike '
      'YouTube playlists these are full course structures with prerequisites and reading lists.'),
    a('https://www.khanacademy.org/economics-finance-domain', 'Khan Academy · Ekonomi',
      ['ücretsiz', 'interaktif', 'müfredat'],
      'Mikro, makro ve finansın temel konularını sıfırdan anlatan ücretsiz video + alıştırma seti. '
      'Üniversite derslerinden farkı giriş seviyesine ve sezgiye odaklanması.',
      'A free video-and-exercise set teaching the basics of micro, macro and finance from scratch. '
      'Unlike university courses it targets the introductory level and intuition.'),
    a('https://quantecon.org/', 'QuantEcon', ['açık-kaynak', 'python', 'ücretsiz'],
      'Hesaplamalı iktisat için açık kaynak dersler ve kütüphaneler (Python ve Julia). Salt teoriden '
      'farkı modelleri kodla kurup çözmeyi öğretmesi — nicel iktisadın fiili standardı.',
      'Open-source lectures and libraries for computational economics (Python and Julia). Unlike pure '
      'theory it teaches building and solving models in code — the de facto standard for quantitative '
      'economics.'),
    a('https://openstax.org/details/books/principles-economics-3e', 'OpenStax · Principles of Economics',
      ['kitap', 'ücretsiz', 'akademik'],
      'Üniversite giriş iktisadı için ücretsiz, açık lisanslı ders kitabı. Ticari kitaplardan farkı '
      'bedava ve düzenli güncellenmesi; PDF, web ve basılı sürümleri var.',
      'A free, openly licensed textbook for introductory university economics. Unlike commercial texts '
      'it is free and regularly updated, with PDF, web and print editions.'),

    # ---------------------------------------------------------- tartışma & referans
    a('https://marginalrevolution.com/', 'Marginal Revolution', ['ücretsiz', 'referans'],
      'Tyler Cowen ve Alex Tabarrok’un günlük iktisat blogu — alandaki en çok okunanlardan. Habere '
      'göre farkı iktisatçı gözüyle, kısa ve sık yorum akışı olması.',
      'Tyler Cowen and Alex Tabarrok’s daily economics blog — among the most-read in the field. '
      'Against news it offers a short, frequent stream of commentary through an economist’s lens.'),
    a('https://cepr.org/voxeu', 'VoxEU / CEPR', ['akademik', 'ücretsiz', 'referans'],
      'Araştırmacıların kendi çalışmalarını politika kitlesine anlattığı yazı akışı (CEPR). Çalışma '
      'kâğıdından farkı jargonu düşürüp bulguyu erişilebilir kılması.',
      'A stream of columns where researchers explain their own work to a policy audience (CEPR). '
      'Unlike a working paper it drops the jargon and makes the finding accessible.'),
    a('https://economics.stackexchange.com/', 'Economics Stack Exchange', ['ücretsiz', 'interaktif', 'referans'],
      'İktisat soru-cevap sitesi; kavram ve modelleri uzmanlara sorabildiğin yer. Foruma göre farkı '
      'oylama ve düzenlemeyle en iyi cevabın öne çıkması.',
      'An economics Q&A site where you can ask experts about concepts and models. Unlike a forum, '
      'voting and editing surface the best answer.'),
    a('https://www.aeaweb.org/rfe/', 'RFE · Resources for Economists', ['referans', 'ücretsiz', 'awesome-liste'],
      'Amerikan İktisat Derneği’nin sürdürdüğü, iktisatçılar için binlerce bağlantıdan oluşan rehber. '
      'Rastgele arama yerine alanın kendi kürasyonuyla düzenlenmiş bir dizin.',
      'A guide of thousands of links for economists, maintained by the American Economic Association. '
      'A directory curated by the field itself rather than random search.'),
    a('https://www.igmchicago.org/igm-economic-experts-panel/', 'IGM Experts Panel', ['akademik', 'ücretsiz'],
      'Önde gelen iktisatçıların güncel politika sorularına katılıp katılmadıklarını oyladığı panel. '
      'Tek uzman görüşünden farkı uzlaşının nerede olduğunu tek bakışta göstermesi.',
      'A panel where leading economists vote whether they agree with topical policy questions. Unlike '
      'a single expert’s view it shows at a glance where the consensus sits.'),

    # ---------------------------------------------------------- kariyer
    a('https://www.aeaweb.org/joe/', 'JOE · Job Openings for Economists', ['referans', 'ücretsiz'],
      'Amerikan İktisat Derneği’nin resmî iş ilanı panosu — akademik iktisat piyasasının merkezî yeri. '
      'Genel iş sitelerinden farkı yalnız iktisat pozisyonlarına odaklanması.',
      'The American Economic Association’s official job board — the central place for the academic '
      'economics market. Unlike general job sites it is economics positions only.'),
    a('https://econjobmarket.org/', 'EconJobMarket', ['referans', 'ücretsiz'],
      'İktisat akademik iş başvurularını tek yerden yöneten platform; başvuru ve referans mektuplarını '
      'topluyor. Dağınık e-postalar yerine standart bir başvuru akışı.',
      'A platform managing academic economics job applications in one place, collecting applications and '
      'reference letters. A standard application flow instead of scattered emails.'),

    # ---------------------------------------------------------- finans & kripto (komşu listeler)
    a('https://github.com/georgezouq/awesome-ai-in-finance', 'Awesome AI in Finance',
      ['awesome-liste', 'github', 'veri-bilimi'], 'Finans problemlerini makine öğrenmesiyle çözen '
      'araç, veri ve makalelerin listesi. Genel finans listelerinden farkı yapay zekâ kesişimine '
      'odaklanması.',
      'A list of tools, data and papers solving finance problems with machine learning. Unlike general '
      'finance lists it focuses on the AI intersection.'),
    a('https://github.com/shi-rudo/awesome-stock-trading', 'Awesome Stock Trading',
      ['awesome-liste', 'github'], 'Hisse senedi alım-satımı için kütüphane, strateji ve veri '
      'kaynaklarının derlemesi. Yatırım tavsiyesi değil; araçların bir arada listesi.',
      'A collection of libraries, strategies and data sources for stock trading. Not investment advice; '
      'a list of the tooling in one place.'),
    a('https://github.com/Zheaoli/awesome-coins', 'Awesome Coins', ['awesome-liste', 'github'],
      'Kripto para araçları ve algoritmalarının listesi — cüzdanlar, düğüm yazılımları, kütüphaneler. '
      'Fiyat sitelerinden farkı ürünü değil altındaki teknolojiyi toplaması.',
      'A list of cryptocurrency tools and algorithms — wallets, node software, libraries. Unlike price '
      'sites it collects the underlying technology, not the product.'),
