# -*- coding: utf-8 -*-
"""Records surfaced by the awesome-useful-websites collection.

The source runs to about 1,400 links across every subject from lawn care to
astronomy. Only the sections inside this directory's scope were read, and
inside those, only entries that were still alive and not already here.

Four candidates were dropped as genuinely dead rather than kept on faith:
Damn Cool Algorithms, the Real World Haskell online book, DataTau and
electronics-tutorials.ws. Two had moved and their URLs were corrected.

These carry src='awesome-uw'.
"""

S = 'awesome-uw'


def load(add):
    def a(url, name, tags, tr, en, cat):
        add(url, name, tags, tr, en, cat, S)

    # ============================================================ LEARNING & CS
    a('https://teachyourselfcs.com/', 'Teach Yourself CS', ['müfredat', 'referans', 'ücretsiz'],
      'Bilgisayar bilimini kendi başına çalışmak için dokuz konu ve her konuda tek bir kitap ile '
      'tek bir ders önerisi. Diğer yol haritalarından farkı seçenek sunmaması: "en iyi kaynak '
      'hangisi" tartışmasını sizin yerinize kapatıp neden o kaynağı seçtiğini yazıyor.',
      'Nine subjects for self-teaching computer science, each with exactly one book and one course '
      'recommended. Unlike other roadmaps it refuses to offer options: it settles the "which '
      'resource" argument for you and explains why it chose that one.',
      'ogrenme')
    a('https://www.learnbyexample.org/', 'LearnByExample', ['öğretici', 'python', 'ücretsiz'],
      'Python, SQL ve R’ı çalıştırılabilir örneklerle öğreten site; her kavram tek bir küçük '
      'kod parçasıyla açılıyor. Belgelerden farkı sıra: önce çalışan örnek, sonra açıklama — '
      'sözdizimini hatırlamak için hızlı bir referans olarak da işe yarıyor.',
      'Teaches Python, SQL and R through runnable examples, opening each concept with one small '
      'piece of code. Against documentation the order is reversed — working example first, '
      'explanation after — which also makes it a fast syntax refresher.',
      'diller')
    a('https://en.algorithmica.org/hpc/', 'Algorithmica HPC', ['algoritma', 'kitap', 'ücretsiz'],
      'Modern donanımda hızlı kod yazmayı anlatan çevrimiçi kitap: önbellek hiyerarşisi, SIMD, '
      'dallanma tahmini. Algoritma kitaplarından farkı büyük-O yerine gerçek makinede geçen süreye '
      'bakması — aynı karmaşıklıktaki iki çözümün neden farklı hızda çalıştığını açıklıyor.',
      'An online book on writing fast code for modern hardware: cache hierarchy, SIMD, branch '
      'prediction. Where algorithm books stop at big-O, this measures wall-clock time on a real '
      'machine and explains why two solutions of equal complexity differ by tenfold.',
      'referans')
    a('https://xlinux.nist.gov/dads/', 'Dictionary of Algorithms and Data Structures',
      ['referans', 'algoritma', 'ücretsiz'],
      'NIST’in algoritma ve veri yapısı sözlüğü; her terim için kısa tanım, varsa formal '
      'tanımlama ve uygulama bağlantısı. Vikipedi’den farkı kısalığı ve terminolojide otorite '
      'olması — bir terimin doğru adını aradığında buraya bakılır.',
      'NIST’s dictionary of algorithms and data structures, with a short definition, a formal '
      'statement where one exists, and links to implementations. Against Wikipedia it is terse and '
      'authoritative on terminology — the place to check what a thing is properly called.',
      'referans')
    a('https://cooervo.github.io/Algorithms-DataStructures-BigONotation/',
      'Algorithms & Big-O Reference', ['referans', 'algoritma', 'kopya-kâğıdı'],
      'Veri yapılarının ve sıralama algoritmalarının zaman/alan karmaşıklıklarını tek tabloda '
      'toplayan referans. Big-O Cheat Sheet’ten farkı her yapının kısa açıklamasını ve örnek '
      'kodunu da taşıması — tabloyu okumadan önce neye baktığını anlıyorsun.',
      'A single-table reference for the time and space complexity of data structures and sorting '
      'algorithms. Against the Big-O Cheat Sheet it also carries a short description and sample '
      'code per structure, so you know what you are reading before you read the table.',
      'referans')
    a('https://www.statlearning.com/', 'An Introduction to Statistical Learning',
      ['kitap', 'veri-bilimi', 'ücretsiz'],
      'İstatistiksel öğrenmenin standart giriş kitabı; PDF’i ücretsiz, R ve Python laboratuvarları '
      'ayrı ayrı var. "Elements of Statistical Learning"den farkı matematiği azaltıp sezgiyi öne '
      'alması — ikisi aynı yazarlardan, bu olanı önce okunanı.',
      'The standard introduction to statistical learning, free as a PDF with separate R and Python '
      'labs. Against "Elements of Statistical Learning" by the same authors it trades mathematics '
      'for intuition — this is the one you read first.',
      'veri')

    # ============================================================ PRACTICE & CTF
    a('https://ctf101.org/', 'CTF 101', ['güvenlik', 'öğretici', 'ücretsiz'],
      'Capture the Flag yarışmalarındaki kategorileri sıfırdan anlatan rehber: tersine mühendislik, '
      'kriptografi, adli bilişim, web. Yarışma platformlarından farkı soru değil temel vermesi — '
      'ilk CTF’ine girmeden önce okunacak metin.',
      'A ground-up guide to the categories in Capture the Flag competitions: reverse engineering, '
      'cryptography, forensics, web. Unlike a competition platform it hands you the fundamentals '
      'rather than challenges — the thing to read before your first CTF.',
      'guvenlik')
    a('https://ctftime.org/', 'CTFtime', ['güvenlik', 'ücretsiz', 'referans'],
      'CTF yarışmalarının takvimi, takım sıralamaları ve geçmiş yarışmaların çözüm yazıları. '
      'Tek tek yarışma sitelerinden farkı merkezî olması — hangi yarışmanın ne zaman olduğunu ve '
      'geçen yıl nasıl çözüldüğünü aynı yerden görüyorsun.',
      'The calendar of CTF competitions, team rankings, and write-ups from past events. Against '
      'individual competition sites it is the central register — when an event runs and how last '
      'year’s challenges were solved, in one place.',
      'guvenlik')
    a('https://github.com/google/google-ctf', 'Google CTF', ['güvenlik', 'açık-kaynak', 'github'],
      'Google’ın düzenlediği CTF yarışmalarının tüm soruları, kaynak kodları ve çözümleri. Diğer '
      'arşivlerden farkı soruların altyapısının da yayımlanması — yarışmayı kendi makinende '
      'yeniden kurup çalışabiliyorsun.',
      'Every challenge from Google’s CTF competitions, with source code and solutions. Unlike other '
      'archives the challenge infrastructure is published too, so you can stand the whole thing up '
      'locally and work through it.',
      'guvenlik')
    a('https://trailofbits.github.io/ctf/', 'Trail of Bits CTF Field Guide',
      ['güvenlik', 'ücretsiz', 'kitap'],
      'Güvenlik firması Trail of Bits’in CTF rehberi; her kategoride hangi becerinin gerektiğini ve '
      'nasıl çalışılacağını anlatıyor. CTF101’den farkı daha derin olması ve profesyonel güvenlik '
      'işine köprü kurması — yarışmadan mesleğe geçiş.',
      'The CTF guide from the security firm Trail of Bits, laying out which skill each category '
      'needs and how to build it. Deeper than CTF101, and it bridges toward professional security '
      'work rather than stopping at the competition.',
      'guvenlik')

    # ============================================================ LANGUAGES
    a('https://learnyouahaskell.github.io/chapters.html', 'Learn You a Haskell',
      ['kitap', 'ücretsiz', 'öğretici'],
      'Haskell’in en bilinen giriş kitabının topluluk tarafından güncellenmiş çevrimiçi hâli. '
      'Akademik Haskell kaynaklarından farkı üslubu: monad’ı kategori teorisiyle değil, çizimlerle '
      've kademeli örneklerle anlatıyor.',
      'The community-maintained online edition of the best-known Haskell introduction. Against the '
      'academic Haskell texts the difference is tone: it gets to monads through drawings and '
      'incremental examples rather than category theory.',
      'diller')
    a('https://www.seas.upenn.edu/~cis1940/spring13/lectures.html', 'CIS 194 Haskell',
      ['müfredat', 'ücretsiz', 'akademik'],
      'Pennsylvania Üniversitesi’nin Haskell dersi; ders notları ve ödevler açık. Kitaplardan farkı '
      'ödevlerin olması — Haskell’i okuyarak değil ancak yazarak öğrenebildiğin için bu ayrım '
      'önemli.',
      'The University of Pennsylvania’s Haskell course, with lecture notes and assignments public. '
      'The difference from a book is the homework — and since Haskell is learned by writing rather '
      'than reading, that difference matters.',
      'diller')
    a('https://guides.rubygems.org/', 'RubyGems Guides', ['dokümantasyon', 'ücretsiz', 'referans'],
      'RubyGems’in nasıl çalıştığını ve kendi gem’ini nasıl yayımlayacağını anlatan resmî rehber. '
      'API belgelerinden farkı sürüm numaralandırma, bağımlılık çözümleme ve yayımlama politikası '
      'gibi kararları da açıklaması.',
      'The official guide to how RubyGems works and how to publish your own gem. Against the API '
      'reference it also explains the decisions — version numbering, dependency resolution, '
      'publishing policy.',
      'diller')
    a('https://libraries.io/', 'Libraries.io', ['referans', 'açık-kaynak', 'ücretsiz'],
      'Otuzdan fazla paket yöneticisini tek yerde arayan dizin; bir kütüphanenin bağımlılıklarını '
      've ona bağımlı olanları gösteriyor. npm veya PyPI aramasından farkı ekosistemler arası '
      'olması ve terk edilmişlik sinyali vermesi.',
      'A directory searching more than thirty package managers at once, showing a library’s '
      'dependencies and its dependents. Against searching npm or PyPI directly it spans ecosystems '
      'and surfaces abandonment signals.',
      'referans')

    # ============================================================ WEB & FRONTEND
    a('https://css-tricks.com/snippets/', 'CSS-Tricks Snippets', ['referans', 'frontend', 'ücretsiz'],
      'CSS, HTML, JavaScript ve .htaccess için yıllar içinde biriktirilmiş parçacık arşivi. '
      'Rastgele blog yazılarından farkı her parçacığın kendi sayfası ve tartışması olması — '
      'yorumlarda genelde daha iyi bir sürüm bulunuyor.',
      'An archive of snippets for CSS, HTML, JavaScript and .htaccess built up over years. Against '
      'scattered blog posts each snippet has its own page and discussion — and the comments usually '
      'hold a better version.',
      'web')
    a('https://codetogo.io/', 'CodeToGo', ['referans', 'javascript', 'ücretsiz'],
      '"Diziyi nasıl ters çeviririm" gibi günlük JavaScript sorularına güncel tek satırlık cevaplar. '
      'Stack Overflow’dan farkı cevabın 2012’den kalma olmaması — modern söz dizimiyle güncel '
      'tutuluyor.',
      'Up-to-date one-line answers to everyday JavaScript questions like "how do I reverse an '
      'array". The difference from Stack Overflow is that the answer is not from 2012 — these are '
      'kept current with modern syntax.',
      'web')
    a('https://beautifier.io/', 'Beautifier.io', ['açık-kaynak', 'tarayıcı-içi', 'ücretsiz'],
      'JavaScript, HTML ve CSS’i biçimlendiren, küçültülmüş kodu açan araç. Prettier’dan farkı '
      'kurulum gerektirmemesi ve okunamaz hâle getirilmiş kodu geri açabilmesi — başkasının '
      'küçültülmüş dosyasını incelemek için.',
      'Formats JavaScript, HTML and CSS and unpacks minified code. Against Prettier it needs no '
      'install and can open obfuscated output back up — which is what you want when inspecting '
      'someone else’s minified bundle.',
      'araclar')
    a('https://codebeautify.org/', 'CodeBeautify', ['tarayıcı-içi', 'ücretsiz', 'referans'],
      'Biçimlendirme, doğrulama ve dönüştürme araçlarının toplandığı site: JSON, XML, YAML, SQL, '
      'Base64. IT Tools’tan farkı daha geniş ama daha reklamlı olması — burada olmayan bir dönüşüm '
      'bulmak zor.',
      'A collection of formatting, validation and conversion tools covering JSON, XML, YAML, SQL and '
      'Base64. Against IT Tools it is broader but heavier on ads — it is hard to find a conversion '
      'it lacks.',
      'araclar')

    # ============================================================ DEVOPS & LINTING
    a('https://www.shellcheck.net/', 'ShellCheck', ['açık-kaynak', 'cli', 'ücretsiz'],
      'Kabuk betiklerindeki hataları bulan statik çözümleyici; tırnaklanmamış değişken, yanlış '
      'test söz dizimi, taşınabilirlik sorunları. `bash -n`’den farkı sözdizimi değil anlam '
      'denetimi yapması — çalışan ama yanlış davranan betiği yakalıyor.',
      'A static analyser for shell scripts that finds unquoted variables, wrong test syntax and '
      'portability traps. Against `bash -n` it checks meaning rather than syntax, so it catches the '
      'script that runs and misbehaves.',
      'devops')
    a('https://jsonlint.com/', 'JSONLint', ['tarayıcı-içi', 'ücretsiz'],
      'JSON doğrulayıcı ve biçimlendirici; hatanın hangi satırda ve neden olduğunu söylüyor. '
      'Editör eklentisinden farkı bir şey kurmadan çalışması — API’den gelen bozuk yanıtı hızlıca '
      'incelemek için.',
      'A JSON validator and formatter that tells you which line failed and why. Against an editor '
      'plugin it needs nothing installed, which is what you want when checking a malformed API '
      'response in a hurry.',
      'araclar')
    a('https://www.yamllint.com/', 'YAMLlint', ['tarayıcı-içi', 'ücretsiz', 'devops'],
      'YAML doğrulayıcı; girinti ve tırnak hatalarını gösterip belgeyi ayrıştırılmış hâliyle '
      'basıyor. JSON doğrulayıcılardan farkı YAML’ın asıl tuzağını yakalaması — girintinin sessizce '
      'yanlış yapıyı üretmesi.',
      'A YAML validator that surfaces indentation and quoting errors and prints the parsed document '
      'back. Against a JSON validator it catches YAML’s actual trap: indentation that silently '
      'produces the wrong structure.',
      'devops')
    a('https://www.fromlatest.io/', 'FromLatest', ['docker', 'tarayıcı-içi', 'devops'],
      'Dockerfile’ı çözümleyip katman katman ne olduğunu açıklayan ve iyileştirme öneren araç. '
      'hadolint’ten farkı görsel olması ve her kuralın neden var olduğunu anlatması — Dockerfile '
      'yazmayı öğrenmek için de kullanılabiliyor.',
      'Analyses a Dockerfile, explains what happens layer by layer and suggests improvements. '
      'Against hadolint it is visual and states why each rule exists, which makes it usable for '
      'learning to write Dockerfiles rather than only linting them.',
      'devops')
    a('https://k8syaml.com/', 'K8s YAML Generator', ['devops', 'tarayıcı-içi', 'ücretsiz'],
      'Kubernetes manifestolarını form doldurarak üreten araç; her alanın ne işe yaradığını '
      'yanında açıklıyor. Belgelerden kopyalamaktan farkı geçerli bir manifesto ile çıkman ve '
      'alanların anlamını okuyarak öğrenmen.',
      'Generates Kubernetes manifests from a form, explaining each field beside it. Against copying '
      'from the docs you leave with a valid manifest and pick up what the fields mean on the way.',
      'devops')
    a('https://crontab-generator.org/', 'Crontab Generator', ['tarayıcı-içi', 'ücretsiz', 'devops'],
      'Cron ifadesini form üzerinden üreten ve ne zaman çalışacağını yazıyla söyleyen araç. '
      'crontab.guru’dan farkı ters yönde çalışması — ifadeyi çözmek yerine istediğin zamanlamadan '
      'ifade üretiyor.',
      'Builds a cron expression from a form and states in words when it will fire. Against '
      'crontab.guru it runs the other way: instead of decoding an expression, it produces one from '
      'the schedule you describe.',
      'devops')
    a('https://algorithm-visualizer.org/', 'Algorithm Visualizer',
      ['açık-kaynak', 'interaktif', 'algoritma'],
      'Algoritmanın kodunu yazarken adım adım görselleştiren platform; kendi kodunu da '
      'çalıştırabiliyorsun. Hazır animasyonlardan farkı bu — algoritmayı izlemekle kalmayıp '
      'değiştirip sonucu görebiliyorsun.',
      'A platform that visualises an algorithm step by step alongside its code, and runs code you '
      'write yourself. That is the difference from a canned animation: you can change the algorithm '
      'and watch what happens.',
      'ogrenme')

    # ============================================================ REGEX
    a('https://www.debuggex.com/', 'Debuggex', ['tarayıcı-içi', 'ücretsiz', 'referans'],
      'Düzenli ifadeyi durum diyagramına çeviren görsel test aracı; JavaScript, Python ve PCRE '
      'destekliyor. regex101’den farkı jeton listesi yerine akış şeması çizmesi — iç içe grupların '
      'yapısını görmek için daha okunaklı.',
      'A visual regex tester that draws the expression as a state diagram, covering JavaScript, '
      'Python and PCRE. Where regex101 lists tokens, this draws a flow chart, which reads better '
      'for nested groups.',
      'araclar')
    a('https://jex.im/regulex/', 'Regulex', ['açık-kaynak', 'tarayıcı-içi', 'ücretsiz'],
      'JavaScript düzenli ifadelerini demiryolu diyagramı olarak çizen araç. Debuggex’ten farkı '
      'tamamen istemci tarafında çalışması ve diyagramı SVG olarak dışa aktarabilmesi — belgeye '
      'koymak için elverişli.',
      'Draws JavaScript regular expressions as railroad diagrams. Against Debuggex it runs entirely '
      'client-side and exports the diagram as SVG, which makes it useful for documentation.',
      'araclar')

    # ============================================================ SECURITY & PRIVACY
    a('https://haveibeenpwned.com/', 'Have I Been Pwned', ['güvenlik', 'gizlilik', 'ücretsiz'],
      'E-posta adresinin ya da parolanın bilinen veri sızıntılarında geçip geçmediğini gösteren '
      'servis. Benzerlerinden farkı Troy Hunt’ın yürüttüğü şeffaf metodoloji ve parola sorgusunda '
      'k-anonimlik kullanması — parolanı sunucuya göndermiyorsun.',
      'Checks whether an email address or password appears in known breaches. What separates it is '
      'Troy Hunt’s transparent methodology and the k-anonymity scheme for password lookups — your '
      'password never reaches the server.',
      'guvenlik')
    a('https://coveryourtracks.eff.org/', 'Cover Your Tracks', ['gizlilik', 'güvenlik', 'ücretsiz'],
      'EFF’in tarayıcı parmak izi testi; tarayıcının ne kadar benzersiz göründüğünü ve izleyicilere '
      'karşı ne kadar korunduğunu ölçüyor. Basit "IP’m ne" sitelerinden farkı parmak izi '
      'entropisini hesaplaması — asıl takip yöntemi bu.',
      'The EFF’s browser fingerprinting test, measuring how unique your browser looks and how well '
      'it resists trackers. Unlike the "what is my IP" sites it computes fingerprint entropy, which '
      'is how tracking actually works now.',
      'guvenlik')
    a('https://ipleak.net/', 'IPLeak', ['gizlilik', 'ağ', 'ücretsiz'],
      'Bağlantının dışarıya ne sızdırdığını gösteren test: IP, DNS sunucuları, WebRTC yerel '
      'adresi, DNS sızıntısı. VPN kullanırken önemli olan da bu — VPN açıkken WebRTC gerçek IP’ni '
      'verebiliyor, burada görünüyor.',
      'Shows what your connection leaks: IP, DNS servers, WebRTC local addresses, DNS leakage. That '
      'is the test that matters with a VPN on — WebRTC can still hand over your real IP, and this '
      'is where you see it.',
      'guvenlik')
    a('https://www.security.org/how-secure-is-my-password/', 'How Secure Is My Password',
      ['güvenlik', 'ücretsiz', 'tarayıcı-içi'],
      'Bir parolanın kaba kuvvetle kırılma süresini tahmin edip gösteren araç; hesaplama tarayıcıda '
      'yapılıyor, parola gönderilmiyor. Parola gücü çubuklarından farkı somut bir süre vermesi — '
      'iki karakter eklemenin etkisi böyle anlaşılıyor.',
      'Estimates how long a password would take to brute-force, computed in the browser so the '
      'password is never sent. Against a strength meter it gives a concrete number, which is how '
      'you feel what adding two characters does.',
      'guvenlik')
    a('https://tineye.com/', 'TinEye', ['ücretsiz', 'osint'],
      'Ters görsel arama motoru; bir görselin internette nerede geçtiğini ve en eski sürümünü '
      'buluyor. Google Görseller’den farkı benzer değil aynı görseli araması — kaynağı bulmak ve '
      'sahte profili doğrulamak için daha isabetli.',
      'A reverse image search that finds where an image appears online and which copy is oldest. '
      'Against Google Images it looks for the same image rather than similar ones, which makes it '
      'better for finding a source or checking a fake profile.',
      'guvenlik')
    a('https://reports.exodus-privacy.eu.org/en/', 'Exodus Privacy', ['gizlilik', 'ücretsiz', 'referans'],
      'Android uygulamalarının içindeki izleyicileri ve istedikleri izinleri raporlayan servis. '
      'Play Store’un gizlilik etiketlerinden farkı beyana değil APK’nın kendisine bakması — '
      'geliştiricinin ne söylediği değil, ne koyduğu.',
      'Reports the trackers and permissions inside Android apps. Unlike Play Store privacy labels it '
      'reads the APK rather than the declaration — what the developer shipped, not what they said.',
      'mobil')
    a('https://adblock-tester.com/', 'AdBlock Tester', ['gizlilik', 'ücretsiz', 'tarayıcı-içi'],
      'Reklam engelleyicinin ne kadarını durdurduğunu ölçen test; reklam, izleyici, sosyal düğme ve '
      'çerez uyarısı ayrı ayrı puanlanıyor. "Çalışıyor mu" testlerinden farkı kategori bazında '
      'eksik gösterip hangi filtre listesinin gerektiğini söylemesi.',
      'Scores how much your ad blocker actually stops, broken out by ads, trackers, social buttons '
      'and cookie notices. Unlike a simple "is it working" check it shows the gaps by category, '
      'which tells you which filter list you are missing.',
      'guvenlik')
    a('https://backgroundchecks.org/justdeleteme/', 'JustDeleteMe', ['gizlilik', 'ücretsiz', 'referans'],
      'Servislerin hesap silme sayfalarına doğrudan bağlantı veren dizin; her biri zorluk '
      'derecesiyle işaretli. Kendi başına aramaktan farkı bu derecelendirme — hangi servisin '
      'silmeyi kasten zorlaştırdığını önceden görüyorsun.',
      'A directory of direct links to account deletion pages, each graded by difficulty. Against '
      'searching yourself, that grading is the point: you see in advance which services made '
      'deletion deliberately hard.',
      'guvenlik')
    a('https://www.accountkiller.com/en/home', 'AccountKiller', ['gizlilik', 'ücretsiz', 'referans'],
      'Hesap silme yönergelerini toplayan dizin; silme yolu olmayan servisler için hesabı '
      'kullanılamaz hâle getirme adımlarını da anlatıyor. JustDeleteMe’den farkı bu — silinemeyen '
      'hesap için bir plan B veriyor.',
      'A directory of account removal instructions that also covers how to neutralise an account '
      'where no deletion path exists. That is the difference from JustDeleteMe: a plan B for the '
      'accounts you cannot delete.',
      'guvenlik')
    a('https://degoogle.jmoore.dev/', 'DeGoogle', ['gizlilik', 'açık-kaynak', 'referans'],
      'Google ürünlerinin her biri için alternatif listesi; kategori kategori düzenlenmiş. Genel '
      '"alternatif" sitelerinden farkı tek bir sağlayıcıdan çıkışa odaklanması — hangi ürünün '
      'yerine ne konacağı sırayla işlenmiş.',
      'A list of alternatives for each Google product, organised category by category. Unlike '
      'general alternative-finder sites it is focused on leaving one provider, working through what '
      'replaces what in order.',
      'guvenlik')
    a('https://www.cryptologie.net/', 'Cryptologie', ['güvenlik', 'ücretsiz', 'akademik'],
      'Kriptograf David Wong’un uygulamalı kriptografi üzerine blogu ve not arşivi. Akademik '
      'makalelerden farkı protokolleri uygulayıcı gözüyle anlatması — teoremi değil, gerçek '
      'sistemlerde nerede yanlış kurulduğunu.',
      'Cryptographer David Wong’s blog and notes on applied cryptography. Against academic papers it '
      'explains protocols from an implementer’s seat — not the theorem, but where real systems get '
      'it wrong.',
      'guvenlik')
    a('https://owasp.org/www-community/Fuzzing', 'OWASP Fuzzing', ['güvenlik', 'referans', 'ücretsiz'],
      'Bulanık test (fuzzing) yöntemini OWASP’ın kendi topluluk sayfasından anlatan giriş: nasıl '
      'çalışır, hangi araçlar var, ne tür açıkları bulur. Araç belgelerinden farkı yöntemin '
      'kendisini tarafsız biçimde tanıtması.',
      'An introduction to fuzzing from OWASP’s own community pages: how it works, which tools exist, '
      'which classes of bug it finds. Against a tool’s own documentation it describes the method '
      'neutrally.',
      'guvenlik')
    a('https://github.com/secfigo/Awesome-Fuzzing', 'Awesome Fuzzing',
      ['awesome-liste', 'güvenlik', 'github'],
      'Bulanık test kaynaklarının derlemesi: araçlar, kitaplar, konuşmalar, akademik makaleler ve '
      'alıştırma ortamları. OWASP sayfasından farkı kapsam — yöntemi öğrendikten sonra derinleşmek '
      'için gidilecek yer.',
      'A compilation of fuzzing resources: tools, books, talks, papers and practice environments. '
      'Against the OWASP page the difference is breadth — this is where you go after you understand '
      'the method.',
      'guvenlik')
    a('https://www.securemessagingapps.com/', 'Secure Messaging Apps Comparison',
      ['güvenlik', 'gizlilik', 'referans'],
      'Mesajlaşma uygulamalarını şifreleme, meta veri, açık kaynaklık ve denetim durumu üzerinden '
      'karşılaştıran tablo. Blog karşılaştırmalarından farkı ölçütlerin sabit ve her uygulama için '
      'aynı olması — pazarlama iddiası değil, satır satır kontrol.',
      'A table comparing messaging apps on encryption, metadata, openness and audit status. Unlike a '
      'blog comparison the criteria are fixed and applied to every app alike — a row-by-row check '
      'rather than a marketing claim.',
      'guvenlik')

    # ============================================================ GIT & GITHUB
    a('https://ohshitgit.com/', 'Oh Shit, Git!?!', ['git', 'referans', 'ücretsiz'],
      'Git’te bir şeyi bozduğunda nasıl geri alacağını anlatan kısa rehber; her başlık gerçek bir '
      'panik anıyla açılıyor. Resmî belgelerden farkı komuttan değil durumdan başlaması — '
      '"yanlış dala commit attım" diye arıyorsun, `reflog` diye değil.',
      'A short guide to undoing whatever you just broke in Git, each entry opening on a real moment '
      'of panic. Against the official docs it starts from the situation rather than the command — '
      'you search "committed to the wrong branch", not `reflog`.',
      'referans')
    a('https://rogerdudler.github.io/git-guide/', 'Git — The Simple Guide',
      ['git', 'öğretici', 'ücretsiz'],
      'Git’in temel akışını tek sayfada anlatan giriş; dal, birleştirme ve uzak depo kadarı var. '
      'Pro Git kitabından farkı kapsamlı olmaya çalışmaması — ilk gün için gereken minimum.',
      'A one-page introduction to Git’s basic flow, going as far as branching, merging and remotes. '
      'Unlike the Pro Git book it makes no attempt at completeness — it is the minimum for day one.',
      'referans')
    a('https://gitsheet.wtf', 'GitSheet', ['git', 'kopya-kâğıdı', 'ücretsiz'],
      'Sık kullanılan Git komutlarının tek sayfalık kopya kâğıdı; kategori kategil düzenlenmiş. '
      'Uzun rehberlerden farkı arama değil tarama için tasarlanmış olması — komutu hatırlamaya '
      'çalışırken göz gezdiriyorsun.',
      'A single-page cheat sheet of common Git commands, grouped by task. Unlike a long guide it is '
      'built for scanning rather than searching — you glance at it while trying to recall a command.',
      'referans')
    a('https://gitexplorer.com/', 'Git Explorer', ['git', 'tarayıcı-içi', 'ücretsiz'],
      'Ne yapmak istediğini menüden seçince doğru Git komutunu üreten araç. Kopya kâğıdından farkı '
      'ters yönde çalışması — komutu hatırlamana gerek yok, niyetini seçiyorsun.',
      'Pick what you are trying to do from menus and it composes the right Git command. Against a '
      'cheat sheet it works backwards: you do not need to recall the command, only your intent.',
      'referans')
    a('https://anvaka.github.io/map-of-github/', 'Map of GitHub', ['github', 'interaktif', 'ücretsiz'],
      'GitHub depolarını yıldız benzerliğine göre kümeleyip harita gibi gezilebilir hâle getiren '
      'görselleştirme. Konuya göre aramadan farkı komşuluğu göstermesi — bir projeyi beğenenlerin '
      'başka neyi yıldızladığı topografya olarak çıkıyor.',
      'A visualisation clustering GitHub repositories by star similarity into a browsable map. '
      'Against topic search it shows adjacency: what else the people who starred one project '
      'starred, laid out as terrain.',
      'referans')
    a('https://relatedrepos.com/', 'Related Repos', ['github', 'ücretsiz', 'referans'],
      'Bir GitHub deposuna benzeyen projeleri bulan araç. GitHub’ın kendi "benzer depolar" '
      'önerisinden farkı yıldız örtüşmesine bakması — konu etiketi yanlış girilmiş projeleri de '
      'yakalıyor.',
      'Finds projects similar to a given GitHub repository. Against GitHub’s own suggestions it '
      'works from star overlap, so it also surfaces projects whose topic tags were filled in badly.',
      'referans')
    a('https://www.codetriage.com/', 'CodeTriage', ['açık-kaynak', 'github', 'ücretsiz'],
      'Açık kaynak projelere katkı vermek isteyenlere her gün bir açık issue gönderen servis. '
      '"good first issue" etiketini taramaktan farkı düzenli ve küçük dozda gelmesi — katkıyı '
      'alışkanlığa çeviren şey bu.',
      'Sends you one open issue a day from projects you follow, for people who want to contribute. '
      'Against scanning "good first issue" labels the difference is regularity and small doses — '
      'which is what turns contribution into a habit.',
      'referans')
    a('https://opensource.guide/', 'Open Source Guides', ['açık-kaynak', 'referans', 'ücretsiz'],
      'GitHub’ın açık kaynak rehberleri: proje başlatma, katkı alma, topluluk yönetme, tükenmişlikle '
      'başa çıkma. Lisans ya da araç rehberlerinden farkı sosyal tarafı ele alması — kodun değil, '
      'projenin sürdürülebilirliği.',
      'GitHub’s guides to open source: starting a project, taking contributions, running a '
      'community, handling burnout. Unlike licence or tooling guides it deals with the social side — '
      'the sustainability of the project rather than the code.',
      'referans')
    a('https://aosabook.org/en/index.html', 'The Architecture of Open Source Applications',
      ['kitap', 'açık-kaynak', 'ücretsiz'],
      'Açık kaynak projelerin mimarisini geliştiricilerinin kendi kalemiyle anlatan kitap serisi. '
      'Kaynak kodu okumaktan farkı hangi kararın neden alındığını ve neyin yanlış gittiğini '
      'öğrenmen — mimari kararların gerekçesi kodda yazmıyor.',
      'A book series in which the developers of open-source projects describe their own '
      'architecture. Against reading the source you learn which decisions were taken and why, and '
      'what went wrong — the rationale is never in the code.',
      'referans')
    a('https://oss.gallery/', 'OSS Gallery', ['açık-kaynak', 'ücretsiz', 'referans'],
      'Açık kaynak projelerin topluluk tarafından derlenen vitrini; her kayıt canlı demo ve depo '
      'bağlantısıyla. Awesome listelerinden farkı görsel olması — ne yaptığını okumadan önce '
      'görüyorsun.',
      'A crowdsourced showcase of open-source projects, each with a live demo and repository link. '
      'Against awesome lists it is visual — you see what a thing does before reading about it.',
      'referans')
    a('https://www.libhunt.com/', 'LibHunt', ['açık-kaynak', 'referans', 'ücretsiz'],
      'Kütüphaneleri karşılaştıran ve alternatiflerini gösteren dizin; etkinlik ve popülerlik '
      'eğilimini birlikte veriyor. Awesome listelerinden farkı verinin güncel olması — proje '
      'yavaşladığında grafikte görünüyor.',
      'A directory that compares libraries and shows their alternatives, with activity and '
      'popularity trends side by side. Against awesome lists the data is live — when a project '
      'slows down, the graph says so.',
      'referans')

    # ============================================================ VIM & EDITORS
    a('https://vim.rtorr.com/', 'Vim Cheat Sheet', ['kopya-kâğıdı', 'cli', 'ücretsiz'],
      'Vim komutlarının kategorilere ayrılmış tek sayfalık listesi; on kadar dile çevrilmiş. '
      '`vimtutor`dan farkı öğretmemesi, hatırlatması — Vim kullanmaya başladıktan sonraki ay '
      'açık tuttuğun sekme.',
      'A one-page list of Vim commands grouped by category, translated into a dozen languages. '
      'Unlike `vimtutor` it does not teach, it reminds — the tab you keep open during your second '
      'month of Vim.',
      'referans')
    a('https://learnvim.irian.to/', 'Learn Vim', ['kitap', 'cli', 'ücretsiz'],
      'Vim’i tuş dizisi ezberleterek değil, dilbilgisi olarak öğreten çevrimiçi kitap: eylem + '
      'hareket + metin nesnesi. Kopya kâğıtlarından farkı bu — komutları ezberlemek yerine yeni '
      'kombinasyonlar türetmeyi öğreniyorsun.',
      'An online book that teaches Vim as a grammar — verb plus motion plus text object — rather '
      'than as key sequences to memorise. That is the break from cheat sheets: you learn to derive '
      'new combinations instead of recalling old ones.',
      'referans')
    a('https://vimawesome.com/', 'Vim Awesome', ['referans', 'cli', 'ücretsiz'],
      'Vim ve Neovim eklentilerinin dizini; popülerlik, kategori ve kurulum yöntemine göre '
      'süzülüyor. GitHub aramasından farkı eklentilerin bakım durumunu ve kurulum satırını hazır '
      'vermesi.',
      'A directory of Vim and Neovim plugins, filterable by popularity, category and install '
      'method. Against searching GitHub it surfaces maintenance status and hands you the install '
      'line.',
      'referans')
    a('https://theia-ide.org/', 'Eclipse Theia', ['açık-kaynak', 'masaüstü', 'sunucu'],
      'Masaüstünde ve tarayıcıda çalışan, VS Code eklentileriyle uyumlu IDE çatısı. VS Code’dan '
      'farkı ürün değil çatı olması — kendi markanla, kendi eklenti setinle bir IDE inşa etmen '
      'için tasarlanmış.',
      'An IDE framework that runs on the desktop and in the browser and takes VS Code extensions. '
      'The difference from VS Code is that it is a framework rather than a product — built for you '
      'to construct your own IDE on top of.',
      'araclar')
    a('https://vscodethemes.com/', 'VS Code Themes', ['referans', 'ücretsiz', 'tarayıcı-içi'],
      'VS Code temalarını gerçek kod üzerinde önizleyen galeri. Marketplace’ten farkı temayı '
      'kurmadan görmen — birkaç dilde aynı anda nasıl göründüğünü karşılaştırabiliyorsun.',
      'A gallery previewing VS Code themes on real code. Against the marketplace you see a theme '
      'without installing it, and can compare how it looks across several languages at once.',
      'araclar')

    # ============================================================ HARDWARE & ELECTRONICS
    a('https://wokwi.com/', 'Wokwi', ['tarayıcı-içi', 'gömülü', 'donanım'],
      'Arduino, ESP32 ve STM32’yi tarayıcıda simüle eden ortam; sensör ve ekran gibi çevre '
      'birimleri de sanal. Gerçek donanımdan farkı kart beklemeden çalışabilmen — kodun mantığını '
      'lehim yapmadan doğruluyorsun.',
      'Simulates Arduino, ESP32 and STM32 in the browser, with virtual sensors and displays '
      'attached. Against real hardware you start without waiting for a board — the logic gets '
      'verified before anything is soldered.',
      'donanim')
    a('https://www.falstad.com/circuit/', 'Falstad Circuit Simulator',
      ['interaktif', 'donanım', 'ücretsiz'],
      'Devreyi çizip akımın akışını canlandırmalı gösteren simülatör; gerilim ve akım renkle '
      'ilerliyor. SPICE’tan farkı sayısal doğruluk değil sezgi hedeflemesi — devrenin nasıl '
      'çalıştığını görmek için.',
      'A simulator that animates current flowing through a circuit you draw, with voltage and '
      'current shown in colour. Against SPICE it aims at intuition rather than numerical accuracy — '
      'it is for seeing how a circuit works.',
      'donanim')
    a('https://everycircuit.com/', 'EveryCircuit', ['interaktif', 'donanım', 'freemium'],
      'Devre simülasyonunu gerçek zamanlı animasyonla gösteren araç; mobilde de çalışıyor. '
      'Falstad’dan farkı dokunmatik arayüz ve bileşen değerlerini kaydırarak değiştirip sonucu '
      'anlık görebilmen.',
      'Circuit simulation with real-time animation, working on mobile as well. Against Falstad it '
      'offers a touch interface and lets you drag component values and watch the result change '
      'immediately.',
      'donanim')
    a('https://octopart.com/', 'Octopart', ['donanım', 'referans', 'ücretsiz'],
      'Elektronik bileşen arama motoru; distribütörlerdeki stok ve fiyatı tek sayfada '
      'karşılaştırıyor. Digi-Key veya Mouser’a tek tek bakmaktan farkı bu — parça tedarik '
      'edilebilirliğini tasarım aşamasında görüyorsun.',
      'A search engine for electronic components that compares stock and price across distributors '
      'on one page. That is what saves you checking Digi-Key and Mouser separately — you see '
      'availability while still designing.',
      'donanim')
    a('https://www.digikey.com/', 'Digi-Key', ['donanım', 'referans'],
      'Elektronik bileşen dağıtıcısı; katalog, veri sayfaları ve parametrik arama çok güçlü. '
      'Diğer dağıtıcılardan farkı stok derinliği ve tek adet satış — prototip için bir parça '
      'almak sorun değil.',
      'An electronics component distributor with a strong catalogue, datasheets and parametric '
      'search. Against other distributors it wins on stock depth and single-unit sales — buying one '
      'part for a prototype is unremarkable here.',
      'donanim')
    a('https://www.opencircuitsbook.com/', 'Open Circuits', ['kitap', 'donanım'],
      'Elektronik bileşenlerin kesitlerini yüksek çözünürlükte fotoğraflayan kitap; direncin, '
      'kondansatörün, konnektörün içi görünüyor. Veri sayfalarından farkı bileşenin nasıl '
      'yapıldığını göstermesi — soyut sembol somut nesneye dönüşüyor.',
      'A book of high-resolution cross-sections of electronic components, showing the insides of '
      'resistors, capacitors and connectors. Against datasheets it shows how a component is made — '
      'the abstract symbol becomes a physical object.',
      'donanim')
    a('https://www.fpga4fun.com/', 'FPGA4Fun', ['öğretici', 'donanım', 'gömülü'],
      'FPGA’ya donanım tanımlama dilleriyle giriş yapan projeler; her biri çalışan bir devre '
      'üretiyor. Üniversite derslerinden farkı doğrudan projeden başlaması — teoriden önce '
      'çalışan bir şey.',
      'Projects that introduce FPGAs through hardware description languages, each producing a '
      'working circuit. Unlike a university course it starts from the project — something that '
      'works before any theory.',
      'donanim')
    a('https://c9x.me/x86/', 'x86 Instruction Set Reference', ['referans', 'gömülü', 'ücretsiz'],
      'x86 komut kümesinin aranabilir referansı; her komut için kodlama, bayraklar ve sözde kod. '
      'Intel’in PDF kılavuzlarından farkı hızlı olması — bir komutu doğrulamak için 5000 sayfalık '
      'PDF açmıyorsun.',
      'A searchable reference for the x86 instruction set with encoding, flags and pseudocode per '
      'instruction. Against Intel’s PDF manuals it is simply fast — you no longer open a '
      '5,000-page document to check one opcode.',
      'referans')
    a('https://www.h-schmidt.net/FloatConverter/IEEE754.html', 'IEEE-754 Converter',
      ['tarayıcı-içi', 'referans', 'ücretsiz'],
      'Ondalık sayı ile IEEE-754 kayan nokta gösterimi arasında iki yönlü dönüştürücü; bitleri tek '
      'tek çevirebiliyorsun. Hesap makinesinden farkı yuvarlama hatasının nereden geldiğini '
      'göstermesi — 0.1 + 0.2 sorusunun cevabı burada görünüyor.',
      'A two-way converter between decimal and IEEE-754 floating point, with individual bits '
      'toggleable. Against a calculator it shows where the rounding error comes from — this is '
      'where the 0.1 + 0.2 question is actually answered.',
      'referans')
    a('https://pcpartpicker.com/list/', 'PCPartPicker', ['donanım', 'ücretsiz', 'referans'],
      'Bilgisayar toplarken parçaların uyumluluğunu denetleyen ve fiyat karşılaştıran araç. '
      'Elle liste yapmaktan farkı uyumsuzluğu önceden yakalaması — güç kaynağı yetmiyorsa ya da '
      'soğutucu kasaya sığmıyorsa uyarıyor.',
      'Checks part compatibility and compares prices while you plan a PC build. Against a manual '
      'list it catches the mismatch in advance — an underpowered PSU or a cooler that will not '
      'clear the case.',
      'donanim')
    a('https://pc-builds.com/', 'PC-Builds', ['donanım', 'ücretsiz', 'referans'],
      'Bilgisayar toplama ve darboğaz hesaplama araçları; işlemci-ekran kartı dengesini oyun ve '
      'çözünürlük bazında tahmin ediyor. PCPartPicker’dan farkı uyumluluk değil performans dengesi '
      'sorusuna cevap vermesi.',
      'PC building tools with a bottleneck calculator that estimates CPU-to-GPU balance per game '
      'and resolution. Where PCPartPicker answers compatibility, this answers whether the balance '
      'makes sense.',
      'donanim')

    # ============================================================ MOBILE
    a('https://fossdroid.com/', 'Fossdroid', ['açık-kaynak', 'ücretsiz', 'gizlilik'],
      'F-Droid deposundaki özgür yazılım Android uygulamalarını gezilebilir hâlde sunan vitrin. '
      'F-Droid istemcisinden farkı web üzerinden popülerliğe göre keşif — hangi uygulamanın '
      'gerçekten kullanıldığını görüyorsun.',
      'A browsable showcase of the free-software Android apps in the F-Droid repository. Against '
      'the F-Droid client it offers discovery by popularity on the web — you can see which apps are '
      'actually used.',
      'mobil')
    a('https://apt.izzysoft.de/fdroid/index.php', 'IzzyOnDroid', ['açık-kaynak', 'gizlilik', 'ücretsiz'],
      'F-Droid’e ek depo; kaynağı açık olduğu hâlde resmî depoya girmemiş uygulamaları barındırıyor '
      've her birine gizlilik denetimi uyguluyor. Resmî depodan farkı daha hızlı güncelleme ve '
      'izleyici raporu.',
      'An additional F-Droid repository carrying apps that are open source but not in the official '
      'repo, each run through a privacy audit. Against the official repository it updates faster '
      'and publishes a tracker report.',
      'mobil')
    a('https://dontkillmyapp.com/', "Don't Kill My App", ['referans', 'ücretsiz', 'mobil'],
      'Android üreticilerinin arka plan uygulamalarını nasıl öldürdüğünü marka marka belgeleyen '
      'site; her cihaz için çözüm adımları var. Genel Android belgelerinden farkı üretici bazında '
      'olması — alarm uygulamasının neden çalmadığının cevabı burada.',
      'Documents how each Android manufacturer kills background apps, brand by brand, with the '
      'workaround for each device. Unlike general Android documentation it is per-vendor — which is '
      'where the answer to "why did my alarm not ring" lives.',
      'mobil')
    a('https://androidweekly.net/', 'Android Weekly', ['ücretsiz', 'referans'],
      'Android ve Kotlin geliştirme haberlerini haftalık derleyen bülten: makaleler, kütüphaneler, '
      'iş ilanları. Blog takip etmekten farkı seçilmiş olması — haftada bir e-posta, dağınık '
      'kaynak takibi yerine.',
      'A weekly newsletter of Android and Kotlin development news: articles, libraries, jobs. '
      'Against following blogs it is curated — one email a week instead of chasing scattered feeds.',
      'mobil')

    # ============================================================ DATA & ACADEMIA
    a('https://dblp.org/', 'DBLP', ['akademik', 'referans', 'ücretsiz'],
      'Bilgisayar bilimi yayınlarının açık bibliyografya veritabanı; yazar sayfaları ve konferans '
      'ciltleri düzenli. Google Scholar’dan farkı temiz ve elle bakımlı olması — yazar '
      'karışıklığı ve hayalet kayıt neredeyse yok.',
      'The open bibliography database of computer science publications, with tidy author pages and '
      'conference volumes. Against Google Scholar it is clean and hand-maintained — author '
      'ambiguity and phantom records are rare.',
      'referans')
    a('https://academictorrents.com/', 'Academic Torrents', ['akademik', 'veri-bilimi', 'ücretsiz'],
      'Büyük araştırma veri kümelerini BitTorrent üzerinden dağıtan topluluk arşivi. Kurumsal '
      'indirme bağlantılarından farkı dayanıklılığı — üniversite sunucusu kapansa bile veri '
      'tohumlayıcılarda yaşamaya devam ediyor.',
      'A community archive distributing large research datasets over BitTorrent. Against '
      'institutional download links the difference is durability: when the university server goes '
      'away, the data survives in the swarm.',
      'veri')
    a('https://www.datasetlist.com/', 'Dataset List', ['veri-bilimi', 'referans', 'ücretsiz'],
      'Makine öğrenmesi veri kümelerini alana göre listeleyen dizin; boyut, lisans ve makale '
      'bağlantısı ile. Kaggle’dan farkı yarışma değil akademik ve endüstriyel kümeler olması — '
      'gerçek dünya verisi arayanlar için.',
      'A directory of machine learning datasets by domain, with size, licence and paper links. '
      'Against Kaggle these are academic and industrial sets rather than competition data — for '
      'when you need something real.',
      'veri')
    a('https://www.image-net.org/', 'ImageNet', ['veri-bilimi', 'akademik', 'ücretsiz'],
      'WordNet hiyerarşisine göre etiketlenmiş, on dört milyon görsellik veri kümesi. Diğer '
      'görüntü kümelerinden farkı tarihsel ağırlığı — 2012’deki derin öğrenme sıçraması bu küme '
      'üzerindeki yarışmadan çıktı, hâlâ ölçüt olarak kullanılıyor.',
      'A dataset of fourteen million images labelled against the WordNet hierarchy. What sets it '
      'apart from other image sets is historical weight: the 2012 deep learning breakthrough came '
      'out of the competition on it, and it is still a benchmark.',
      'veri')

    # ============================================================ QUANTUM
    a('https://quantumflytrap.com/', 'Quantum Flytrap', ['kuantum', 'interaktif', 'ücretsiz'],
      'Optik kuantum deneylerini sürükle bırak ile kurup çalıştıran sanal laboratuvar; foton, '
      'polarizör ve ışın bölücülerle. Devre simülatörlerinden farkı kübit soyutlamasıyla değil '
      'fiziksel deney düzeneğiyle çalışması.',
      'A virtual lab where you assemble and run optical quantum experiments by dragging photons, '
      'polarisers and beam splitters. Unlike circuit simulators it works at the level of the '
      'physical apparatus rather than the qubit abstraction.',
      'kuantum')
    a('https://qplaylearn.com', 'QPlayLearn', ['kuantum', 'öğretici', 'ücretsiz'],
      'Kuantum kavramlarını üç ayrı derinlikte anlatan eğitim projesi: oyun, animasyon ve teknik '
      'açıklama. Tek seviyeli kaynaklardan farkı bu katmanlı yapı — aynı kavramı çocuğa da '
      'lisans öğrencisine de anlatabiliyor.',
      'An education project explaining quantum concepts at three separate depths: game, animation '
      'and technical account. Unlike single-level resources that layering lets the same concept '
      'reach a child and an undergraduate.',
      'kuantum')
    a('https://www.vqol.org/', 'Virtual Quantum Optics Laboratory',
      ['kuantum', 'interaktif', 'akademik'],
      'Kuantum optik deneylerini tasarlayıp simüle eden tarayıcı tabanlı laboratuvar. Quantum '
      'Flytrap’tan farkı oyunlaştırma yerine araştırma düzeyinde doğruluk hedeflemesi — ders '
      'laboratuvarı yerine geçebiliyor.',
      'A browser-based laboratory for designing and simulating quantum optics experiments. Against '
      'Quantum Flytrap it aims at research-grade accuracy rather than gamification, enough to stand '
      'in for a teaching lab.',
      'kuantum')

    # ============================================================ REFERENCE & CHEAT SHEETS
    a('https://cheatography.com/', 'Cheatography', ['kopya-kâğıdı', 'referans', 'ücretsiz'],
      'Kullanıcıların hazırladığı kopya kâğıdı arşivi; her biri PDF olarak basılabiliyor. Tek '
      'konuya adanmış kopya kâğıtlarından farkı kapsamı — programlama dilinden klavye kısayoluna '
      'kadar aynı biçimde.',
      'An archive of user-made cheat sheets, each printable as a PDF. Against single-subject cheat '
      'sheets the difference is coverage — everything from a programming language to an '
      'application’s shortcuts in the same format.',
      'referans')
    a('https://www.cheat-sheets.org/', 'Cheat-Sheets.org', ['kopya-kâğıdı', 'referans', 'ücretsiz'],
      'İnternete dağılmış kopya kâğıtlarını konuya göre toplayan dizin. Cheatography’den farkı '
      'kendi içerik üretmemesi — başka sitelerdeki iyi kâğıtlara işaret ediyor, tek merkez değil '
      'katalog.',
      'A directory collecting cheat sheets scattered across the web, filed by subject. Unlike '
      'Cheatography it produces nothing itself — it points at the good sheets elsewhere, a '
      'catalogue rather than a source.',
      'referans')
    a('https://lecoupa.github.io/awesome-cheatsheets/', 'Awesome Cheatsheets',
      ['kopya-kâğıdı', 'awesome-liste', 'github'],
      'Programlama dilleri, çatılar ve komut satırı araçları için tek dosyada yoğunlaştırılmış '
      'kopya kâğıtları. Görsel kâğıtlardan farkı düz metin olması — aranabiliyor, kopyalanabiliyor '
      've depoda sürümleniyor.',
      'Cheat sheets for languages, frameworks and command-line tools, each condensed into a single '
      'file. Unlike visual sheets these are plain text — searchable, copyable and versioned in a '
      'repository.',
      'referans')
    a('https://www.sans.org/blog/the-ultimate-list-of-sans-cheat-sheets/', 'SANS Cheat Sheets',
      ['kopya-kâğıdı', 'güvenlik', 'ücretsiz'],
      'SANS Enstitüsü’nün güvenlik kopya kâğıtları: adli bilişim, olay müdahalesi, bellek analizi, '
      'Windows kayıt defteri. Genel kopya kâğıtlarından farkı olay anında kullanılmak üzere '
      'tasarlanmış olması — hangi komutun ne kanıt ürettiği yazılı.',
      'The SANS Institute’s security cheat sheets: forensics, incident response, memory analysis, '
      'the Windows registry. Unlike general cheat sheets these are built for use during an '
      'incident — which command yields which evidence.',
      'guvenlik')
    a('https://www.pythoncheatsheet.org/', 'Python Cheatsheet', ['kopya-kâğıdı', 'python', 'ücretsiz'],
      '"Automate the Boring Stuff" kitabına dayanan Python referansı; temel söz diziminden standart '
      'kütüphaneye. Resmî belgelerden farkı örnek ağırlıklı olması — sözdizimini hatırlamak için '
      'açılıyor, öğrenmek için değil.',
      'A Python reference based on "Automate the Boring Stuff", covering syntax through the standard '
      'library. Against the official documentation it leans on examples — you open it to recall '
      'syntax, not to learn it.',
      'referans')
    a('https://speedsheet.io/', 'Speedsheet', ['referans', 'python', 'interaktif'],
      'Aramaya göre daralan etkileşimli Python referansı; yazdıkça ilgili bölüm açılıyor. Statik '
      'kopya kâğıtlarından farkı bu — sayfada göz gezdirmek yerine aradığını yazıyorsun.',
      'An interactive Python reference that narrows as you search, opening the relevant section as '
      'you type. That is the break from a static cheat sheet: you type what you need rather than '
      'scanning a page.',
      'referans')
    a('https://sankeydiagram.net/', 'SankeyDiagram.net', ['açık-kaynak', 'tarayıcı-içi', 'ücretsiz'],
      'Metin girdisinden Sankey akış diyagramı üreten araç; enerji, bütçe ya da dönüşüm hunisi '
      'akışları için. Genel diyagram araçlarından farkı tek bir grafik türüne odaklanması ve '
      'girdiyi grafik değil metin olarak alması.',
      'Generates Sankey flow diagrams from text input, for energy, budget or funnel flows. Unlike '
      'general diagram tools it does one chart type, and takes its input as text rather than as '
      'drawing.',
      'araclar')
    a('https://www.diffchecker.com/', 'Diffchecker', ['tarayıcı-içi', 'ücretsiz', 'referans'],
      'Metin, görsel, PDF ve klasör karşılaştıran fark aracı. `diff` komutundan farkı biçimlendirme '
      've görsel karşılaştırma yapabilmesi — iki PDF sözleşme arasındaki farkı bulmak için komut '
      'satırı yetmiyor.',
      'A diff tool for text, images, PDFs and folders. Against the `diff` command it handles '
      'formatted and visual comparison — the command line will not tell you what changed between '
      'two PDF contracts.',
      'araclar')
    a('https://www.codingfont.com/', 'CodingFont', ['interaktif', 'ücretsiz'],
      'Kodlama fontlarını turnuva usulü ikişer ikişer karşılaştırıp sana en uygun olanı buldurmayı '
      'amaçlayan araç. Font listelerinden farkı seçimi karara indirgemesi — yirmi fontu yan yana '
      'koymuyor, ikisini seçtiriyor.',
      'Compares coding fonts two at a time in a tournament until one wins. Unlike a font list it '
      'turns browsing into a decision — it never puts twenty fonts side by side, only two.',
      'araclar')
    a('https://techspecs.io/', 'TechSpecs', ['donanım', 'referans', 'ücretsiz'],
      'Tüketici elektroniği ürünlerinin teknik özelliklerini arayan ve karşılaştıran motor. '
      'Üretici sayfalarından farkı normalize edilmiş veri sunması — iki markanın farklı adlarla '
      'yazdığı aynı özelliği yan yana koyabiliyorsun.',
      'A search engine for the specifications of consumer electronics, with comparison. Against '
      'manufacturer pages the data is normalised, so the same property written under two different '
      'names by two brands lines up.',
      'donanim')
    a('https://www.rtings.com/', 'RTINGS', ['donanım', 'referans', 'ücretsiz'],
      'Televizyon, kulaklık, monitör ve fare gibi cihazları laboratuvar ölçümleriyle inceleyen '
      'site; metodoloji ve ham veri açık. Kanaat yazılarından farkı ölçülebilir olması — '
      'kullanımına göre ağırlıklandırılmış puanı kendin ayarlıyorsun.',
      'Reviews TVs, headphones, monitors and mice through laboratory measurements, with methodology '
      'and raw data published. Unlike opinion reviews the results are measurable, and you can '
      'reweight the score for your own use.',
      'donanim')

    # ============================================================ LICENSING & MISC
    a('https://shields.io/', 'Shields.io', ['açık-kaynak', 'github', 'ücretsiz'],
      'README rozetleri üreten servis: derleme durumu, sürüm, indirme sayısı, lisans. Elle SVG '
      'hazırlamaktan farkı canlı veriye bağlanabilmesi — rozet npm sürümünü ya da CI durumunu '
      'kendisi çekiyor.',
      'Generates README badges: build status, version, downloads, licence. Against hand-made SVGs '
      'they bind to live data — the badge fetches the npm version or CI status itself.',
      'referans')
    a('https://choosealicense.com/appendix/', 'Choose a License — Appendix',
      ['açık-kaynak', 'referans', 'ücretsiz'],
      'Açık kaynak lisanslarını izin, koşul ve sınırlama sütunlarıyla tek tabloda karşılaştıran '
      'ek. Lisans metinlerini okumaktan farkı bu — patent hükmü var mı, aynı lisansla paylaşma '
      'zorunlu mu, satırdan görüyorsun.',
      'An appendix comparing open-source licences in one table of permissions, conditions and '
      'limitations. Against reading licence texts you see it in a row — whether there is a patent '
      'clause, whether share-alike applies.',
      'referans')
    a('https://ufal.github.io/public-license-selector/', 'Public License Selector',
      ['açık-kaynak', 'referans', 'ücretsiz'],
      'Sorulara verdiğin cevaplara göre uygun lisansı öneren araç; yazılım, veri ve içerik için '
      'ayrı akışlar var. choosealicense.com’dan farkı veri kümesi ve içerik lisanslarını da '
      'kapsaması — CC lisansları arasında seçim yapmak için.',
      'Recommends a licence from your answers to a series of questions, with separate flows for '
      'software, data and content. Against choosealicense.com it also covers datasets and content, '
      'which is what you need when choosing among the CC licences.',
      'referans')
    a('https://nocodelist.co/', 'No Code List', ['referans', 'otomasyon', 'ücretsiz'],
      'Üç yüzden fazla kod yazmadan iş yapan aracın kategorilere ayrılmış dizini. Ürün avı '
      'sitelerinden farkı yeni olanı değil kategoriyi tam kapsamayı hedeflemesi — bir kategoride '
      'ne varsa listeleniyor.',
      'A categorised directory of over three hundred tools for getting things done without code. '
      'Unlike product-hunt style sites it aims at covering a category rather than surfacing the '
      'newest thing.',
      'araclar')
    a('https://lookup.icann.org/en', 'ICANN Lookup', ['referans', 'ağ', 'ücretsiz'],
      'Alan adı kayıt bilgilerini ICANN’in kendi arayüzünden sorgulama. Üçüncü parti WHOIS '
      'sitelerinden farkı reklam ve satış teklifi olmaması — sorguladığın alan adı için ertesi gün '
      'e-posta almıyorsun.',
      'Domain registration lookup through ICANN’s own interface. Against third-party WHOIS sites '
      'there are no ads and no sales pitch — you do not get an email the next day about the domain '
      'you looked up.',
      'ag')
