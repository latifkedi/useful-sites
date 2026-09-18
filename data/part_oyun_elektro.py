# -*- coding: utf-8 -*-
"""Oyun Geliştirme + Elektrik & Elektronik.

İki yeni ve küçük alan. Oyun kaynaklarının çoğu sindresorhus/awesome alt-
listeleri; gerçek gamedev değeri olanlar alındı. Elektronik alanı kaynakta
çok zayıftı (iki liste), bu yüzden alanı temsil eden birkaç kanonik kaynak
(All About Circuits, Falstad, Adafruit, SparkFun) eklendi.
"""


def load(add):
    def a(url, name, tags, tr, en, cat, src):
        add(url, name, tags, tr, en, cat, src)

    AL = 'awesomelist'
    K = 'kedi'

    # ======================================================= OYUN GELİŞTİRME
    a('https://www.codingame.com/', 'CodinGame', ['pratik', 'ücretsiz', 'interaktif'],
      'Programlama bulmacalarını oyun temasıyla, kodun sonucunu bir oyun sahnesinde göstererek '
      'çözdüren platform. Kuru problem setlerinden farkı çözümünü görsel olarak canlandırması.',
      'A platform that has you solve programming puzzles with a game theme, showing your code’s result '
      'in a game scene. Unlike dry problem sets it animates your solution visually.', 'oyun', K),
    a('https://unity.com/', 'Unity', ['freemium', 'masaüstü'],
      'En yaygın kullanılan çapraz platform oyun motoru; 2B/3B, mobil ve konsol. Godot’dan farkı '
      'devasa varlık mağazası ve endüstri yaygınlığı — iş ilanlarının çoğu bunu ister.',
      'The most widely used cross-platform game engine; 2D/3D, mobile and console. Unlike Godot it has a '
      'huge asset store and industry ubiquity — most job listings ask for it.', 'oyun', K),
    a('https://gameprogrammingpatterns.com/', 'Game Programming Patterns', ['kitap', 'ücretsiz', 'öğretici'],
      'Robert Nystrom’un oyun kodunda tekrar eden tasarım kalıplarını anlatan ücretsiz kitabı. Genel '
      'tasarım deseni kitaplarından farkı örneklerinin oyun döngüsü ve performansına özgü olması.',
      'Robert Nystrom’s free book on the design patterns that recur in game code. Unlike general '
      'design-pattern books its examples are specific to the game loop and performance.', 'oyun', K),
    a('https://github.com/godotengine/awesome-godot', 'Awesome Godot', ['awesome-liste', 'github', 'açık-kaynak'],
      'Açık kaynak Godot motoru için eklenti, öğretici ve örnek projelerin listesi. Resmî dokümandan '
      'farkı topluluğun ürettiği araç ve şablonları toplaması.',
      'A list of plugins, tutorials and example projects for the open-source Godot engine. Unlike the '
      'official docs it gathers the tools and templates the community produced.', 'oyun', AL),
    a('https://github.com/Calinou/awesome-gamedev', 'Awesome Game Development', ['awesome-liste', 'github', 'referans'],
      'Motorlardan varlık araçlarına oyun geliştirmenin tüm dallarını kapsayan kaynak listesi. Tek '
      'motora bağlı listelerden farkı motor-bağımsız, geniş bir başlangıç haritası olması.',
      'A resource list covering every branch of game development from engines to asset tools. Unlike '
      'engine-specific lists it is engine-agnostic — a broad starting map.', 'oyun', AL),
    a('https://github.com/michelpereira/awesome-open-source-games', 'Awesome Open Source Games',
      ['awesome-liste', 'github', 'açık-kaynak'],
      'Kaynak kodu açık, oynanabilir oyunların listesi. Oyun mağazalarından farkı kodunu okuyup nasıl '
      'yapıldığını öğrenebileceğin, üstüne inşa edebileceğin projeler olması.',
      'A list of playable games whose source is open. Unlike game stores these are projects whose code '
      'you can read to learn how they were made and build on.', 'oyun', AL),
    a('https://github.com/gbdev/awesome-gbdev', 'Awesome Game Boy Dev', ['awesome-liste', 'github', 'gömülü'],
      'Game Boy için oyun geliştirme — assembler, araç ve donanım belgeleri. Modern motor '
      'listelerinden farkı kısıtlı retro donanıma programlamaya odaklanması.',
      'Game development for the Game Boy — assemblers, tools and hardware docs. Unlike modern engine '
      'lists it focuses on programming constrained retro hardware.', 'oyun', AL),
    a('https://github.com/stevinz/awesome-game-engine-dev', 'Awesome Game Engine Dev',
      ['awesome-liste', 'github', 'referans'],
      'Oyun değil, oyun motorunun kendisini yazmak için kaynaklar — render, fizik, ECS. Motor kullanma '
      'listelerinden farkı motoru sıfırdan kurmayı hedeflemesi.',
      'Resources for writing the game engine itself, not a game — rendering, physics, ECS. Unlike '
      'engine-usage lists it aims at building an engine from scratch.', 'oyun', AL),
    a('https://github.com/notpresident35/awesome-learn-gamedev', 'Awesome Learn Gamedev',
      ['awesome-liste', 'github', 'ogrenme'],
      'Oyun yapımını öğrenmeye yönelik ders, kitap ve topluluk kaynakları. Araç listelerinden farkı '
      'sıralı bir öğrenme yolu ve sanat/ses/tasarım gibi yan alanları da kapsaması.',
      'Course, book and community resources for learning to make games. Unlike tool lists it offers an '
      'ordered path and also covers side crafts like art, audio and design.', 'oyun', AL),
    a('https://github.com/ellisonleao/magictools', 'MagicTools', ['awesome-liste', 'github', 'araclar'],
      'Oyun ve grafik geliştirme için araç ve kaynakların listesi — sprite, tile, ses, seviye editörü. '
      'Motor listelerinden farkı üretim boru hattındaki yardımcı araçlara odaklanması.',
      'A list of tools and resources for game and graphics development — sprites, tiles, audio, level '
      'editors. Unlike engine lists it focuses on the helper tools in the production pipeline.', 'oyun', AL),
    a('https://github.com/radek-sprta/awesome-game-remakes', 'Awesome Game Remakes',
      ['awesome-liste', 'github', 'açık-kaynak'],
      'Klasik oyunların aktif bakımlı, açık kaynak yeniden yapımlarının listesi. Emülatörlerden farkı '
      'oyunun motorunun sıfırdan yeniden yazılmış olması — kodu okunabilir.',
      'A list of actively maintained, open-source remakes of classic games. Unlike emulators the game’s '
      'engine has been rewritten from scratch — the code is readable.', 'oyun', AL),
    a('https://github.com/michelpereira/awesome-games-of-coding', 'Awesome Games of Coding',
      ['awesome-liste', 'github', 'pratik'],
      'Bir programlama dilini oyun yaparak öğreten oyunların listesi. Kuru alıştırmalardan farkı '
      'öğrenmeyi bir oyunun ilerleyişine bağlaması.',
      'A list of games that teach a programming language by making games. Unlike dry exercises it ties '
      'learning to a game’s progression.', 'oyun', AL),

    # ======================================================= ELEKTRİK & ELEKTRONİK
    a('https://www.allaboutcircuits.com/', 'All About Circuits', ['öğretici', 'ücretsiz', 'referans'],
      'Elektrik ve elektroniği temelden anlatan ücretsiz ders, hesaplayıcı ve forum. Dağınık '
      'videolardan farkı DC’den sayısal tasarıma sıralı, ders kitabı düzeninde ilerlemesi.',
      'Free lessons, calculators and a forum teaching electrical and electronics from the ground up. '
      'Unlike scattered videos it progresses in textbook order from DC to digital design.', 'elektronik', K),
    a('https://www.falstad.com/circuit/', 'Falstad Circuit Simulator', ['interaktif', 'ücretsiz', 'tarayıcı-içi'],
      'Devreyi tarayıcıda çizip akım ve gerilimi canlı animasyonla gösteren simülatör. Statik '
      'şemalardan farkı elektronun nasıl aktığını gerçek zamanlı görmen — sezgi kurmak için.',
      'A simulator that lets you draw a circuit in the browser and shows current and voltage as a live '
      'animation. Unlike static schematics you see how the electrons flow in real time — for intuition.',
      'elektronik', K),
    a('https://learn.adafruit.com/', 'Adafruit Learn', ['öğretici', 'ücretsiz', 'gömülü'],
      'Mikrodenetleyici, sensör ve elektronik projeleri için adım adım, resimli rehberler. Ürün '
      'sayfalarından farkı satın alınan parçayı çalışır bir projeye kadar götürmesi.',
      'Step-by-step, illustrated guides for microcontroller, sensor and electronics projects. Unlike '
      'product pages it carries the part you bought all the way to a working project.', 'elektronik', K),
    a('https://learn.sparkfun.com/', 'SparkFun Learn', ['öğretici', 'ücretsiz', 'gömülü'],
      'Elektronik temelleri ve gömülü projeler için öğretici kütüphanesi. Adafruit’e benzer; farkı '
      'lehim, güç ve iletişim protokolleri gibi temel kavramlara daha çok eğilmesi.',
      'A tutorial library for electronics basics and embedded projects. Similar to Adafruit; it leans '
      'more into foundational concepts like soldering, power and communication protocols.', 'elektronik', K),
    a('https://github.com/kitspace/awesome-electronics', 'Awesome Electronics', ['awesome-liste', 'github', 'referans'],
      'Elektronik mühendisleri ve hobiciler için araç, üretici ve topluluk listesi. Genel donanım '
      'listelerinden farkı PCB tasarımı, komponent tedariki ve simülasyona odaklanması.',
      'A list of tools, manufacturers and communities for electronics engineers and hobbyists. Unlike '
      'general hardware lists it focuses on PCB design, component sourcing and simulation.', 'elektronik', AL),
    a('https://github.com/adafruit/awesome-circuitpython', 'Awesome CircuitPython', ['awesome-liste', 'github', 'python'],
      'Mikrodenetleyicilerde Python (CircuitPython) için kütüphane ve proje listesi. Genel gömülü '
      'listelerinden farkı C yerine Python’la donanım programlamaya odaklanması.',
      'A list of libraries and projects for Python on microcontrollers (CircuitPython). Unlike general '
      'embedded lists it focuses on programming hardware in Python rather than C.', 'elektronik', AL),
