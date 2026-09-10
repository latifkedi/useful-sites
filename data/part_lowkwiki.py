# -*- coding: utf-8 -*-
"""Records surfaced by the awesome-lowkenuinely-wikis collection.

The source is a maguowei/starred dump of one person's GitHub stars, sorted by
hand into wikis, digital gardens, cybersecurity references, OSINT tools and
directories -- about 320 repositories. It is CC0, and its own README warns
that not everything linked is safe.

Most of it was left out on purpose. A dump of stars is not a directory: it
carries dead personal blogs, one-line profile repos, piracy aggregators, and
whole sections (genealogy, humanitarian, religious) outside a tech directory's
scope. What was taken is the part that survives that filter -- living projects
with a clear job, each given a description that says where it parts ways with
the neighbours already here.

Every entry was fetched before being kept: alive, in scope, and not already in
the directory. map-of-github was dropped as a duplicate of an existing record.

These carry src='lowkwiki'.
"""

S = 'lowkwiki'


def load(add):
    def a(url, name, tags, tr, en, cat):
        add(url, name, tags, tr, en, cat, S)

    # ===================================================== THE LIST ITSELF
    a('https://github.com/Te1eG0esbrr/awesome-lowkenuinely-wikis',
      'Awesome Lowkenuinely Wikis', ['github', 'awesome-liste', 'referans', 'osint'],
      'Bir kişinin GitHub yıldızlarından derlenmiş; wiki, dijital bahçe, siber güvenlik '
      'referansı, OSINT aracı ve dizin başlıkları altında elle ayrılmış ~320 depo. Diğer '
      '“awesome” listelerinden farkı kişisel ve ayıklanmamış olması: değerli projelerle ölü '
      'bloglar yan yana, README’si bile her bağlantının güvenli olmadığını uyarıyor. Ham cevher '
      'olarak iyi, ama süzmek sana kalıyor.',
      'A hand-sorted dump of one person’s GitHub stars — about 320 repositories filed under '
      'wikis, digital gardens, cybersecurity references, OSINT tools and directories. Unlike '
      'other “awesome” lists it is personal and unfiltered: living projects sit beside dead '
      'blogs, and its own README warns that not every link is safe. Good raw ore, but the '
      'sieving is left to you.',
      'referans')

    # ============================================================ CYBERSECURITY WIKIS
    a('https://hacktricks.wiki/', 'HackTricks',
      ['güvenlik', 'referans', 'öğretici', 'ücretsiz'],
      'Pentest, red team, web, bulut ve ayrıcalık yükseltme tekniklerini adım adım komutlarla '
      'veren bilgi tabanı. Kavramsal güvenlik kitaplarından farkı doğrudan çalıştırılabilir '
      'olması: her sayfa “şu porta şu komutu at, çıktıda şunu ara” diyecek kadar somut, ezber '
      'değil sahada kullanılan bir başvuru.',
      'A knowledge base giving pentest, red-team, web, cloud and privilege-escalation techniques '
      'as step-by-step commands. Unlike conceptual security books it is directly runnable: every '
      'page is concrete enough to say “throw this command at that port, look for this in the '
      'output” — a field reference, not theory.',
      'guvenlik')
    a('https://github.com/notthehiddenwiki/NTHW', 'Not The Hidden Wiki',
      ['güvenlik', 'referans', 'awesome-liste', 'ücretsiz'],
      '5000’den fazla siber güvenlik bağlantısını uzmanlık alanlarına göre toplayan açık wiki. '
      'Adının çağrıştırdığı karanlık ağ dizinlerinden farkı tamamen açık web ve meşru olması: '
      'araçlar, yayınlar ve eğitim kayıtları için düz bir başlangıç noktası, gizli servis değil.',
      'An open wiki gathering 5,000+ cybersecurity links sorted by specialism. Against the '
      'dark-web directories its name plays on, it is entirely clearnet and legitimate: a plain '
      'starting point for tools, publications and training recordings, not a hidden service.',
      'guvenlik')
    a('https://github.com/rmusser01/Infosec_Reference', 'Infosec Reference',
      ['güvenlik', 'referans', 'awesome-liste', 'github'],
      'Kırmızı ve mavi takım, DFIR, AppSec ve daha fazlasını kapsayan tek çatı altında devasa '
      'bir güvenlik başvurusu. Konu bazlı awesome listelerinden farkı bütünsel olması: her '
      'uzmanlığa ayrı liste aramak yerine tek yerde, açıklamalı ve düzenli bir referans.',
      'A vast security reference under one roof — red team, blue team, DFIR, AppSec and more. '
      'Unlike single-topic awesome lists it is holistic: instead of hunting a separate list per '
      'specialism, one annotated, organised reference in a single place.',
      'guvenlik')
    a('https://github.com/qazbnm456/awesome-web-security', 'Awesome Web Security',
      ['güvenlik', 'awesome-liste', 'github', 'frontend'],
      'Web güvenliğine odaklı, saldırı sınıflarına (XSS, SSRF, deserialization) göre bölünmüş '
      'kaynak listesi. Genel hacking listelerinden farkı dar ve derin olması: yalnız web '
      'katmanını hedefliyor, her zafiyet türü için makale, araç ve laboratuvarı bir arada '
      'topluyor.',
      'A resource list focused on web security, split by attack class (XSS, SSRF, '
      'deserialisation). Against general hacking lists it is narrow and deep: it targets the web '
      'layer alone, gathering articles, tools and labs together for each vulnerability type.',
      'guvenlik')
    a('https://github.com/Hack-with-Github/Awesome-Hacking', 'Awesome Hacking',
      ['güvenlik', 'awesome-liste', 'github', 'referans'],
      'Hacker, pentester ve araştırmacılar için awesome listelerini toplayan bir liste. Tek tek '
      'konu listelerinden farkı üst dizin olması: OSINT’ten zararlı yazılım analizine kadar onlarca '
      'alt listeye tek kapıdan giriş sağlıyor.',
      'A list that collects awesome lists for hackers, pentesters and researchers. Unlike the '
      'individual topic lists it is the index above them: one door into dozens of sub-lists from '
      'OSINT to malware analysis.',
      'guvenlik')
    a('https://github.com/UCYBERS/Awesome-Blackhat-Tools', 'Awesome Black Hat Tools',
      ['güvenlik', 'awesome-liste', 'github'],
      'Yalnızca Black Hat konferanslarında resmen sunulmuş araçları toplayan liste. Genel araç '
      'listelerinden farkı giriş engeli olması: her araç sahnede canlı gösterilmiş, yani rastgele '
      'depo değil hakem süzgecinden geçmiş, sahada denenmiş araçlar.',
      'A list of tools officially presented at Black Hat events, and only those. Against general '
      'tool lists it has a bar to entry: each was demonstrated live on stage, so these are '
      'field-tested, vetted tools rather than random repositories.',
      'guvenlik')
    a('https://github.com/gmh5225/awesome-game-security', 'Awesome Game Security',
      ['güvenlik', 'awesome-liste', 'github'],
      'Oyun güvenliğine — anti-hile, tersine mühendislik, koruma atlatma — özel kaynak listesi. '
      'Genel tersine mühendislik listelerinden farkı oyunlara odaklanması: anti-cheat sistemleri '
      've oyun korumaları gibi bu alana has konuları bir arada topluyor.',
      'A resource list specific to game security — anti-cheat, reverse engineering, protection '
      'bypasses. Unlike general reverse-engineering lists it centres on games, gathering '
      'domain-specific topics like anti-cheat systems and game protections together.',
      'guvenlik')

    # ============================================================ OSINT
    a('https://github.com/jivoi/awesome-osint', 'Awesome OSINT',
      ['osint', 'awesome-liste', 'github', 'referans'],
      'Açık kaynak istihbarat araç ve kaynaklarının kategori kategori (kişi, alan adı, sosyal '
      'medya, coğrafi) listesi. Tek amaçlı OSINT araçlarından farkı harita olması: hangi işe '
      'hangi aracın olduğunu gösteren, alanın en çok atıf alan başlangıç dizini.',
      'A category-by-category list of open-source intelligence tools and resources (people, '
      'domains, social media, geolocation). Unlike a single-purpose OSINT tool it is the map: the '
      'field’s most-cited starting index for which tool fits which job.',
      'guvenlik')
    a('https://github.com/OffcierCia/non-typical-OSINT-guide', 'Atypical OSINT Guide',
      ['osint', 'öğretici', 'github', 'ücretsiz'],
      'Sıradan araç listelerinin atladığı OSINT tekniklerini toplayan rehber — blokzincir izleme, '
      'meta veri, alışılmadık kaynaklar. Standart OSINT listelerinden farkı köşe kapmaca '
      'yöntemlere gitmesi: herkesin bildiği araçları değil, az bilinen yolları anlatıyor.',
      'A guide gathering OSINT techniques the usual tool lists skip — blockchain tracing, '
      'metadata, unconventional sources. Against standard OSINT lists it goes to the corners: it '
      'covers little-known methods rather than the tools everyone already names.',
      'guvenlik')
    a('https://github.com/wddadk/OSINT-for-countries', 'OSINT for Countries',
      ['osint', 'awesome-liste', 'github', 'referans'],
      'OSINT kaynaklarını 193 ülke ve bölgeye göre ayıran liste. Küresel OSINT listelerinden '
      'farkı coğrafi olması: belirli bir ülkenin resmi kayıtları, sicilleri ve yerel araçlarını '
      'arıyorsan doğrudan o başlığa gidiyorsun.',
      'A list that sorts OSINT resources by 193 countries and territories. Unlike global OSINT '
      'lists it is geographic: if you need a specific country’s public records, registries and '
      'local tools, you go straight to that heading.',
      'guvenlik')
    a('https://github.com/snooppr/snoop', 'Snoop',
      ['osint', 'açık-kaynak', 'github', 'cli'],
      'Bir kullanıcı adını yüzlerce sitede arayan takma ad avcısı. Sherlock gibi araçlardan farkı '
      'BDT/Rusça web’e ağırlık vermesi: batı odaklı araçların kaçırdığı bölgesel platformları da '
      'kapsıyor.',
      'A username hunter that searches one handle across hundreds of sites. Unlike tools such as '
      'Sherlock it weights the CIS/Russian-language web: it covers the regional platforms that '
      'western-focused tools miss.',
      'guvenlik')

    # ============================================================ THREAT INTEL / CVE
    a('https://github.com/trickest/cve', 'Trickest CVE',
      ['güvenlik', 'github', 'otomasyon', 'referans'],
      'Bilinen tüm CVE’leri, varsa kavram kanıtı (PoC) bağlantılarıyla birlikte otomatik toplayan '
      've güncel tutan depo. NVD gibi resmi veri tabanlarından farkı istismar odaklı olması: bir '
      'zafiyetin sömürülebilir kodu nerede diye bakıyorsan doğrudan onu gösteriyor.',
      'A repository that automatically gathers and keeps current every known CVE, with links to '
      'proof-of-concept code where it exists. Unlike official databases like the NVD it is '
      'exploit-focused: if you want to know where a vulnerability’s working code lives, it points '
      'straight to it.',
      'guvenlik')
    a('https://github.com/nomi-sec/PoC-in-GitHub', 'PoC-in-GitHub',
      ['güvenlik', 'github', 'otomasyon'],
      'CVE’lere ait kavram kanıtı depolarını GitHub’dan otomatik toplayan ve günlük güncelleyen '
      'liste. Trickest CVE’den farkı yalnız GitHub’ı taraması: her zafiyet için açıkça “bu tarihte '
      'şu depo yayınlandı” diyen, PoC’a en hızlı ulaşma yolu (README’de zararlı yazılım uyarısı var).',
      'A list that automatically harvests CVE proof-of-concept repositories from GitHub and '
      'updates daily. Against Trickest CVE it scans GitHub alone: for each vulnerability it states '
      '“this repo was published on this date” — the fastest route to a PoC (its README warns of '
      'malware).',
      'guvenlik')
    a('https://github.com/mthcht/ThreatIntel-Reports', 'ThreatIntel-Reports',
      ['güvenlik', 'github', 'referans'],
      'Binlerce tehdit istihbaratı raporundan çıkarılmış içeriği aranabilir kılan depo. '
      'Raporların kendisinden farkı içlerini taraması: bir aracın ya da APT grubunun adını '
      'giriyorsun, hangi raporlarda geçtiğini tek seferde döküyor.',
      'A repository that makes the content extracted from thousands of threat-intelligence '
      'reports searchable. Unlike the reports themselves it searches inside them: you enter a '
      'tool or APT-group name and it lists every report that mentions it at once.',
      'guvenlik')
    a('https://github.com/jacobdjwilson/awesome-annual-security-reports',
      'Awesome Annual Security Reports', ['güvenlik', 'awesome-liste', 'github', 'referans'],
      'Araştırma kuruluşları ve devlet kurumlarının yıllık siber güvenlik raporlarını tek yerde '
      'toplayan liste. Tek bir raporu okumaktan farkı satıcı bağımsız olması: pazarlama metnini '
      'ayıklayıp trendleri karşılaştırabilmen için hepsini yan yana koyuyor.',
      'A list gathering the annual cybersecurity reports of research consultancies and government '
      'agencies in one place. Unlike reading a single report it is vendor-neutral: it sets them '
      'side by side so you can strip the marketing and compare the trends.',
      'guvenlik')
    a('https://github.com/MISP/misp-warninglists', 'MISP Warning Lists',
      ['güvenlik', 'github', 'otomasyon', 'referans'],
      'Tehdit göstergelerindeki yanlış pozitifleri elemek için hazır listeler — genel DNS '
      'çözücüleri, bilinen bulut aralıkları, kamu hizmetleri. Ham gösterge akışlarından farkı '
      'gürültü filtresi olması: alarm üretmemesi gereken meşru altyapıyı işaretliyor.',
      'Ready-made lists for weeding false positives out of threat indicators — public DNS '
      'resolvers, known cloud ranges, public services. Unlike raw indicator feeds it is the noise '
      'filter: it marks the legitimate infrastructure that should not raise an alarm.',
      'guvenlik')
    a('https://tweetfeed.live/', 'TweetFeed',
      ['güvenlik', 'osint', 'api', 'ücretsiz'],
      'Infosec topluluğunun Twitter/X’te paylaştığı zararlı URL, alan adı, IP ve hash’leri '
      'toplayıp CSV/JSON/RSS/API olarak sunan canlı IOC akışı. Ticari tehdit beslemelerinden farkı '
      'kaynağının açık sosyal paylaşımlar olması ve ücretsiz olması: araştırmacı gözlemlerini '
      'gerçek zamanlı, makinece okunur hâle getiriyor.',
      'A live IOC feed that collects malicious URLs, domains, IPs and hashes shared by the infosec '
      'community on Twitter/X, served as CSV/JSON/RSS/API. Unlike commercial threat feeds its '
      'source is open social posts and it is free: it turns researcher observations into '
      'real-time, machine-readable data.',
      'guvenlik')

    # ============================================================ PRIVACY / NETWORK
    a('https://lokinet.org/', 'Lokinet',
      ['ağ', 'gizlilik', 'açık-kaynak', 'ücretsiz'],
      'IP tabanlı, merkezi olmayan bir soğan yönlendirme ağı; trafiği stake edilmiş düğümler '
      'üzerinden anonimleştiriyor. Tor’dan farkı yalnız web değil her IP protokolünü taşıması: '
      'onion yönlendirmenin üstünde tam bir kaplama ağı, tek uygulama değil.',
      'A decentralised, IP-based onion-routing network that anonymises traffic across staked '
      'nodes. Unlike Tor it carries any IP protocol, not just web: a full overlay network on top '
      'of onion routing rather than a single application.',
      'ag')
    a('https://github.com/DandelionSprout/adfilt', 'DandelionSprout Filters',
      ['gizlilik', 'github', 'ücretsiz', 'referans'],
      'uBlock Origin ve benzeri engelleyiciler için elle bakımlı reklam/izleyici filtre listeleri, '
      'İskandinav listesi dâhil. Varsayılan EasyList’ten farkı bölgesel ve niş kapsam: ana '
      'listelerin atladığı yerel siteleri ve özel senaryoları hedefliyor.',
      'Hand-maintained ad/tracker filter lists for uBlock Origin and similar blockers, including '
      'a Nordic list. Unlike the default EasyList its coverage is regional and niche: it targets '
      'the local sites and special cases the main lists skip.',
      'guvenlik')
    a('https://github.com/citizenlab/test-lists', 'Citizen Lab Test Lists',
      ['gizlilik', 'osint', 'github', 'ücretsiz'],
      'Ülke ülke sansür ölçümünde kullanılan, engellenip engellenmediği test edilecek URL '
      'listeleri. Genel alan adı listelerinden farkı amacının sansür tespiti olması: OONI gibi '
      'ölçüm projelerinin beslendiği, hangi sitelerin nerede engellendiğini haritalayan kaynak.',
      'Country-by-country URL lists used to measure censorship — the sites to test for blocking. '
      'Unlike general domain lists their purpose is censorship detection: the source that '
      'measurement projects like OONI draw on to map which sites are blocked where.',
      'guvenlik')

    # ============================================================ SELF-HOSTING
    a('https://awesome-selfhosted.net/', 'Awesome-Selfhosted',
      ['self-hosted', 'barındırma', 'awesome-liste', 'açık-kaynak'],
      'Kendi sunucunda barındırabileceğin özgür yazılım servislerinin kategorilere ayrılmış '
      'kanonik listesi. Ham GitHub listesinden farkı gezilebilir sitesi: her giriş lisans, dil ve '
      '“aktif mi” bilgisiyle filtrelenebiliyor, bulut hizmetine bağımlı kalmadan alternatif '
      'aramanın standart yeri.',
      'The canonical, categorised list of free-software services you can host on your own server. '
      'Unlike the raw GitHub list its browsable site filters every entry by licence, language and '
      'whether it is still active — the standard place to find an alternative without depending '
      'on a cloud service.',
      'barindirma')
    a('https://geek-cookbook.funkypenguin.co.nz/', 'Geek Cookbook',
      ['self-hosted', 'barındırma', 'docker', 'öğretici'],
      'Docker Swarm üzerinde yüksek erişilebilir bir “özel bulut” kurmak için uçtan uca tarifler. '
      'Awesome-Selfhosted’un liste yaklaşımından farkı adım adım kurulum vermesi: hangi yazılımı '
      'seçeceğini değil, seçtiğini üretimde nasıl ayağa kaldıracağını anlatıyor.',
      'End-to-end recipes for building a highly-available “private cloud” on Docker Swarm. Unlike '
      'Awesome-Selfhosted’s list approach it gives step-by-step deployment: not which software to '
      'pick, but how to stand up the one you picked in production.',
      'barindirma')
    a('https://selfh.st/', 'selfh.st',
      ['self-hosted', 'barındırma', 'ücretsiz'],
      'Kendinden barındırma dünyasından haftalık haber, yeni yazılım ve güncelleme derleyen '
      'bülten ve içerik sitesi. Statik listelerden farkı akış olması: yeni ne çıktı, ne '
      'güncellendi diye takip etmek için canlı, tarihli bir kaynak.',
      'A newsletter and content site rounding up weekly news, new software and updates from the '
      'self-hosting world. Unlike static lists it is a feed: a live, dated source for tracking '
      'what launched and what was updated.',
      'barindirma')
    a('https://yunohost.org/', 'YunoHost',
      ['self-hosted', 'barındırma', 'açık-kaynak', 'sunucu'],
      'Kendi sunucunu tek tıkla uygulama kuran bir işletim sistemine çeviren proje. El ile Docker '
      'kurmaktan farkı yönetimi soyutlaması: kullanıcı, alan adı ve yedeği tek panelden yönetiyorsun, '
      'katalogdaki uygulamalar tek komutla geliyor.',
      'A project that turns your own server into an operating system with one-click app installs. '
      'Unlike setting up Docker by hand it abstracts the admin: you manage users, domains and '
      'backups from one panel, and catalog apps install in a single step.',
      'barindirma')

    # ============================================================ STATIC SITES / GARDENS
    a('https://gohugo.io/', 'Hugo',
      ['web', 'frontend', 'açık-kaynak', 'dokümantasyon'],
      'Markdown içeriği statik sitelere dönüştüren, Go ile yazılmış üretici. Node tabanlı '
      'üreticilerden farkı ham hızı: binlerce sayfayı saniyeler içinde derliyor, tek ikili dosya, '
      'JS bağımlılık ağacı yok.',
      'A static-site generator written in Go that turns Markdown into websites. Unlike '
      'Node-based generators its distinction is raw speed: it builds thousands of pages in '
      'seconds, from a single binary, with no JS dependency tree.',
      'web')
    a('https://quartz.jzhao.xyz/', 'Quartz',
      ['web', 'frontend', 'açık-kaynak', 'dokümantasyon'],
      'Markdown notlarını — özellikle Obsidian kasalarını — bağlantılı bir siteye dönüştüren '
      'üretici. Genel statik üreticilerden farkı çift yönlü bağlantı ve geri-bağlantıları koruması: '
      'dijital bahçeni ağ yapısıyla birlikte yayımlıyor.',
      'A generator that turns Markdown notes — Obsidian vaults especially — into a linked site. '
      'Unlike general static generators it preserves bidirectional links and backlinks: it '
      'publishes your digital garden with its network structure intact.',
      'web')
    a('https://docusaurus.io/', 'Docusaurus',
      ['web', 'frontend', 'açık-kaynak', 'dokümantasyon'],
      'Meta’nın React tabanlı dokümantasyon sitesi üreticisi; sürümleme ve çeviri yerleşik geliyor. '
      'Genel statik üreticilerden farkı belge odaklı olması: özellikle yazılım dokümantasyonu için '
      'sürüm arşivi ve i18n gibi hazır parçalarla geliyor.',
      'Meta’s React-based documentation-site generator, with versioning and translation built in. '
      'Unlike general static generators it is docs-first: it ships ready-made pieces like version '
      'archives and i18n aimed specifically at software documentation.',
      'web')
    a('https://github.com/oleeskild/obsidian-digital-garden', 'Obsidian Digital Garden',
      ['web', 'eklenti', 'açık-kaynak', 'frontend'],
      'Obsidian notlarını doğrudan yayımlanmış bir dijital bahçeye çeviren eklenti. Quartz gibi '
      'üreticilerden farkı derleme adımı istememesi: not içinden tek düğmeyle yayınlıyorsun, '
      'ayrı bir build hattı kurmana gerek kalmıyor.',
      'An Obsidian plugin that publishes notes straight into a live digital garden. Unlike '
      'generators such as Quartz it needs no build step: you publish from inside a note with one '
      'button, with no separate build pipeline to set up.',
      'web')
    a('https://github.com/MaggieAppleton/digital-gardeners', 'Digital Gardeners',
      ['awesome-liste', 'github', 'referans'],
      'Herkese açık notlarını “bahçe” gibi işleyenler için kaynak, bağlantı ve fikir listesi. '
      'Araç odaklı listelerden farkı felsefeye ağırlık vermesi: hangi yazılımdan çok, aç­ık '
      'düşünmenin nasıl yapıldığına dair yazı ve örnekleri topluyor.',
      'A list of resources, links and ideas for people who tend their public notes like a garden. '
      'Unlike tool-focused lists it weights the philosophy: it gathers essays and examples on how '
      'to think in public rather than which software to use.',
      'referans')
    a('https://github.com/KasperZutterman/Second-Brain', 'Second-Brain',
      ['awesome-liste', 'github', 'referans'],
      'Herkese açık Zettelkasten’ler, “ikinci beyin”ler ve dijital bahçelerin derli toplu listesi. '
      'Genel not alma listelerinden farkı örnek toplaması: teoriden çok, insanların gerçekten '
      'yayımladığı bilgi kasalarını gezip görebiliyorsun.',
      'A curated list of public Zettelkastens, “second brains” and digital gardens. Unlike '
      'general note-taking lists it collects examples: rather than theory, you can browse the '
      'knowledge vaults people have actually published.',
      'referans')
    a('https://github.com/RichardLitt/meta-knowledge', 'meta-knowledge',
      ['awesome-liste', 'github', 'referans'],
      'Bilgi depoları hakkında bir liste — yani listelerin ve kişisel wiki’lerin listesi. Konu '
      'listelerinden farkı bir üst katman olması: “insanlar bilgiyi nasıl saklıyor” sorusuna '
      'örnek arıyorsan giriş noktan burası.',
      'A list about knowledge repositories — a list of lists and personal wikis. Unlike topic '
      'lists it sits one layer up: if you are looking for examples of how people store knowledge, '
      'this is the entry point.',
      'referans')

    # ============================================================ DIRECTORIES / DISCOVERY
    a('https://bukmark.club/', 'BUKMARK.CLUB',
      ['referans', 'awesome-liste', 'ücretsiz'],
      'Yalnızca bağlantı koleksiyonu barındıran siteleri listeleyen bir dizin — yer imi '
      'koleksiyonlarının dizini. Genel web dizinlerinden farkı bu şartı koşması: listelenmek için '
      'sitenin kendisi başka sitelere derli toplu bir bağlantı koleksiyonu sunmalı.',
      'A directory that lists only sites which themselves host a curated collection of links — a '
      'directory of bookmark collections. Unlike general web directories it sets that one '
      'condition: to be listed, a site must offer a tidy collection of links to other sites.',
      'referans')
    a('https://www.trackawesomelist.com/', 'Track Awesome List',
      ['referans', 'awesome-liste', 'otomasyon', 'ücretsiz'],
      '500’den fazla awesome listesini izleyip günlük eklenenleri gösteren, RSS ile takip '
      'edilebilen servis. Listeyi yıldızlamaktan farkı değişimi göstermesi: koca listeyi baştan '
      'taramadan yalnızca yeni girişleri görüyorsun.',
      'A service that tracks 500+ awesome lists and shows what was added daily, followable by RSS. '
      'Unlike starring a list it shows the change: you see only the new entries without '
      're-scanning the whole list.',
      'referans')
    a('https://github.com/AboutRSS/ALL-about-RSS', 'ALL about RSS',
      ['awesome-liste', 'github', 'referans'],
      'RSS’e dair her şeyi — okuyucular, dönüştürücüler, servisler, öğreticiler — toplayan liste. '
      'Tek bir okuyucudan farkı ekosistemin haritası olması: bir siteye feed yoksa nasıl '
      'üretileceğinden okuma akışını nasıl kuracağına kadar tüm araçları bir arada veriyor.',
      'A list gathering everything about RSS — readers, converters, services, tutorials. Unlike a '
      'single reader it is the map of the ecosystem: from generating a feed for a site that lacks '
      'one to building a reading pipeline, it holds all the tools together.',
      'referans')
    a('https://github.com/maguowei/starred', 'starred',
      ['github', 'otomasyon', 'açık-kaynak', 'cli'],
      'GitHub yıldızlarını dile göre gruplanmış awesome-liste biçiminde otomatik üreten araç. '
      'Elle liste tutmaktan farkı kendini güncellemesi: yıldızladıkça listen bir iş akışıyla '
      'tazeleniyor (bu dizindeki lowkenuinely-wikis kaynağı da bununla üretildi).',
      'A tool that automatically generates an awesome-list from your GitHub stars, grouped by '
      'language. Unlike keeping a list by hand it updates itself: as you star, a workflow '
      'refreshes the list (the lowkenuinely-wikis source in this directory was built with it).',
      'referans')
    a('https://ossinsight.io/', 'OSSInsight',
      ['github', 'veri-bilimi', 'interaktif', 'ücretsiz'],
      '10 milyardan fazla GitHub olayını gerçek zamanlı analiz eden açık kaynak istatistik '
      'platformu; depoları yıldız, commit ve katkıcı sağlığına göre karşılaştırıyor. Yıldız '
      'sayısına bakmaktan farkı derin metrik vermesi: bir projenin gerçekten canlı mı yoksa '
      'sadece popüler mi olduğunu ölçebiliyorsun.',
      'An open-source analytics platform that analyses 10B+ GitHub events in real time, comparing '
      'repositories by stars, commits and contributor health. Unlike glancing at a star count it '
      'gives deep metrics: you can measure whether a project is genuinely alive or merely popular.',
      'referans')

    # ============================================================ ARCHIVING
    a('https://github.com/WikiTeam/wikiteam', 'WikiTeam',
      ['arşivlenmiş', 'github', 'python', 'cli'],
      'MediaWiki wiki’lerini indirip arşivleyen araç takımı; 600.000’den fazla wiki korunmuş. '
      'Genel site kopyalayıcılardan farkı wiki’ye özel olması: sayfa geçmişi ve medya dâhil tam '
      'döküm alıyor, HTML kabuğunu değil.',
      'A toolset that downloads and archives MediaWiki wikis — 600,000+ preserved. Unlike general '
      'site copiers it is wiki-specific: it takes a full dump including page history and media, '
      'not just the HTML shell.',
      'referans')
    a('https://github.com/ArchiveTeam/grab-site', 'grab-site',
      ['arşivlenmiş', 'github', 'python', 'cli'],
      'WARC çıktısı üreten, tüm taramaları tek panelden izlenen arşivci web tarayıcısı. wget gibi '
      'araçlardan farkı dinamik yok sayma kuralları: tarama sürerken tuzağa düşüren desenleri '
      'anında dışlayıp büyük siteleri düzgün arşivleyebiliyorsun.',
      'An archivist’s web crawler with WARC output and a dashboard for all crawls. Unlike tools '
      'like wget it has dynamic ignore rules: you exclude trap patterns mid-crawl, so large sites '
      'archive cleanly.',
      'referans')

    # ============================================================ LEARNING
    a('https://github.com/0xsyr0/OSCP', 'OSCP Cheat Sheet',
      ['güvenlik', 'kopya-kâğıdı', 'github', 'sertifika'],
      'OSCP sınavı için sık gereken komut ve teknikleri toplayan, sürekli güncellenen kopya '
      'kâğıdı. Genel pentest notlarından farkı sınava göre budanmış olması: OSCP+ kapsamındaki '
      'AD CS istismarı gibi konulara odaklı, sınav anında hızlı bakılacak biçimde.',
      'A continually updated cheat sheet of the commands and techniques the OSCP exam most often '
      'needs. Unlike general pentest notes it is pruned to the exam: focused on topics in OSCP+ '
      'scope like AD CS abuse, laid out for quick reference during the test.',
      'guvenlik')
    a('https://github.com/Zeyad-Azima/Offensive-Resources', 'Offensive-Resources',
      ['güvenlik', 'awesome-liste', 'github', 'öğretici'],
      'Ofansif güvenliğin her dalını — altyapı, kablosuz, IoT, exploit geliştirme, bulut — '
      'laboratuvarlarla birlikte toplayan kaynak seti. Tek konulu listelerden farkı geniş ve '
      'laboratuvar odaklı olması: okumakla kalmayıp pratik yapabileceğin ortamları da işaret ediyor.',
      'A resource set covering every branch of offensive security — infrastructure, wireless, '
      'IoT, exploit development, cloud — together with labs. Unlike single-topic lists it is broad '
      'and lab-focused: it points to environments where you can practise, not just read.',
      'guvenlik')
    a('https://github.com/01-edu/public', '01 Edu Public',
      ['ogrenme', 'müfredat', 'github', 'ücretsiz'],
      '01 Edu okulunun açık ders ve proje deposu; öğretmensiz, akran değerlendirmeli eğitim '
      'modeline dayanıyor. Video kurslardan farkı proje temelli olması: bilerek muğlak bırakılmış '
      'görevlerle kendi çözümünü kurmayı öğretiyor.',
      'The open course-and-project repository of the 01 Edu school, built on a teacherless, '
      'peer-reviewed model. Unlike video courses it is project-based: with deliberately ambiguous '
      'tasks it teaches you to build your own solution.',
      'ogrenme')

    # ============================================================ HARDWARE
    a('https://github.com/jamisonderek/flipper-zero-tutorials', 'Flipper Zero Tutorials',
      ['donanım', 'gömülü', 'github', 'öğretici'],
      'Flipper Zero için uygulama, donanım eklentisi ve kullanım anlatan geniş öğretici deposu. '
      'Resmi belgelerden farkı topluluk projelerine inmesi: SAO rozetleri ve FlipBoard gibi '
      'aksesuarları da kapsayan, video destekli pratik rehberler.',
      'A large tutorial repository for the Flipper Zero covering apps, hardware add-ons and usage. '
      'Unlike the official docs it goes into community projects: practical, video-backed guides '
      'that also cover accessories like SAO badges and the FlipBoard.',
      'donanim')
    a('https://github.com/peterzieba/5Vpld', '5Vpld',
      ['donanım', 'gömülü', 'github', 'cad'],
      'Hâlâ üretilen az sayıdaki 5V programlanabilir mantık parçası (Atmel ATF150x, GAL) için '
      'betik ve araç derlemesi. Modern FPGA araç zincirlerinden farkı eski 5V lojiğe odaklanması: '
      'retro ve onarım projelerinde bu nadir parçaları programlamanın pratik yolu.',
      'A collection of scripts and tools for the few still-made 5V programmable logic parts '
      '(Atmel ATF150x, GAL). Unlike modern FPGA toolchains it focuses on legacy 5V logic: the '
      'practical way to program these rare parts in retro and repair projects.',
      'donanim')

    # ============================================================ MOBILE
    a('https://github.com/mobilenetworkltd/openapk', 'OpenAPK',
      ['mobil', 'açık-kaynak', 'github', 'awesome-liste'],
      'Android için açık kaynak uygulama ve oyunların günlük güncellenen kategorili listesi. '
      'F-Droid gibi depolardan farkı mağaza değil dizin olması: uygulamaları doğrudan kendi kaynak '
      'depolarına yönlendiriyor, kendi paket dağıtımı yok.',
      'A daily-updated, categorised list of open-source apps and games for Android. Unlike '
      'repositories such as F-Droid it is a directory, not a store: it points apps straight to '
      'their own source repositories, with no package distribution of its own.',
      'mobil')
    a('https://awesome-android-root.org/', 'Awesome Android Root',
      ['mobil', 'referans', 'öğretici', 'awesome-liste'],
      'Android root’lama için 600’den fazla uygulama, Magisk/KernelSU/APatch/LSPosed modülü ve '
      'cihaz bazlı rehber içeren bilgi tabanı. Dağınık forum başlıklarından farkı düzenli olması: '
      'Pixel, Samsung, Xiaomi gibi cihazlara özel adım adım rehberleri tek yerde topluyor.',
      'A knowledge base for rooting Android with 600+ apps, Magisk/KernelSU/APatch/LSPosed modules '
      'and device-specific guides. Unlike scattered forum threads it is organised: it gathers '
      'step-by-step guides for devices like Pixel, Samsung and Xiaomi in one place.',
      'mobil')

    # ============================================================ MEDIA / GAME DEV
    a('https://www.retroreversing.com/', 'RetroReversing',
      ['medya', 'referans', 'öğretici', 'gömülü'],
      'Retro oyunların tersine mühendisliği için kaynak, öğretici ve araç sitesi — kaynak kod '
      'sızıntıları, donanım, derleyici çözme. Genel tersine mühendislik sitelerinden farkı retro '
      'oyun donanımına odaklanması: konsol iç mimarisi ve dönem araç zincirlerine iniyor.',
      'A site of resources, tutorials and tools for reverse-engineering retro games — source '
      'leaks, hardware, decompilation. Unlike general reverse-engineering sites it centres on '
      'retro game hardware: it goes into console internals and period toolchains.',
      'medya')
    a('https://github.com/OTFCG/Awesome-Game-Analysis', 'Awesome Game Analysis',
      ['medya', 'awesome-liste', 'github', 'referans'],
      'Video oyun teknolojisinin analizine — motor içi çalışma, grafik teknikleri, dosya '
      'formatları — dair topluluk destekli kaynak koleksiyonu. Oyun yapım derslerinden farkı '
      'tersine bakması: nasıl yapılır değil, çıkmış oyunların içinde ne olduğunu çözüyor.',
      'A community-driven collection of resources on analysing video-game technology — engine '
      'internals, graphics techniques, file formats. Unlike game-making courses it looks the '
      'other way: not how to build, but working out what is inside shipped games.',
      'medya')
    a('https://github.com/killop/anything_about_game', 'anything_about_game',
      ['medya', 'awesome-liste', 'github', 'referans'],
      'Oyun geliştirmenin her yanını — grafik, motor, ses, akademik makaleler — kapsayan devasa '
      'kaynak listesi. Awesome-Game-Analysis’in analiz odağından farkı yapım tarafına bakması: '
      'oyunu çözmek değil sıfırdan üretmek için gereken her dalı topluyor.',
      'A vast resource list covering every side of game development — graphics, engines, audio, '
      'academic papers. Unlike Awesome-Game-Analysis’s analysis focus it looks at the build side: '
      'it gathers every branch you need to make a game from scratch, not to dissect one.',
      'medya')

    # ============================================================ AI / TOOLS
    a('https://github.com/Alibaba-NLP/DeepResearch', 'Tongyi DeepResearch',
      ['llm', 'agent', 'açık-kaynak', 'github'],
      'Alibaba’nın açık kaynak “derin araştırma” ajan modeli; çok adımlı web araştırmasını kendi '
      'yürütüyor. Sohbet LLM’lerinden farkı ajan olması: tek yanıt vermek yerine araç çağırıp '
      'kaynak gezerek uzun bir araştırma görevini baştan sona tamamlıyor.',
      'Alibaba’s open-source “deep research” agent model that runs multi-step web research on its '
      'own. Unlike chat LLMs it is an agent: rather than a single reply it calls tools and browses '
      'sources to carry a long research task from start to finish.',
      'yz_altyapi')
    a('https://github.com/sipyourdrink-ltd/bernstein', 'Bernstein',
      ['agent', 'guardrail', 'açık-kaynak', 'github'],
      'AI ajanları için açık kaynak yönetişim katmanı; ajanların ne yapabileceğine dair kural ve '
      'sınırları uyguluyor. Ajan çatılarından farkı denetime bakması: ajanı kurmaz, kurulmuş bir '
      'ajanın eylemlerini politikayla sınırlar ve kayda geçirir.',
      'An open-source governance layer for AI agents that enforces rules and limits on what agents '
      'may do. Unlike agent frameworks it is about control: it does not build the agent, it '
      'constrains a built agent’s actions with policy and logs them.',
      'yz_altyapi')
    a('https://qsniyg.github.io/maxurl/', 'Image Max URL',
      ['araclar', 'tarayıcı-içi', 'eklenti', 'açık-kaynak'],
      'Bir görselin ya da videonun küçültülmüş hâlinden en büyük/orijinal sürümünü bulan tarayıcı '
      'eklentisi. Sağ tık “görseli aç”tan farkı yeniden boyutlandırmayı geri alması: küçük resim '
      'URL’sinden tam çözünürlüklü kaynağı çözüyor.',
      'A browser extension that finds the largest/original version of an image or video from its '
      'shrunken form. Unlike right-click “open image” it reverses the resizing: it resolves the '
      'full-resolution source from a thumbnail URL.',
      'araclar')
    a('https://eylenburg.github.io/', 'Eylenburg Tech Website',
      ['referans', 'interaktif', 'ücretsiz'],
      'İşletim sistemleri, dosya sistemleri ve ülkelerin dijital özgürlüğü gibi konuları geniş '
      'karşılaştırma tablolarıyla veren teknik site. Ansiklopedi maddelerinden farkı yan yana '
      'tablo olması: 18 işletim sistemini ya da 17 ülkeyi tek ızgarada karşılaştırabiliyorsun.',
      'A technical site giving broad comparison tables on operating systems, file systems and '
      'countries’ digital freedom. Unlike encyclopaedia articles it is side-by-side tables: you '
      'can compare 18 operating systems or 17 countries in a single grid.',
      'referans')
