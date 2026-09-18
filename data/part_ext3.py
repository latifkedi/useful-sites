# -*- coding: utf-8 -*-
"""Second pass over the Best-websites-a-programmer-should-visit leftovers.

The first pass took roughly 140 of the source's 702 links and left the rest in
missing.txt. That file was easy to mistake for a backlog of the owner's own
bookmarks; it is not. Of the entries revisited here, 80 of 81 came from the
external list, and a fair number of them were worth having after all --
Missing Semester, Rust by Example, explainshell, Data Structure Visualization.

Two candidates were dropped for the reason that keeps recurring in this
directory: the domain answers, but somebody else owns it now. branition.com
serves an Indonesian gambling site and issuehub.io a Korean game-server ad.
Both return HTTP 200.

These carry src='bwapsv'.
"""

S = 'bwapsv'


def load(add):
    def a(url, name, tags, tr, en, cat):
        add(url, name, tags, tr, en, cat, S)

    # ============================================================ LEARNING
    a('https://missing.csail.mit.edu/', 'The Missing Semester',
      ['müfredat', 'ücretsiz', 'cli'],
      'MIT’nin müfredatta yeri olmayan konuları topladığı ders: kabuk, betik yazımı, düzenleyici, '
      'sürüm denetimi, hata ayıklama. Programlama derslerinden farkı dili değil dilin etrafındaki '
      'aletleri öğretmesi — mezun olup da terminalde kaybolanların açığını kapatıyor.',
      'MIT’s course for the subjects no syllabus covers: the shell, scripting, editors, version '
      'control, debugging. Unlike a programming course it teaches the tools around the language '
      'rather than the language — the gap that leaves graduates lost in a terminal.',
      'ogrenme')
    a('https://see.stanford.edu/Course/CS106A', 'Stanford CS106A',
      ['müfredat', 'ücretsiz', 'akademik'],
      'Stanford’ın programlamaya giriş dersinin tamamı: video, ödev ve sınavlarla. Çevrimiçi kurs '
      'platformlarından farkı gerçek bir üniversite dersinin kayıtları olması — hiçbir şey '
      'kısaltılmamış, ödevler de otomatik değerlendirilen alıştırmalar değil.',
      'The whole of Stanford’s introduction to programming — lectures, assignments and exams. '
      'Unlike an online course platform these are the recordings of an actual university course: '
      'nothing is abridged, and the assignments are not auto-graded exercises.',
      'ogrenme')
    a('https://www.khanacademy.org/computing/computer-science', 'Khan Academy · Computer Science',
      ['müfredat', 'ücretsiz', 'interaktif'],
      'Algoritma, kriptografi ve bilgi teorisi konularını etkileşimli anlatımlarla veren ücretsiz '
      'müfredat. Üniversite derslerinden farkı ön koşul istememesi ve her kavramı tarayıcıda '
      'oynanabilir bir örnekle açması.',
      'A free curriculum covering algorithms, cryptography and information theory through '
      'interactive lessons. Against a university course it assumes no prerequisites and opens each '
      'concept with something playable in the browser.',
      'ogrenme')
    a('https://course.elementsofai.com/', 'Elements of AI', ['müfredat', 'ücretsiz', 'llm'],
      'Helsinki Üniversitesi’nin yapay zekaya matematik gerektirmeyen girişi; Türkçe dahil çok '
      'dilde. Teknik kurslardan farkı hedef kitlesi: model eğitmeyi değil, yapay zekanın ne yapıp '
      'ne yapamadığını anlamak isteyenler için.',
      'The University of Helsinki’s introduction to AI, requiring no mathematics and available in '
      'many languages including Turkish. Its audience is the difference: it is for people who want '
      'to understand what AI can and cannot do, not to train models.',
      'ogrenme')
    a('https://opendatastructures.org/', 'Open Data Structures',
      ['kitap', 'algoritma', 'ücretsiz'],
      'Veri yapılarını Java, C++, Python ve sözde kod olarak paralel anlatan açık ders kitabı. '
      'Diğer kitaplardan farkı her yapının aynı anda birden çok dilde verilmesi — kendi dilinde '
      'okuyup başka dile geçiş kolaylaşıyor.',
      'An open textbook presenting data structures in Java, C++, Python and pseudocode side by '
      'side. Unlike other books each structure appears in several languages at once, which makes '
      'reading in your own and translating to another straightforward.',
      'ogrenme')
    a('https://github.com/EbookFoundation/free-programming-books', 'Free Programming Books',
      ['awesome-liste', 'kitap', 'github', 'ücretsiz'],
      'Yüzlerce dilde ücretsiz programlama kitabı, kurs ve etkileşimli eğitim derlemesi; GitHub’ın '
      'en çok yıldızlanan depolarından. Benzer listelerden farkı ölçeği ve aktif bakımı — dil '
      'bazında ayrılmış, Türkçe bölümü de var.',
      'A compilation of free programming books, courses and interactive tutorials in hundreds of '
      'languages, and one of GitHub’s most-starred repositories. Against similar lists it wins on '
      'scale and active maintenance, and it is split by language — Turkish included.',
      'referans')
    a('https://programmingbooks.dev/', 'Programming Books',
      ['kitap', 'referans', 'ücretsiz'],
      'Yazılım zanaatı üzerine okuma listesi; her kitap için neden okunması gerektiği yazılı. '
      'Ücretsiz kitap derlemelerinden farkı seçici olması — nicelik değil sıra öneriyor.',
      'A reading list on software craftsmanship with a reason attached to each book. Unlike the '
      'free-book compilations it is selective: it proposes an order rather than a quantity.',
      'referans')

    # ============================================================ PRACTICE & INTERVIEW
    a('https://neetcode.io/', 'NeetCode', ['mülakat', 'algoritma', 'freemium'],
      'LeetCode sorularını konuya göre gruplayıp çözüm videolarıyla veren yol haritası. Ham soru '
      'listelerinden farkı sıralama: hangi 150 soruyu hangi sırayla çözersen kalıpları '
      'öğreneceğini söylüyor — rastgele çözmenin en büyük eksiği buydu.',
      'A roadmap that groups LeetCode problems by topic and pairs each with a solution video. '
      'Against a raw problem list the difference is ordering: which 150 problems, in which '
      'sequence, teach the patterns — the thing random grinding never gives you.',
      'pratik')
    a('https://www.techinterviewhandbook.org/', 'Tech Interview Handbook',
      ['mülakat', 'ücretsiz', 'referans'],
      'Teknik mülakatın tamamını kapsayan açık kaynak rehber: algoritma hazırlığı, sistem tasarımı, '
      'davranışsal sorular, özgeçmiş ve maaş pazarlığı. Soru bankalarından farkı sürecin '
      'algoritma dışı yarısını da ele alması.',
      'An open-source guide covering the whole technical interview: algorithm preparation, system '
      'design, behavioural questions, résumé and salary negotiation. Unlike a problem bank it '
      'covers the half of the process that is not algorithms.',
      'pratik')
    a('https://www.pramp.com/', 'Pramp', ['mülakat', 'ücretsiz', 'interaktif'],
      'Eşleştirilmiş canlı mock mülakat: bir tur sen soruyorsun, bir tur karşı taraf. Tek başına '
      'soru çözmekten farkı basınç altında sesli düşünmeyi çalıştırması — mülakatta asıl '
      'değerlendirilen de bu.',
      'Paired live mock interviews: one round you ask, the next round they do. Against solving '
      'problems alone it exercises thinking aloud under pressure, which is what interviews '
      'actually assess.',
      'pratik')
    a('https://www.codility.com/', 'Codility', ['mülakat', 'ücretli', 'algoritma'],
      'Şirketlerin teknik eleme için kullandığı değerlendirme platformu; adaylar için açık '
      'alıştırma bölümü var. Diğer soru sitelerinden farkı gerçek eleme sorularının biçimini '
      'birebir taşıması — sınavdan önce sınav ortamını görüyorsun.',
      'The assessment platform companies use for technical screening, with a practice section open '
      'to candidates. Its difference from other problem sites is that it mirrors the format of real '
      'screening tests — you see the exam environment before the exam.',
      'pratik')
    a('https://app.codesignal.com/', 'CodeSignal', ['mülakat', 'freemium', 'algoritma'],
      'Beceri değerlendirmesi ve mülakat platformu; standartlaştırılmış bir puan üretiyor ve bu '
      'puanı birden çok şirkete gönderebiliyorsun. Her şirkete ayrı sınav girmekten farkı bu tek '
      'seferlik değerlendirme.',
      'A skills assessment and interview platform that produces a standardised score you can send '
      'to several companies. The single assessment is the difference from sitting a separate test '
      'for every employer.',
      'pratik')
    a('https://cses.fi/book.html', 'Competitive Programmer’s Handbook',
      ['kitap', 'algoritma', 'ücretsiz'],
      'Yarışmacı programlama için ücretsiz el kitabı; temel algoritmalardan ileri tekniklere. '
      'Akademik algoritma kitaplarından farkı yarışma odaklı olması — ispat değil, uygulanabilir '
      'şablon veriyor.',
      'A free handbook for competitive programming, from basic algorithms to advanced techniques. '
      'Against academic algorithm books it is contest-oriented: it hands you an implementable '
      'template rather than a proof.',
      'pratik')
    a('https://www.topcoder.com/community/competitive-programming/tutorials',
      'TopCoder Tutorials', ['algoritma', 'ücretsiz', 'referans'],
      'Yarışmacı programlamanın klasik öğreticileri; birçoğu 2000’lerin başından ama konular '
      'eskimiyor. Yeni kaynaklardan farkı derinliği — tek bir tekniği baştan sona işleyen uzun '
      'metinler.',
      'The classic competitive programming tutorials, many from the early 2000s, on subjects that '
      'do not age. Against newer material the difference is depth: long pieces that work a single '
      'technique from start to finish.',
      'pratik')
    a('https://www.techiedelight.com/', 'Techie Delight',
      ['algoritma', 'mülakat', 'ücretsiz'],
      'Veri yapısı ve algoritma sorularını konuya göre gruplayıp C++, Java ve Python çözümleriyle '
      'veren arşiv. LeetCode’dan farkı çözümün açıklamasıyla birlikte gelmesi — çözmeden önce '
      'okumak için de uygun.',
      'An archive of data structure and algorithm problems grouped by topic, with C++, Java and '
      'Python solutions. Against LeetCode the solution arrives with its explanation, which makes '
      'it readable before you attempt the problem.',
      'pratik')
    a('https://learnersbucket.com/', 'Learnersbucket',
      ['javascript', 'mülakat', 'ücretsiz'],
      'JavaScript mülakat sorularına odaklanan alıştırma arşivi: polyfill yazma, olay döngüsü, '
      'kapanış. Genel algoritma sitelerinden farkı dile özgü olması — "bind’i kendin yaz" tipi '
      'sorular başka yerde bulunmuyor.',
      'A practice archive focused on JavaScript interview questions: writing polyfills, the event '
      'loop, closures. Unlike general algorithm sites it is language-specific — "implement bind '
      'yourself" is not a question you find elsewhere.',
      'pratik')

    # ============================================================ LANGUAGES
    a('https://doc.rust-lang.org/book/title-page.html', 'The Rust Book',
      ['rust', 'kitap', 'dokümantasyon', 'ücretsiz'],
      'Rust’ın resmî kitabı; sahiplik ve ödünç alma gibi dile özgü kavramları sıfırdan kuruyor. '
      'Diğer dil kitaplarından farkı derleyicinin hata mesajlarını öğretinin parçası yapması — '
      'Rust’ta derleyiciyle tartışmayı öğrenmek dilin yarısı.',
      'Rust’s official book, building up ownership and borrowing from nothing. Unlike other '
      'language books it makes the compiler’s error messages part of the teaching — in Rust, '
      'learning to argue with the compiler is half the language.',
      'diller')
    a('https://doc.rust-lang.org/rust-by-example/', 'Rust by Example',
      ['rust', 'öğretici', 'ücretsiz', 'interaktif'],
      'Rust’ı çalıştırılabilir örneklerle anlatan resmî kaynak; her örnek tarayıcıda düzenlenip '
      'derlenebiliyor. Kitaptan farkı okumak yerine denemek üzere kurulmuş olması — ikisi birlikte '
      'kullanılmak için tasarlanmış.',
      'The official companion teaching Rust through runnable examples, each editable and '
      'compilable in the browser. Against the book it is built for trying rather than reading — '
      'the two are designed to be used together.',
      'diller')
    a('https://rust-lang-nursery.github.io/rust-cookbook/', 'Rust Cookbook',
      ['rust', 'referans', 'ücretsiz'],
      '"Dosyayı satır satır oku", "HTTP isteği at" gibi gündelik işlerin Rust karşılıklarını veren '
      'tarif kitabı. Kitap ve örneklerden farkı görev odaklı olması — dili öğrenmek için değil, '
      'bir işi bitirmek için açılıyor.',
      'A cookbook of everyday tasks in Rust — read a file line by line, make an HTTP request. '
      'Against the book and the examples it is task-oriented: you open it to finish something, not '
      'to learn the language.',
      'diller')
    a('https://docs.oracle.com/javase/tutorial/', 'The Java Tutorials',
      ['dokümantasyon', 'öğretici', 'ücretsiz'],
      'Oracle’ın resmî Java öğreticisi; dil temellerinden koleksiyonlara ve eşzamanlılığa. '
      'Üçüncü parti kurslardan farkı standart kütüphanenin niyetini birinci ağızdan anlatması — '
      'karşılığında üslubu kuru ve bazı bölümleri eski sürümlerde kalmış.',
      'Oracle’s official Java tutorial, from language basics through collections and concurrency. '
      'Against third-party courses it explains the standard library’s intent first-hand; the price '
      'is a dry register and sections that stopped at older releases.',
      'diller')
    a('https://www.stroustrup.com/C++.html', 'Stroustrup on C++',
      ['c-ailesi', 'referans', 'ücretsiz'],
      'C++’ın yaratıcısının kendi sayfası: sıkça sorulan sorular, üslup önerileri ve dilin neden '
      'öyle tasarlandığını anlatan yazılar. Öğreticilerden farkı gerekçe sunması — bir kararın '
      'nedenini ancak kararı verenden okuyabiliyorsun.',
      'The C++ creator’s own pages: FAQs, style advice and essays on why the language was designed '
      'as it was. Unlike tutorials it supplies rationale — the reason behind a decision is only '
      'available from the person who made it.',
      'diller')
    a('https://doc.qt.io/', 'Qt Documentation', ['dokümantasyon', 'c-ailesi', 'masaüstü'],
      'Qt çatısının resmî belgeleri; C++ ve QML için sınıf referansı, örnekler ve platform '
      'kılavuzları. Diğer arayüz çatılarının belgelerinden farkı kapsamı — masaüstü, mobil ve '
      'gömülü aynı API altında anlatılıyor.',
      'The official documentation for the Qt framework: class reference, examples and platform '
      'guides for C++ and QML. Against other UI framework docs the difference is scope — desktop, '
      'mobile and embedded described under one API.',
      'diller')
    a('https://www.learnpython.org/', 'Learn Python',
      ['python', 'öğretici', 'interaktif', 'ücretsiz'],
      'Python’ı tarayıcıdaki alıştırmalarla öğreten etkileşimli giriş; kurulum gerektirmiyor. '
      'Kitaplardan farkı her bölümün sonunda çalıştırılan bir alıştırma olması — okuduğunun '
      'oturduğunu hemen görüyorsun.',
      'An interactive introduction teaching Python through in-browser exercises, with nothing to '
      'install. Against a book, each section ends in an exercise that runs — you see immediately '
      'whether it stuck.',
      'diller')
    a('https://www.learnshell.org/', 'Learn Shell',
      ['cli', 'öğretici', 'interaktif', 'ücretsiz'],
      'Kabuk betiklerini tarayıcıda çalıştırılabilir alıştırmalarla öğreten giriş. Kabuk '
      'kılavuzlarından farkı denemenin bedava olması — kendi makinende `rm` denemeye çekinirken '
      'burada takılıp kalmıyorsun.',
      'An introduction to shell scripting through exercises that run in the browser. Against the '
      'shell manuals the difference is that experimenting is free — you can try `rm` without '
      'hesitating over what it might hit.',
      'diller')
    a('https://guide.bash.academy/', 'The Bash Guide',
      ['cli', 'kitap', 'ücretsiz', 'referans'],
      'Bash’i baştan sona, doğru alışkanlıklarla öğreten rehber; tırnaklama ve kelime bölme gibi '
      'tuzakları erkenden ele alıyor. Kopyala-yapıştır öğreticilerinden farkı bu — çoğu betik '
      'hatası tam olarak o tuzaklardan çıkıyor.',
      'A guide teaching Bash end to end with the right habits, tackling quoting and word splitting '
      'early. That is the break from copy-paste tutorials: most script bugs come from exactly '
      'those traps.',
      'diller')

    # ============================================================ TOOLS
    a('https://explainshell.com/', 'explainshell', ['cli', 'ücretsiz', 'referans'],
      'Bir kabuk komutunu yapıştırınca her parçasının man sayfasındaki karşılığını gösteriyor. '
      '`man` okumaktan farkı ters yönde çalışması — elindeki komutun `-xzvf` kısmının ne anlama '
      'geldiğini kılavuzu taramadan öğreniyorsun.',
      'Paste a shell command and it maps every fragment to its entry in the man page. Against '
      'reading `man` it works backwards — you learn what the `-xzvf` in front of you means without '
      'scanning the manual.',
      'araclar')
    a('https://www.cs.usfca.edu/~galles/visualization/Algorithms.html', 'Data Structure Visualization',
      ['algoritma', 'interaktif', 'akademik', 'ücretsiz'],
      'Veri yapısı ve algoritmaların adım adım canlandırıldığı klasik koleksiyon; kırmızı-siyah '
      'ağaçtan Dijkstra’ya. Modern görselleştiricilerden farkı kapsamı ve hızının senin '
      'denetiminde olması — her adımı durdurup geri alabiliyorsun.',
      'The classic collection of step-by-step animations for data structures and algorithms, from '
      'red-black trees to Dijkstra. Against newer visualisers it wins on coverage and on giving '
      'you the speed control — every step can be paused and reversed.',
      'ogrenme')
    a('https://pythontutor.com/visualize.html', 'Python Tutor',
      ['interaktif', 'python', 'ücretsiz', 'öğretici'],
      'Kodu satır satır çalıştırıp bellekteki nesneleri ve işaretçileri çizerek gösteriyor; '
      'Python, Java, C ve C++ destekliyor. Hata ayıklayıcıdan farkı yığın ve öbek arasındaki '
      'ilişkiyi resmetmesi — işaretçi kavramını anlatmanın en kısa yolu.',
      'Runs code line by line and draws the objects and pointers in memory, covering Python, Java, '
      'C and C++. Against a debugger it pictures the relationship between stack and heap, which is '
      'the shortest route to explaining what a pointer is.',
      'ogrenme')
    a('https://jsoncrack.com/', 'JSON Crack', ['açık-kaynak', 'tarayıcı-içi', 'ücretsiz'],
      'JSON’u ağaç yerine düğüm grafiği olarak çiziyor; iç içe yapılar tek bakışta görülüyor. '
      'JSON biçimlendiricilerinden farkı bu grafik gösterim — derin bir yanıtın şeklini anlamak '
      'için girintilere bakmaktan hızlı.',
      'Draws JSON as a node graph rather than a tree, so nested structures are visible at a glance. '
      'Against a JSON formatter that graph view is the point — faster than counting indentation to '
      'work out the shape of a deep response.',
      'araclar')
    a('https://webhook.site/', 'Webhook.site', ['api', 'ücretsiz', 'tarayıcı-içi'],
      'Anında bir URL veriyor ve o adrese gelen istekleri başlıklarıyla birlikte gösteriyor. '
      'Yerel sunucu açıp tünellemekten farkı sıfır kurulum — bir webhook’un gerçekten ne '
      'gönderdiğini görmek için en kısa yol.',
      'Hands you a URL instantly and shows every request that arrives, headers included. Against '
      'running a local server behind a tunnel it needs no setup — the shortest way to see what a '
      'webhook actually sends.',
      'backend')
    a('https://sourcegraph.com/search', 'Sourcegraph', ['github', 'referans', 'freemium'],
      'Açık kaynak depolarda kod araması; düzenli ifade ve yapısal sorgu destekliyor. GitHub '
      'aramasından farkı depo sınırı olmadan tüm ekosistemde arayabilmesi — bir API’nin gerçek '
      'dünyada nasıl çağrıldığını görmek için.',
      'Code search across open-source repositories, with regular expressions and structural '
      'queries. Against GitHub search it spans the ecosystem rather than one repository — the way '
      'to see how an API is actually called in the wild.',
      'referans')
    a('https://yqnn.github.io/svg-path-editor/', 'SVG Path Editor',
      ['açık-kaynak', 'tarayıcı-içi', 'frontend', 'ücretsiz'],
      'SVG yol verisini (`d` özniteliği) görsel olarak düzenleyip komutları tek tek gösteriyor. '
      'Genel vektör editörlerinden farkı yolun ham metnine dokunabilmen — elle yazılmış bir '
      'ikonu düzeltmek için doğru araç.',
      'Edits SVG path data (the `d` attribute) visually while listing the commands one by one. '
      'Against a general vector editor you get at the raw path text, which is what you want for '
      'fixing a hand-written icon.',
      'medya')
    a('https://snapsvg.io/', 'Snap.svg', ['açık-kaynak', 'javascript', 'frontend'],
      'SVG’yi betikle üretmek ve canlandırmak için JavaScript kütüphanesi; Raphaël’in modern '
      'tarayıcılara yazılmış hâli. D3’ten farkı veri görselleştirme değil doğrudan SVG '
      'kurgulaması — grafik değil grafik nesnesi üretiyorsun.',
      'A JavaScript library for generating and animating SVG, written as Raphaël’s successor for '
      'modern browsers. Against D3 it is not about data visualisation but about composing SVG '
      'directly — you produce graphics, not charts.',
      'web')
    a('https://onelang.io/', 'OneLang', ['açık-kaynak', 'tarayıcı-içi', 'ücretsiz'],
      'Bir dilde yazılan kodu başka dillere çeviren deneysel araç; C#, Java, Python, JavaScript. '
      'Sözdizimi tablolarından farkı çalışan çeviri üretmesi — bir dilin kalıbının başka dilde '
      'nasıl karşılandığını görmek için.',
      'An experimental tool that converts code written in one language into others — C#, Java, '
      'Python, JavaScript. Against a syntax comparison table it produces working translations, '
      'which shows how one language’s idiom lands in another.',
      'araclar')
    a('https://playcode.io/', 'PlayCode', ['tarayıcı-içi', 'javascript', 'freemium'],
      'Yazdıkça çalışan JavaScript ve TypeScript oyun alanı; npm paketi ekleyebiliyorsun. '
      'CodePen’den farkı anlık geri bildirim ve konsolun her zaman görünür olması — kütüphane '
      'denemek için CodeSandbox’tan hafif.',
      'A JavaScript and TypeScript playground that runs as you type and accepts npm packages. '
      'Against CodePen the feedback is instant and the console always visible; against CodeSandbox '
      'it is lighter for trying a library.',
      'araclar')
    a('https://phpize.online/', 'phpize.online', ['php', 'tarayıcı-içi', 'ücretsiz', 'sql'],
      'PHP kodunu farklı sürümlerde çalıştırıp yanına MySQL, PostgreSQL veya SQLite bağlayan '
      'oyun alanı. Diğer PHP oyun alanlarından farkı veritabanı bağlantısı sunması — sorgu '
      'davranışını denemek için sunucu kurmaya gerek kalmıyor.',
      'A playground that runs PHP across versions with MySQL, PostgreSQL or SQLite attached. '
      'Unlike other PHP playgrounds it gives you a database, so trying query behaviour needs no '
      'server of your own.',
      'diller')
    a('https://coder.com/', 'Coder', ['açık-kaynak', 'self-hosted', 'sunucu', 'devops'],
      'Geliştirme ortamını kendi altyapında kapsayıcı olarak çalıştıran platform; VS Code ya da '
      'JetBrains istemcisiyle bağlanıyorsun. GitHub Codespaces’ten farkı bulut sağlayıcısına '
      'bağlı olmaması — kaynak da kod da sende kalıyor.',
      'Runs development environments as containers on your own infrastructure, reached from a VS '
      'Code or JetBrains client. Against GitHub Codespaces it is not tied to a cloud provider — '
      'both the compute and the code stay with you.',
      'devops')
    a('https://kodytools.com/dev-tools', 'Kody Tools', ['tarayıcı-içi', 'ücretsiz', 'referans'],
      'Dönüştürücü, biçimlendirici ve üreteçlerden oluşan geliştirici araç koleksiyonu. IT Tools '
      'gibi derlemelerden farkı görsel ve metin araçlarını bir arada tutması — renk, görsel ve '
      'kod araçları aynı yerde.',
      'A collection of developer converters, formatters and generators. Against compilations like '
      'IT Tools it keeps visual and textual tools together — colour, image and code utilities in '
      'one place.',
      'araclar')
    a('https://www.keybr.com/', 'keybr.com', ['interaktif', 'ücretsiz'],
      'On parmak yazmayı öğreten alıştırma; hangi harfte zorlandığını ölçüp metni ona göre '
      'üretiyor. Sabit metinli yazma testlerinden farkı bu uyarlama — zayıf harfleri daha sık '
      'karşına çıkarıyor.',
      'Touch-typing practice that measures which letters you struggle with and generates text '
      'accordingly. Against fixed-text typing tests that adaptation is the point — your weak '
      'letters keep coming back.',
      'araclar')
    a('https://wakatime.com/', 'WakaTime', ['gözlemlenebilirlik', 'freemium', 'eklenti'],
      'Editör eklentisiyle hangi projede, hangi dilde ne kadar zaman geçirdiğini ölçüyor. '
      'Genel zaman takip araçlarından farkı elle başlatma gerektirmemesi — ölçüm editörün '
      'kendisinden geliyor.',
      'Measures how long you spend in which project and language through an editor plugin. Against '
      'general time trackers it needs no manual start — the measurement comes from the editor '
      'itself.',
      'araclar')

    # ============================================================ GIT & OPEN SOURCE
    a('https://maryrosecook.com/blog/post/git-from-the-inside-out', 'Git from the Inside Out',
      ['git', 'referans', 'ücretsiz'],
      'Git’i komutlarından değil veri modelinden anlatan uzun yazı: her komutun `.git` klasöründe '
      'ne değiştirdiğini adım adım gösteriyor. Komut rehberlerinden farkı bu — modeli anlayınca '
      'komutları ezberlemeye gerek kalmıyor.',
      'A long essay explaining Git from its data model rather than its commands, showing what each '
      'command changes inside `.git`. That is the difference from a command guide: once the model '
      'is clear the commands stop needing memorisation.',
      'referans')
    a('https://wildlyinaccurate.com/a-hackers-guide-to-git/', "A Hacker's Guide to Git",
      ['git', 'referans', 'ücretsiz'],
      'Git’in nesne veritabanını, referanslarını ve birleştirme algoritmasını açıklayan rehber. '
      '"Git from the Inside Out"tan farkı daha kısa ve komut odaklı olması — ikisi birbirini '
      'tamamlıyor.',
      'A guide to Git’s object database, refs and merge algorithm. Against "Git from the Inside '
      'Out" it is shorter and more command-oriented — the two complement each other.',
      'referans')
    a('https://guides.github.com/features/mastering-markdown/', 'Mastering Markdown',
      ['dokümantasyon', 'github', 'ücretsiz', 'kopya-kâğıdı'],
      'GitHub’ın kendi Markdown lehçesinin resmî özeti: tablolar, görev listeleri, kod blokları, '
      'bahsetmeler. Genel Markdown referanslarından farkı GitHub’a özgü eklentileri kapsaması — '
      'README yazarken doğru kaynak bu.',
      'GitHub’s official summary of its own Markdown dialect: tables, task lists, code fences, '
      'mentions. Against a general Markdown reference it covers the GitHub-specific extensions, '
      'which is what a README actually renders with.',
      'referans')
    a('https://up-for-grabs.net/', 'Up For Grabs', ['açık-kaynak', 'github', 'ücretsiz'],
      'Yeni katkıcılar için ayrılmış issue’ları olan projeleri listeliyor. GitHub’ta etiket '
      'aramaktan farkı projelerin bu iş için gönüllü olması — issue’yu açan kişi zaten birinin '
      'gelmesini bekliyor.',
      'Lists projects that set aside issues for new contributors. Against searching labels on '
      'GitHub the projects here opted in — whoever opened the issue is already waiting for someone '
      'to take it.',
      'referans')
    a('https://www.firsttimersonly.com/', 'First Timers Only',
      ['açık-kaynak', 'öğretici', 'ücretsiz'],
      'İlk açık kaynak katkısını yapmak isteyenler için hazırlanmış giriş; korkuyu azaltmaya '
      'odaklanıyor. Katkı rehberlerinden farkı teknik değil psikolojik engeli ele alması.',
      'An introduction for people making their first open-source contribution, aimed squarely at '
      'reducing the fear. Unlike contribution guides it addresses the psychological barrier rather '
      'than the technical one.',
      'referans')
    a('https://github.com/MunGell/awesome-for-beginners', 'Awesome for Beginners',
      ['awesome-liste', 'açık-kaynak', 'github'],
      'Yeni başlayanlara uygun issue’ları olan depoların dil bazında listesi. Up For Grabs’tan '
      'farkı programlama diline göre ayrılmış olması — bildiğin dilde bir proje bulmak kolay.',
      'A list of repositories with beginner-friendly issues, organised by programming language. '
      'Against Up For Grabs the split by language is the difference — finding a project in a '
      'language you know is straightforward.',
      'referans')
    a('https://opensource.com/', 'Opensource.com', ['açık-kaynak', 'ücretsiz', 'referans'],
      'Açık kaynak kültürü, araçları ve yönetişimi üzerine yazı arşivi; Red Hat destekliyor. '
      'Teknik bloglardan farkı lisans, topluluk ve kurumsal benimseme gibi konulara girmesi.',
      'An archive of writing on open-source culture, tooling and governance, supported by Red Hat. '
      'Against technical blogs it goes into licensing, community and institutional adoption.',
      'referans')
    a('https://opensource.google/', 'Google Open Source', ['açık-kaynak', 'referans', 'ücretsiz'],
      'Google’ın açık kaynak projeleri, politikaları ve programları için merkez sayfa. Depoya '
      'tek tek bakmaktan farkı kurumsal politikanın da yayımlanmış olması — büyük bir şirketin '
      'açık kaynağı nasıl yönettiğini görmek için.',
      'The hub for Google’s open-source projects, policies and programmes. Against browsing the '
      'repositories one by one, the corporate policy is published too — a look at how a large '
      'company runs open source.',
      'referans')
    a('https://summerofcode.withgoogle.com/', 'Google Summer of Code',
      ['açık-kaynak', 'ücretsiz', 'müfredat'],
      'Öğrencileri açık kaynak projelerle eşleştiren ve ücretli çalıştıran yıllık program. '
      'Staj başvurusundan farkı çıktının kamuya açık olması — yaptığın iş özgeçmişte bağlantı '
      'olarak duruyor.',
      'An annual programme that pairs students with open-source projects and pays them. Against an '
      'internship the output is public — the work sits on your résumé as a link.',
      'referans')
    a('https://fellowship.mlh.io/', 'MLH Fellowship', ['açık-kaynak', 'müfredat', 'ücretsiz'],
      'Uzaktan, takım hâlinde açık kaynak katkısı yaptıran burslu program. Google Summer of '
      'Code’dan farkı takım çalışması ve mentorluğun yapılandırılmış olması — tek başına değil '
      'ekiple çalışıyorsun.',
      'A funded remote programme where you contribute to open source in a team. Against Google '
      'Summer of Code the teamwork and mentorship are structured — you work with a group rather '
      'than alone.',
      'referans')
    a('https://www.gitcoin.co/', 'Gitcoin', ['açık-kaynak', 'github', 'freemium'],
      'Açık kaynak işlerine ödül koyup fon toplayan platform; Ethereum ekosisteminde doğdu. '
      'Bağış düğmelerinden farkı işi ödüllendirmesi — belirli bir issue’ya para bağlanabiliyor.',
      'A platform for placing bounties on open-source work and raising funds, born in the Ethereum '
      'ecosystem. Against a donate button it rewards the work: money can be attached to a specific '
      'issue.',
      'referans')

    # ============================================================ SYSADMIN
    a('https://linuxcommand.org/', 'LinuxCommand.org', ['ağ', 'cli', 'kitap', 'ücretsiz'],
      'Komut satırını sıfırdan öğretip kabuk betiği yazmaya götüren site; "The Linux Command '
      'Line" kitabının kaynağı. Komut listelerinden farkı bir yol izlemesi — dağınık kopya '
      'kâğıdı değil, sıralı bir ders.',
      'Teaches the command line from nothing and carries you into shell scripting; the home of '
      '"The Linux Command Line". Against a list of commands it follows a path — a sequenced course '
      'rather than a scattered cheat sheet.',
      'ag')
    a('https://ryanstutorials.net/linuxtutorial/', 'Ryan’s Linux Tutorial',
      ['ağ', 'cli', 'öğretici', 'ücretsiz'],
      'Linux ve Bash’e giriş; her bölümün sonunda alıştırma var. LinuxCommand.org’dan farkı daha '
      'kısa ve sınav odaklı olması — temel komutları hızla geçmek isteyenler için.',
      'An introduction to Linux and Bash with exercises closing every section. Against '
      'LinuxCommand.org it is shorter and more drill-oriented — for getting through the basic '
      'commands quickly.',
      'ag')
    a('https://mempool.space/', 'mempool.space', ['açık-kaynak', 'self-hosted', 'gözlemlenebilirlik'],
      'Bitcoin ağının bekleyen işlem havuzunu ve blok zincirini görselleştiren gezgin; kendi '
      'düğümünle çalıştırılabiliyor. Diğer blok gezginlerinden farkı ücret tahmini ve mempool '
      'görselleştirmesi — ağın o anki tıkanıklığını gösteriyor.',
      'An explorer visualising Bitcoin’s pending transaction pool and the chain, runnable against '
      'your own node. Against other block explorers it adds fee estimation and a mempool view — it '
      'shows how congested the network is right now.',
      'ag')
    a('https://learnmeabitcoin.com/', 'Learn Me a Bitcoin', ['öğretici', 'ücretsiz', 'referans'],
      'Bitcoin’in teknik işleyişini — işlem yapısı, betik dili, madencilik — örneklerle anlatan '
      'site. Beyaz bültenden farkı somut olması: gerçek işlemleri baytına kadar açıp gösteriyor.',
      'Explains Bitcoin’s technical workings — transaction structure, script, mining — through '
      'worked examples. Against the whitepaper it is concrete: real transactions pulled apart byte '
      'by byte.',
      'referans')

    # ============================================================ REFERENCE & MEDIA
    a('https://www.promptingguide.ai/', 'Prompt Engineering Guide',
      ['llm', 'referans', 'ücretsiz', 'akademik'],
      'İstem mühendisliği tekniklerini akademik kaynaklara dayandırarak toplayan rehber: '
      'düşünce zinciri, az örnekli öğrenme, RAG. Blog yazılarından farkı her tekniğin makale '
      'atfıyla gelmesi — iddia ile bulgu ayrışıyor.',
      'A guide collecting prompt engineering techniques with academic citations: chain of thought, '
      'few-shot, RAG. Against blog posts each technique carries a paper reference, which separates '
      'claim from finding.',
      'yz_altyapi')
    a('https://speaking.io/', 'speaking.io', ['referans', 'ücretsiz', 'kitap'],
      'Teknik konuşma hazırlamak ve sunmak üzerine rehber: içerik kurma, slayt tasarımı, sahne '
      'korkusu. Genel sunum tavsiyelerinden farkı geliştirici konferanslarına özgü olması — '
      'canlı demo riski gibi konular ele alınıyor.',
      'A guide to preparing and delivering technical talks: structuring content, slide design, '
      'stage fright. Against general presentation advice it is specific to developer conferences — '
      'the risk of a live demo gets its own treatment.',
      'referans')
    a('https://sqlzoo.net/wiki/SQL_Tutorial', 'SQLZoo',
      ['sql', 'interaktif', 'ücretsiz', 'öğretici'],
      'SQL’i doğrudan tarayıcıda sorgu yazdırarak öğreten alıştırma seti; her bölüm bir veri '
      'kümesi üzerinde. Kurulum gerektiren öğreticilerden farkı bu — ilk `SELECT`’ini yazmak için '
      'veritabanı kurmak gerekmiyor.',
      'An exercise set that teaches SQL by making you write queries in the browser, each section '
      'over its own dataset. That is the difference from tutorials needing an install: your first '
      '`SELECT` requires no database.',
      'veritabani')
    a('https://learnvimscriptthehardway.stevelosh.com/', 'Learn Vimscript the Hard Way',
      ['kitap', 'cli', 'ücretsiz'],
      'Vim’i yapılandırmak ve eklenti yazmak için Vimscript öğreten kitap. Vim kullanım '
      'rehberlerinden farkı editörü kullanmayı değil programlamayı anlatması — `.vimrc`’in '
      'ötesine geçmek isteyenler için.',
      'A book teaching Vimscript for configuring Vim and writing plugins. Unlike Vim usage guides '
      'it is about programming the editor rather than using it — for going past `.vimrc`.',
      'referans')
    a('https://www.geeksforgeeks.org/', 'GeeksforGeeks',
      ['referans', 'algoritma', 'ücretsiz'],
      'Algoritma, veri yapısı ve dil konularında çok geniş bir makale arşivi. Kapsamı en büyük '
      'gücü, tutarsızlığı en büyük zayıflığı: aynı konuda birbirinden farklı kalitede yazılar '
      'bulunuyor, kod örneklerini doğrulamadan kullanma.',
      'An enormous archive of articles on algorithms, data structures and languages. Its breadth '
      'is its strength and its inconsistency the weakness: quality varies sharply between articles '
      'on the same subject, so verify code before using it.',
      'referans')
    a('https://www.tutorialspoint.com/index.htm', 'TutorialsPoint',
      ['referans', 'öğretici', 'ücretsiz'],
      'Yüzlerce teknoloji için kısa öğretici serileri. GeeksforGeeks’ten farkı konu başına düzenli '
      'bir sıra izlemesi; karşılığında derinliği sınırlı — bir teknolojiye hızlı bakış için '
      'uygun, ustalaşmak için değil.',
      'Short tutorial series for hundreds of technologies. Against GeeksforGeeks it follows an '
      'orderly sequence per subject; the trade is limited depth — good for a first look at a '
      'technology, not for mastering one.',
      'referans')
    a('https://www.codeproject.com/', 'CodeProject', ['referans', 'ücretsiz', 'c-ailesi'],
      'Geliştiricilerin yazdığı, çalışan kod içeren uzun makale arşivi; ağırlık .NET ve C++ '
      'tarafında. Blog toplayıcılarından farkı her makalenin indirilebilir kaynak projesiyle '
      'gelmesi.',
      'An archive of long, developer-written articles with working code, weighted towards .NET and '
      'C++. Against a blog aggregator each article ships with a downloadable source project.',
      'referans')
    a('https://dzone.com/', 'DZone', ['referans', 'ücretsiz', 'devops'],
      'Yazılım geliştirme, DevOps ve mimari üzerine makale ve "refcard" arşivi. Kişisel '
      'bloglardan farkı refcard’lar — tek konuyu iki sayfaya sığdıran indirilebilir özetler.',
      'An archive of articles and "refcards" on software development, DevOps and architecture. The '
      'refcards are what distinguish it from personal blogs: downloadable two-page summaries of a '
      'single subject.',
      'referans')
    a('https://www.infoq.com/presentations/', 'InfoQ Presentations',
      ['video', 'sistem-tasarımı', 'ücretsiz'],
      'Yazılım konferanslarından seçilmiş sunumların video arşivi; çoğunda yazıya dökülmüş metin '
      'de var. YouTube’dan farkı küratörlü ve aranabilir olması — konu ve seviyeye göre '
      'süzülüyor.',
      'A video archive of selected talks from software conferences, most with a transcript. '
      'Against YouTube it is curated and searchable, filterable by subject and level.',
      'referans')
    a('https://classpert.com/', 'Classpert', ['müfredat', 'referans', 'ücretsiz'],
      'Farklı platformlardaki çevrimiçi kursları tek yerde arayan dizin. Tek tek platformlara '
      'bakmaktan farkı fiyat ve süre karşılaştırması — aynı konunun beş ayrı kursunu yan yana '
      'koyabiliyorsun.',
      'A directory searching online courses across platforms. Against checking each platform it '
      'compares price and length — five courses on the same subject, side by side.',
      'ogrenme')

    # ============================================================ VIDEO CHANNELS
    a('https://www.youtube.com/user/computerphile/videos', 'Computerphile',
      ['video', 'ücretsiz', 'algoritma'],
      'Bilgisayar bilimi kavramlarını akademisyenlerle konuşarak anlatan kanal. Öğretici '
      'kanallardan farkı kod öğretmemesi — şifreleme, derleyici ya da karmaşıklık gibi konuların '
      'arkasındaki fikri anlatıyor.',
      'A channel explaining computer science concepts in conversation with academics. Unlike '
      'tutorial channels it does not teach code — it explains the idea behind encryption, '
      'compilers or complexity.',
      'ogrenme')
    a('https://www.youtube.com/user/cppcon/videos', 'CppCon', ['video', 'c-ailesi', 'ücretsiz'],
      'Yıllık C++ konferansının tüm konuşmaları. Öğreticilerden farkı dilin standardını yazan '
      'kişilerin sunumlarını içermesi — bir özelliğin neden öyle tasarlandığını burada '
      'duyuyorsun.',
      'Every talk from the annual C++ conference. Against tutorials it carries presentations from '
      'the people who write the standard — where you hear why a feature was designed as it was.',
      'diller')
    a('https://www.youtube.com/user/MeetingCPP/videos', 'Meeting C++',
      ['video', 'c-ailesi', 'ücretsiz'],
      'Avrupa’nın en büyük C++ konferansının konuşma arşivi. CppCon’dan farkı daha küçük ve '
      'uygulama ağırlıklı olması — standart tartışmasından çok gerçek projelerden deneyimler.',
      'The talk archive of Europe’s largest C++ conference. Against CppCon it is smaller and more '
      'applied — experience from real projects rather than standards debate.',
      'diller')
    a('https://www.youtube.com/user/GoogleTechTalks/videos', 'Google Tech Talks',
      ['video', 'akademik', 'ücretsiz'],
      'Google’da verilen teknik konuşmaların arşivi; birçoğu alanının kurucu isimlerinden. '
      'Konferans kayıtlarından farkı iç seyirciye anlatılmış olması — soru-cevap bölümleri '
      'genelde konuşmanın kendisinden değerli.',
      'The archive of technical talks given at Google, many by the founding figures of their '
      'fields. Against conference recordings these were delivered to an internal audience, and the '
      'Q&A is often worth more than the talk.',
      'referans')
    a('https://www.youtube.com/user/GotoConferences', 'GOTO Conferences',
      ['video', 'sistem-tasarımı', 'ücretsiz'],
      'Yazılım mimarisi ve mühendislik kültürü ağırlıklı konferans kayıtları. Dile özgü '
      'konferanslardan farkı teknoloji bağımsız olması — mimari kararlar ve takım pratikleri '
      'üzerine.',
      'Conference recordings weighted towards software architecture and engineering culture. '
      'Unlike language-specific conferences it is technology-agnostic — about architectural '
      'decisions and team practice.',
      'referans')
    a('https://www.youtube.com/user/ComputerHistory/videos', 'Computer History Museum',
      ['video', 'akademik', 'ücretsiz'],
      'Bilgisayar tarihinin öncüleriyle yapılmış sözlü tarih röportajları ve ders arşivi. Teknik '
      'kanallardan farkı bir kararın hangi koşullarda alındığını kaydetmesi — belgelerde yazmayan '
      'bağlam burada.',
      'Oral history interviews with the pioneers of computing, plus a lecture archive. Unlike '
      'technical channels it records the circumstances a decision was made in — the context no '
      'document holds.',
      'bilim')
    a('https://www.youtube.com/user/mycodeschool/videos', 'mycodeschool',
      ['video', 'algoritma', 'ücretsiz'],
      'Veri yapıları ve algoritmaları tahta üzerinde anlatan klasik seri. Yeni kanallardan farkı '
      'kod yerine mantığa odaklanması — bağlı liste ve ağaç konularında hâlâ en açık anlatımlardan '
      'biri.',
      'The classic whiteboard series on data structures and algorithms. Against newer channels it '
      'focuses on the reasoning rather than the code, and remains one of the clearest treatments '
      'of linked lists and trees.',
      'ogrenme')
    a('https://www.youtube.com/user/tusharroy2525/videos', 'Tushar Roy',
      ['video', 'algoritma', 'mülakat', 'ücretsiz'],
      'Algoritma sorularını adım adım çözen kanal; dinamik programlama serisi özellikle bilinir. '
      'Çözüm okumaktan farkı düşünme sürecini sesli göstermesi — mülakatta beklenen de bu.',
      'A channel working algorithm problems step by step, best known for its dynamic programming '
      'series. Against reading a solution it shows the thinking aloud, which is what an interview '
      'asks for.',
      'pratik')
    a('https://www.youtube.com/c/takeUforward', 'take U forward',
      ['video', 'algoritma', 'mülakat', 'ücretsiz'],
      'Veri yapısı ve algoritma konularını sıralı bir müfredat hâlinde veren kanal. Dağınık '
      'çözüm videolarından farkı sırayla izlenmek üzere kurgulanmış olması.',
      'A channel presenting data structures and algorithms as an ordered curriculum. Unlike '
      'scattered solution videos it is built to be watched in sequence.',
      'pratik')
    a('https://www.youtube.com/user/derekbanas/videos', 'Derek Banas',
      ['video', 'öğretici', 'ücretsiz'],
      'Bir dili ya da çatıyı tek videoda özetleyen "hızlandırılmış kurs" serisi. Uzun kurslardan '
      'farkı yoğunluğu — bildiğin bir dilden yenisine geçerken sözdizimini bir oturuşta '
      'topluyorsun.',
      'A "crash course" series summarising a language or framework in a single video. Against long '
      'courses the density is the point — moving from a language you know to a new one, you pick '
      'up the syntax in one sitting.',
      'ogrenme')
    a('https://www.youtube.com/user/thenewboston/videos', 'thenewboston',
      ['video', 'öğretici', 'ücretsiz'],
      'Çok sayıda dil ve teknoloji için kısa bölümlerden oluşan geniş öğretici arşivi. Modern '
      'kurslardan farkı arşiv niteliği — bazı seriler eskimiş, ama kapsamı hâlâ az bulunur.',
      'A large archive of tutorials in short episodes across many languages and technologies. '
      'Against modern courses it is an archive — some series have aged, but the breadth is still '
      'rare.',
      'ogrenme')
    a('https://www.youtube.com/user/kudvenkat', 'kudvenkat', ['video', 'öğretici', 'ücretsiz'],
      '.NET, C# ve SQL Server konularında uzun ve düzenli ders serileri. Kısa öğreticilerden farkı '
      'her serinin bir müfredat gibi ilerlemesi — kurumsal .NET yığınını sıfırdan öğrenmek için.',
      'Long, orderly lecture series on .NET, C# and SQL Server. Against short tutorials each '
      'series advances like a syllabus — for learning the enterprise .NET stack from nothing.',
      'diller')
    a('https://www.youtube.com/user/thoughtbotvideo/videos', 'thoughtbot',
      ['video', 'ücretsiz', 'sistem-tasarımı'],
      'Bir yazılım danışmanlığının kayıtları: eşli programlama oturumları, kod incelemeleri, '
      'tasarım tartışmaları. Öğretici kanallardan farkı gerçek işin kaydı olması — hazırlanmış '
      'ders değil, çalışan insanlar.',
      'Recordings from a software consultancy: pair programming sessions, code reviews, design '
      'discussions. Unlike tutorial channels this is a record of real work — people working, not a '
      'prepared lesson.',
      'referans')
    a('https://www.youtube.com/user/ThinMatrix/videos', 'ThinMatrix',
      ['video', 'interaktif', 'ücretsiz'],
      'Bağımsız oyun geliştiricisinin kendi oyununu yaparken tuttuğu günlük ve OpenGL ders '
      'serisi. Motor öğreticilerinden farkı motoru sıfırdan yazması — soyutlamanın altında ne '
      'olduğunu gösteriyor.',
      'An indie developer’s devlog alongside an OpenGL tutorial series. Unlike engine tutorials he '
      'writes the engine from scratch, which shows what sits underneath the abstraction.',
      'mobil')
    a('https://www.youtube.com/user/Hak5Darren', 'Hak5', ['video', 'güvenlik', 'ücretsiz'],
      'Sızma testi araçlarını ve tekniklerini uygulamalı gösteren güvenlik kanalı. Teorik '
      'anlatımlardan farkı donanım tarafına girmesi — ağ implantları ve fiziksel saldırı '
      'araçları burada.',
      'A security channel demonstrating penetration testing tools and techniques hands-on. Against '
      'theoretical treatments it goes to the hardware side — network implants and physical attack '
      'tools.',
      'guvenlik')
