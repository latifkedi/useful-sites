# -*- coding: utf-8 -*-
"""sindresorhus/awesome'dan seçili awesome listeleri, konu kategorilerine.

Kaynakta 290'dan fazla awesome listesi vardı; hepsini tek "Referans" kovasına
yığmak yerine yaygın ve dizide olmayanlar doğal kategorilerine dağıtıldı, böylece
her alan zenginleşiyor. Niş diller (Idris, Vala, J2ME) alınmadı.
"""

AL = 'awesomelist'


def load(add):
    def a(url, name, tags, tr, en, cat):
        add(url, name, tags, tr, en, cat, AL)

    # -- diller
    a('https://github.com/uhub/awesome-cpp', 'Awesome C++', ['awesome-liste', 'github', 'c-ailesi'],
      'C++ kütüphane ve çerçevelerini konuya göre düzenleyen liste. Genel aramadan farkı bakımı yapılan, '
      'kategorilenmiş bir başlangıç haritası olması.',
      'A list organising C++ libraries and frameworks by topic. Unlike general search it is a maintained, '
      'categorised starting map.', 'diller')
    a('https://github.com/h4cc/awesome-elixir', 'Awesome Elixir', ['awesome-liste', 'github'],
      'Elixir dili ve Erlang ekosistemi için kütüphane listesi. Hex paket aramasından farkı seçilmiş ve '
      'konuya göre gruplanmış olması.',
      'A library list for the Elixir language and Erlang ecosystem. Unlike a Hex package search it is '
      'curated and grouped by topic.', 'diller')
    a('https://github.com/lauris/awesome-scala', 'Awesome Scala', ['awesome-liste', 'github'],
      'Scala kütüphane ve araçlarının konuya göre listesi. Dağınık aramadan farkı fonksiyonel ve büyük '
      'veri kütüphanelerini bir arada göstermesi.',
      'A topic-by-topic list of Scala libraries and tools. Unlike scattered search it shows functional '
      'and big-data libraries together.', 'diller')
    a('https://github.com/markets/awesome-ruby', 'Awesome Ruby', ['awesome-liste', 'github'],
      'Ruby kütüphane ve araçlarını kategori kategori toplayan liste. RubyGems aramasından farkı '
      'seçilmiş, güncel ve gruplanmış olması.',
      'A list gathering Ruby libraries and tools category by category. Unlike a RubyGems search it is '
      'curated, current and grouped.', 'diller')

    # -- web
    a('https://github.com/PatrickJS/awesome-angular', 'Awesome Angular', ['awesome-liste', 'github', 'frontend'],
      'Angular uygulama çatısı için bileşen, araç ve öğretici listesi. Resmî dokümandan farkı topluluk '
      'kütüphanelerini ve gerçek örnekleri toplaması.',
      'A list of components, tools and tutorials for the Angular application framework. Unlike the '
      'official docs it gathers community libraries and real examples.', 'web')
    a('https://github.com/TheComputerM/awesome-svelte', 'Awesome Svelte', ['awesome-liste', 'github', 'frontend'],
      'Svelte ve SvelteKit için bileşen ve araç listesi. React ağırlıklı listelerden farkı bu derleme-'
      'zamanı çatısına özgü ekosistemi göstermesi.',
      'A list of components and tools for Svelte and SvelteKit. Unlike React-heavy lists it shows the '
      'ecosystem specific to this compile-time framework.', 'web')
    a('https://github.com/fregante/Awesome-WebExtensions', 'Awesome WebExtensions', ['awesome-liste', 'github', 'eklenti'],
      'Tarayıcılar arası eklenti (WebExtension) geliştirmek için kaynak listesi. Tek tarayıcı '
      'dokümanından farkı Chrome, Firefox ve Safari’de çalışan ortak API’ye odaklanması.',
      'A resource list for building cross-browser add-ons (WebExtensions). Unlike single-browser docs it '
      'focuses on the common API that works across Chrome, Firefox and Safari.', 'web')

    # -- backend
    a('https://github.com/sindresorhus/awesome-nodejs', 'Awesome Node.js', ['awesome-liste', 'github', 'javascript'],
      'Node.js paket ve kaynaklarını konuya göre düzenleyen liste. npm aramasından farkı seçilmiş, '
      'kalitesi denetlenmiş bir başlangıç noktası olması.',
      'A list organising Node.js packages and resources by topic. Unlike an npm search it is a curated, '
      'quality-checked starting point.', 'backend')
    a('https://github.com/denolib/awesome-deno', 'Awesome Deno', ['awesome-liste', 'github', 'javascript'],
      'Node’a güvenlik ve TypeScript odaklı bir alternatif olan Deno için kaynak listesi. Node '
      'listelerinden farkı bu güvenli çalışma zamanına özgü modülleri toplaması.',
      'A resource list for Deno, a security- and TypeScript-focused alternative to Node. Unlike Node lists '
      'it gathers modules specific to this secure runtime.', 'backend')
    a('https://github.com/ziadoz/awesome-php', 'Awesome PHP', ['awesome-liste', 'github', 'php'],
      'PHP kütüphane, çerçeve ve araçlarını konuya göre toplayan liste. Packagist aramasından farkı '
      'seçilmiş ve modern PHP pratiğine göre düzenlenmiş olması.',
      'A list gathering PHP libraries, frameworks and tools by topic. Unlike a Packagist search it is '
      'curated and organised around modern PHP practice.', 'backend')

    # -- mobil
    a('https://github.com/matteocrippa/awesome-swift', 'Awesome Swift', ['awesome-liste', 'github', 'masaüstü'],
      'Apple’ın Swift dili için kütüphane ve araç listesi. Genel iOS listelerinden farkı doğrudan dile '
      've paketlerine odaklanması.',
      'A list of libraries and tools for Apple’s Swift language. Unlike general iOS lists it focuses '
      'directly on the language and its packages.', 'mobil')
    a('https://github.com/Solido/awesome-flutter', 'Awesome Flutter', ['awesome-liste', 'github'],
      'Flutter ile çapraz platform uygulama geliştirmek için paket, örnek ve öğretici listesi. Resmî '
      'katalogtan farkı topluluk paketlerini ve gerçek uygulama örneklerini bir araya getirmesi.',
      'A list of packages, samples and tutorials for building cross-platform apps with Flutter. Unlike '
      'the official catalog it brings together community packages and real app examples.', 'mobil')
    a('https://github.com/jondot/awesome-react-native', 'Awesome React Native', ['awesome-liste', 'github', 'javascript'],
      'React Native ile mobil geliştirme için bileşen ve araç listesi. Web React listelerinden farkı '
      'yerel mobil bileşenlere ve köprülere odaklanması.',
      'A list of components and tools for mobile development with React Native. Unlike web React lists it '
      'focuses on native mobile components and bridges.', 'mobil')
    a('https://github.com/JStumpp/awesome-android', 'Awesome Android', ['awesome-liste', 'github'],
      'Android geliştirme için kütüphane, araç ve öğrenme kaynağı listesi. Genel aramadan farkı '
      'mimariden UI’ye kadar kategorilere ayrılmış olması.',
      'A list of libraries, tools and learning resources for Android development. Unlike general search '
      'it is split into categories from architecture to UI.', 'mobil')

    # -- veri / kuantum
    a('https://github.com/qinwf/awesome-R', 'Awesome R', ['awesome-liste', 'github', 'veri-bilimi'],
      'İstatistik dili R için paket ve kaynak listesi. CRAN’dan farkı görev bazında (görselleştirme, '
      'makine öğrenmesi) seçilmiş paketleri öne çıkarması.',
      'A list of packages and resources for R, the statistics language. Unlike CRAN it foregrounds '
      'packages chosen by task (visualisation, machine learning).', 'veri')
    a('https://github.com/ebraminio/awesome-qsharp', 'Awesome Q#', ['awesome-liste', 'github', 'kuantum'],
      'Microsoft’un kuantum programlama dili Q# için kaynak listesi. Genel kuantum listelerinden farkı '
      'tek dile ve onun araç zincirine odaklanması.',
      'A resource list for Q#, Microsoft’s quantum programming language. Unlike general quantum lists it '
      'focuses on one language and its toolchain.', 'kuantum')

    # -- sistem
    a('https://github.com/thibmaek/awesome-raspberry-pi', 'Awesome Raspberry Pi', ['awesome-liste', 'github', 'donanım'],
      'Raspberry Pi projeleri, işletim sistemleri ve donanım eklentileri listesi. Forum başlıklarından '
      'farkı derli toplu, kategorilenmiş bir başlangıç noktası olması.',
      'A list of Raspberry Pi projects, operating systems and hardware add-ons. Unlike forum threads it '
      'is a tidy, categorised starting point.', 'donanim')
    a('https://github.com/agucova/awesome-esp', 'Awesome ESP', ['awesome-liste', 'github', 'gömülü'],
      'WiFi’li ucuz mikrodenetleyiciler ESP8266/ESP32 için kütüphane ve proje listesi. Genel gömülü '
      'listelerden farkı bu yonga ailesine ve kablosuz projelere odaklanması.',
      'A list of libraries and projects for the ESP8266/ESP32, cheap microcontrollers with WiFi. Unlike '
      'general embedded lists it focuses on this chip family and wireless projects.', 'elektronik')
    a('https://github.com/nix-community/awesome-nix', 'Awesome Nix', ['awesome-liste', 'github', 'devops'],
      'Nix paket yöneticisi ve NixOS için araç, kütüphane ve rehber listesi. Genel Linux listelerinden '
      'farkı yeniden üretilebilir, bildirimsel yapılandırmaya odaklanması.',
      'A list of tools, libraries and guides for the Nix package manager and NixOS. Unlike general Linux '
      'lists it focuses on reproducible, declarative configuration.', 'devops')
    a('https://github.com/frenck/awesome-home-assistant', 'Awesome Home Assistant', ['awesome-liste', 'github', 'self-hosted'],
      'Açık kaynak ev otomasyonu Home Assistant için eklenti, bileşen ve pano listesi. Resmî '
      'entegrasyonlardan farkı topluluk yapımı özel bileşenleri ve otomasyonları toplaması.',
      'A list of add-ons, components and dashboards for Home Assistant, the open-source home automation '
      'platform. Unlike the official integrations it gathers community-made custom components and '
      'automations.', 'barindirma')
