# -*- coding: utf-8 -*-
"""Korsan & Arşiv — Igglybuff/awesome-piracy'den merkezler ve araç zinciri.

Kaynak listede 800’den fazla tek tek site vardı; hepsini listelemek dizini bir
korsan dizinine çevirirdi. Buraya iki tür kayıt alındı: (1) meta-merkezler —
FMHY ve topluluk wiki’leri, nereye bakılacağını gösteren indeksler; (2) bu
alanın büyük ölçüde yasal, açık kaynak araç zinciri — medya sunucuları, *arr
otomasyonu, torrent/Usenet istemcileri. Tek tek içerik siteleri alınmadı;
onlar merkezlerden bulunur.
"""

P = 'piracy'


def load(add):
    def a(url, name, tags, tr, en, src=P):
        add(url, name, tags, tr, en, 'korsan', src)

    # ---------------------------------------------------------- meta-merkezler
    a('https://fmhy.net/', 'FMHY', ['referans', 'ücretsiz', 'awesome-liste'],
      '“Free Media Heck Yeah” — ücretsiz medya, araç ve kaynakların en büyük indeksi. Tek tek '
      'sitelerden farkı hepsini kategori kategori, güvenlik notlarıyla toplayıp güncel tutması.',
      '“Free Media Heck Yeah” — the largest index of free media, tools and resources. Unlike individual '
      'sites it gathers them category by category, with safety notes, and keeps them current.'),
    a('https://www.reddit.com/r/Piracy/wiki/megathread/', 'r/Piracy Megathread', ['referans', 'ücretsiz'],
      'r/Piracy topluluğunun sürdürdüğü, alan alan düzenlenmiş kaynak indeksi. Rastgele aramadan farkı '
      'topluluk denetiminden geçmiş, ölü ve tuzak bağlantıları ayıklanmış olması.',
      'A resource index maintained by the r/Piracy community, organised by area. Unlike random search it '
      'is community-vetted, with dead and trap links weeded out.'),
    a('https://www.reddit.com/r/Usenet/wiki/index', 'r/Usenet Wiki', ['referans', 'ücretsiz'],
      'Usenet’e giriş, sağlayıcı ve indeksleyici seçimi için topluluk rehberi. Reklam sitelerinden farkı '
      'karşılaştırmalı, tarafsız ve deneyime dayalı olması.',
      'A community guide to getting started with Usenet and choosing providers and indexers. Unlike ad '
      'sites it is comparative, neutral and experience-based.'),
    a('https://www.reddit.com/r/trackers/wiki/gettingintoprivatetrackers/', 'Getting Into Private Trackers',
      ['referans', 'ücretsiz', 'öğretici'],
      'Özel torrent izleyicilerinin nasıl çalıştığını ve nasıl üye olunacağını anlatan topluluk rehberi. '
      'Söylentiden farkı oran, davet ve kural sistemini adım adım açması.',
      'A community guide to how private torrent trackers work and how to get in. Unlike rumour it explains '
      'the ratio, invite and rules systems step by step.'),
    a('https://github.com/Igglybuff/awesome-piracy', 'Awesome Piracy', ['awesome-liste', 'github', 'referans'],
      'Bu alandaki bağlantıların çoğunun geldiği kaynak liste; medya, oyun, kitap ve araçları kategori '
      'kategori toplar. FMHY’den farkı GitHub üzerinde, katkıya açık bir depo olması.',
      'The source list most of this field’s links come from; it gathers media, games, books and tools by '
      'category. Unlike FMHY it is a GitHub repository open to contribution.'),

    # ---------------------------------------------------------- medya sunucuları
    a('https://www.plex.tv/', 'Plex', ['self-hosted', 'medya', 'freemium'],
      'Kendi medya kütüphaneni düzenleyip her cihaza yayınlayan sunucu. Klasör paylaşımından farkı afiş, '
      'özet ve altyazıyı otomatik toplayıp Netflix benzeri bir arayüz kurması.',
      'A server that organises your own media library and streams it to any device. Unlike folder sharing '
      'it auto-fetches posters, summaries and subtitles and builds a Netflix-like interface.'),
    a('https://jellyfin.org/', 'Jellyfin', ['self-hosted', 'medya', 'açık-kaynak', 'ücretsiz'],
      'Plex’in tümüyle açık kaynak, ücretsiz karşılığı; hiçbir özellik ödeme duvarında değil. Plex’ten '
      'farkı merkezî bir hesaba bağlı olmaması — her şey senin sunucunda.',
      'A fully open-source, free counterpart to Plex; no feature behind a paywall. Unlike Plex it is not '
      'tied to a central account — everything stays on your server.'),
    a('https://kodi.tv/', 'Kodi', ['self-hosted', 'medya', 'açık-kaynak', 'ücretsiz'],
      'Yerel ve ağ medyasını tek arayüzde toplayan açık kaynak medya merkezi yazılımı. Sunucu '
      'modelinden farkı doğrudan cihazda çalışıp eklentilerle genişlemesi.',
      'Open-source media-centre software gathering local and network media in one interface. Unlike the '
      'server model it runs directly on the device and extends through add-ons.'),

    # ---------------------------------------------------------- *arr otomasyon
    a('https://sonarr.tv/', 'Sonarr', ['self-hosted', 'otomasyon', 'açık-kaynak'],
      'Dizileri izleyip yeni bölümleri indirici üzerinden otomatik alan ve düzenleyen araç. Elle '
      'takipten farkı kaliteyi, adlandırmayı ve arşivi kurala bağlaması.',
      'A tool that watches TV series and automatically fetches and organises new episodes via a '
      'downloader. Unlike manual tracking it puts quality, naming and archiving under rules.'),
    a('https://radarr.video/', 'Radarr', ['self-hosted', 'otomasyon', 'açık-kaynak'],
      'Sonarr’ın film karşılığı — istek listeni izleyip uygun sürüm çıkınca otomatik indirir. Tek tek '
      'aramaktan farkı kalite profiline göre en iyi kaynağı kendisi seçmesi.',
      'The film counterpart to Sonarr — it watches your wishlist and downloads automatically when a '
      'suitable release appears. Unlike searching one by one it picks the best source by quality profile.'),
    a('https://prowlarr.com/', 'Prowlarr', ['self-hosted', 'otomasyon', 'açık-kaynak'],
      'Torrent ve Usenet indeksleyicilerini tek yerden yönetip *arr araçlarına bağlayan köprü. Her '
      'aracı ayrı ayrı ayarlamaktan farkı indeksleyici listesini merkezîleştirmesi.',
      'A bridge that manages torrent and Usenet indexers in one place and connects them to the *arr '
      'tools. Unlike configuring each tool separately it centralises the indexer list.'),
    a('https://www.bazarr.media/', 'Bazarr', ['self-hosted', 'otomasyon', 'açık-kaynak'],
      'Sonarr/Radarr kütüphanen için altyazıları otomatik bulup indiren yardımcı. Elle altyazı '
      'aramaktan farkı dili ve kaliteyi kurala bağlayıp eksikleri sürekli tamamlaması.',
      'A companion that automatically finds and downloads subtitles for your Sonarr/Radarr library. '
      'Unlike hunting subtitles by hand it rules the language and quality and keeps filling gaps.'),
    a('https://overseerr.dev/', 'Overseerr', ['self-hosted', 'açık-kaynak', 'medya'],
      'Ev halkının film/dizi isteklerini alıp *arr araçlarına ileten istek arayüzü. Doğrudan sunucu '
      'erişiminden farkı teknik olmayan kullanıcıya düğmeyle istek yapma imkânı vermesi.',
      'A request interface that takes the household’s film/series requests and passes them to the *arr '
      'tools. Unlike direct server access it lets a non-technical user request with a button.'),
    a('https://tautulli.com/', 'Tautulli', ['self-hosted', 'açık-kaynak', 'gözlemlenebilirlik'],
      'Plex sunucundaki izlenmeleri ve kullanıcıları izleyip raporlayan araç. Plex’in kendi istatistiğinden '
      'farkı ayrıntılı geçmiş, bildirim ve grafik sunması.',
      'A tool that monitors and reports plays and users on your Plex server. Unlike Plex’s own stats it '
      'offers detailed history, notifications and charts.'),

    # ---------------------------------------------------------- istemciler
    a('https://www.qbittorrent.org/', 'qBittorrent', ['açık-kaynak', 'ücretsiz', 'masaüstü'],
      'Reklamsız, açık kaynak BitTorrent istemcisi; yerleşik arama ve akış sırası var. Kapalı '
      'istemcilerden farkı paketli yazılım ya da reklam içermemesi.',
      'An ad-free, open-source BitTorrent client with built-in search and sequential streaming. Unlike '
      'closed clients it carries no bundled software or ads.'),
    a('https://transmissionbt.com/', 'Transmission', ['açık-kaynak', 'ücretsiz', 'self-hosted'],
      'Hafif, açık kaynak BitTorrent istemcisi; sunucuda başsız (headless) çalışabilir. Masaüstü '
      'istemcilerden farkı düşük kaynak kullanımı ve uzaktan yönetime uygunluğu.',
      'A lightweight, open-source BitTorrent client that can run headless on a server. Unlike desktop '
      'clients it uses few resources and suits remote management.'),
    a('https://sabnzbd.org/', 'SABnzbd', ['self-hosted', 'açık-kaynak', 'otomasyon'],
      'Usenet indirmelerini otomatikleştiren açık kaynak istemci — doğrulama, onarım ve çıkarma dâhil. '
      'Elle indirmeden farkı NZB’yi alıp tüm işlem zincirini kendisi tamamlaması.',
      'An open-source client that automates Usenet downloads — including verification, repair and '
      'extraction. Unlike manual downloading it takes an NZB and completes the whole chain itself.'),

    # ---------------------------------------------------------- keşif & merkeziyetsiz
    a('https://ipfs.tech/', 'IPFS', ['açık-kaynak', 'ağ', 'gizlilik'],
      'İçeriği adrese değil özüne (hash) göre adresleyen merkeziyetsiz dosya sistemi. Klasik '
      'barındırmadan farkı aynı dosyanın birçok düğümden, sansüre dirençli biçimde gelmesi.',
      'A decentralised file system that addresses content by its hash, not its location. Unlike classic '
      'hosting the same file can come from many nodes, resistant to censorship.'),
