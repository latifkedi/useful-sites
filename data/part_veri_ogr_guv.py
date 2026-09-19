# -*- coding: utf-8 -*-
"""Veri Bilimi + Öğrenme + Güvenlik — çeşitli listelerden.

Üç mevcut alana toplu ekleme: veri bilimi awesome listeleri, oyunla öğrenme
siteleri ve güvenlik awesome listeleri + kasıtlı-zafiyetli pratik uygulamaları
(Test kovasından buraya taşındı — bunlar güvenlik hedefi).
"""

AL = 'awesomelist'
DS = 'dsbest'
AP = 'awesomeproj'
TS = 'testsites'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, cat, src):
        add(url, name, tags, tr, en, cat, src)

    # ============================================================ VERİ BİLİMİ
    a('https://github.com/awesomedata/awesome-public-datasets', 'Awesome Public Datasets',
      ['awesome-liste', 'github', 'veri-bilimi', 'ücretsiz'],
      'Herkese açık, konu konu düzenlenmiş veri kümelerinin listesi. Rastgele veri aramaktan farkı '
      'temiz, kullanılabilir ve alanına göre gruplanmış kaynaklara götürmesi.',
      'A list of public datasets organised by topic. Unlike random data search it points to clean, '
      'usable sources grouped by domain.', 'veri', AL),
    a('https://github.com/ChristosChristofidis/awesome-deep-learning', 'Awesome Deep Learning',
      ['awesome-liste', 'github', 'veri-bilimi'],
      'Derin öğrenme için ders, makale, çerçeve ve veri kümesi listesi. Genel ML listelerinden farkı '
      'sinir ağlarına ve modern mimarilere odaklanması.',
      'A list of courses, papers, frameworks and datasets for deep learning. Unlike general ML lists it '
      'focuses on neural networks and modern architectures.', 'veri', AL),
    a('https://github.com/krzjoa/awesome-python-data-science', 'Awesome Python Data Science',
      ['awesome-liste', 'github', 'python', 'veri-bilimi'],
      'Python veri bilimi kütüphanelerini iş akışına göre (veri, model, görselleştirme) düzenleyen liste. '
      'PyPI aramasından farkı her aşama için seçilmiş araçları göstermesi.',
      'A list organising Python data-science libraries by workflow (data, models, visualisation). Unlike '
      'a PyPI search it shows curated tools for each stage.', 'veri', AL),
    a('https://github.com/SE-ML/awesome-seml', 'Awesome SE for ML', ['awesome-liste', 'github', 'veri-bilimi'],
      'Deneyden üretime makine öğrenmesi mühendisliği kaynakları. Model listelerinden farkı test, '
      'dağıtım ve izleme gibi “ML’i ürün yapma” tarafına bakması.',
      'Resources for machine-learning engineering from experiment to production. Unlike model lists it '
      'looks at the “making ML a product” side — testing, deployment, monitoring.', 'veri', AL),
    a('https://paperswithcode.com/', 'Papers with Code', ['veri-bilimi', 'akademik', 'ücretsiz'],
      'Makine öğrenmesi makalelerini uygulama koduyla ve karşılaştırma tablolarıyla eşleştiren site. '
      'Salt makaleden farkı sonucun kodunu ve en iyi yöntem sıralamasını yanına koyması.',
      'A site pairing machine-learning papers with their implementation code and benchmark tables. '
      'Unlike a paper alone it puts the result’s code and the leaderboard beside it.', 'veri', K),

    # ============================================================ ÖĞRENME (oyunla + platform)
    a('http://www.flexboxdefense.com/', 'Flexbox Defense', ['interaktif', 'ücretsiz', 'frontend'],
      'Kule savunması oyunu üzerinden CSS Flexbox öğreten site. Dokümandan farkı her hizalama '
      'özelliğini bir oyun hamlesiyle ezberletmesi.',
      'A site teaching CSS Flexbox through a tower-defence game. Unlike the docs it fixes each alignment '
      'property with a game move.', 'ogrenme', AP),
    a('https://flukeout.github.io/', 'CSS Diner', ['interaktif', 'ücretsiz', 'frontend'],
      'CSS seçicilerini bir masa üzerindeki yemekleri seçerek öğreten oyun. Kuru alıştırmadan farkı '
      'seçici sözdizimini görsel ve eğlenceli bir bulmacaya çevirmesi.',
      'A game teaching CSS selectors by picking dishes on a table. Unlike dry drills it turns selector '
      'syntax into a visual, fun puzzle.', 'ogrenme', AP),
    a('https://silentteacher.toxicode.fr/', 'Silent Teacher', ['interaktif', 'ücretsiz'],
      'Tek kelime açıklama olmadan, deneme-yanılmayla programlamanın temellerini sezdiren oyun. Ders '
      'anlatımından farkı kuralı sana kendin keşfettirmesi.',
      'A game that teaches the basics of programming by trial and error, with no word of explanation. '
      'Unlike a lecture it has you discover the rule yourself.', 'ogrenme', AP),
    a('https://www.sololearn.com/', 'SoloLearn', ['ücretsiz', 'interaktif', 'müfredat'],
      'Programlamayı mobilde, küçük dersler ve topluluk üzerinden öğreten platform. Uzun kurslardan '
      'farkı otobüste bile ilerlenebilen, ısırıklık yapılı olması.',
      'A platform teaching programming on mobile through small lessons and community. Unlike long courses '
      'it is bite-sized enough to progress even on the bus.', 'ogrenme', AP),
    a('https://techguide.sh/', 'TechGuide', ['ogrenme', 'ücretsiz', 'referans'],
      'Yazılımın farklı kariyer patikalarını (frontend, veri, mobil) görsel yol haritası olarak veren '
      'site. Tek kaynaktan farkı bir role hangi sırayla ne öğrenileceğini haritalaması.',
      'A site giving software’s different career paths (frontend, data, mobile) as visual roadmaps. '
      'Unlike a single resource it maps what to learn in which order for a role.', 'ogrenme', AP),
    a('https://learntocodewith.me/', 'Learn to Code With Me', ['ogrenme', 'ücretsiz', 'referans'],
      'Kendi kendine kod öğrenenler için yol, araç ve kariyer tavsiyesi toplayan kaynak. Tek konuya '
      'odaklı sitelerden farkı “nereden başlamalı ve işe nasıl dönüştürmeli” sorusuna eğilmesi.',
      'A resource gathering paths, tools and career advice for self-taught coders. Unlike single-topic '
      'sites it addresses “where to start and how to turn it into a job”.', 'ogrenme', AP),

    # ============================================================ GÜVENLİK
    a('https://portswigger.net/web-security', 'Web Security Academy', ['güvenlik', 'öğretici', 'ücretsiz', 'interaktif'],
      'PortSwigger’ın ücretsiz, uygulamalı web güvenliği kursu — her zafiyet için canlı laboratuvar. '
      'Teorik kurslardan farkı saldırıyı gerçek bir hedefte denetmesi.',
      'PortSwigger’s free, hands-on web-security course — a live lab for each vulnerability. Unlike '
      'theory courses it has you perform the attack on a real target.', 'guvenlik', K),
    a('https://ctftime.org/', 'CTFtime', ['güvenlik', 'pratik', 'ücretsiz'],
      'Dünyadaki Capture The Flag yarışmalarını takvimleyen ve takım sıralaması tutan site. Dağınık '
      'duyurulardan farkı hangi yarışmanın ne zaman olduğunu tek yerde toplaması.',
      'A site scheduling Capture The Flag competitions worldwide and keeping team rankings. Unlike '
      'scattered announcements it gathers which contest is when in one place.', 'guvenlik', K),
    a('https://www.bugcrowd.com/', 'Bugcrowd', ['güvenlik', 'freemium'],
      'Şirketlerle güvenlik araştırmacılarını buluşturan kitlesel zafiyet (bug bounty) platformu. '
      'Tek tek programlardan farkı çok sayıda hedefi tek panelde toplaması.',
      'A crowdsourced vulnerability (bug bounty) platform connecting companies with security researchers. '
      'Unlike individual programs it gathers many targets in one dashboard.', 'guvenlik', K),
    a('https://github.com/apsdehal/awesome-ctf', 'Awesome CTF', ['awesome-liste', 'github', 'güvenlik', 'pratik'],
      'Capture The Flag için araç, wargame ve öğretici listesi. Tek yarışmadan farkı hazırlık için '
      'gereken tüm araç zincirini kategori kategori vermesi.',
      'A list of tools, wargames and tutorials for Capture The Flag. Unlike a single contest it gives the '
      'whole toolchain needed to prepare, category by category.', 'guvenlik', AL),
    a('https://github.com/paralax/awesome-honeypots', 'Awesome Honeypots', ['awesome-liste', 'github', 'güvenlik'],
      'Saldırganı tuzağa çekmek için kurulan sahte sistemlerin (honeypot) listesi. Genel savunma '
      'listelerinden farkı yalnız aldatma ve erken uyarı araçlarına odaklanması.',
      'A list of decoy systems (honeypots) set up to lure attackers. Unlike general defence lists it '
      'focuses only on deception and early-warning tools.', 'guvenlik', AL),
    a('https://github.com/TaptuIT/awesome-devsecops', 'Awesome DevSecOps', ['awesome-liste', 'github', 'güvenlik', 'devops'],
      'Güvenliği CI/CD boru hattına gömen araç ve pratiklerin listesi. Ayrı güvenlik testlerinden farkı '
      'denetimi geliştirme akışının içine yerleştirmesi.',
      'A list of tools and practices embedding security into the CI/CD pipeline. Unlike separate security '
      'tests it places the checks inside the development flow.', 'guvenlik', AL),
    a('https://github.com/fabacab/awesome-cybersecurity-blueteam', 'Awesome Cybersecurity Blue Team',
      ['awesome-liste', 'github', 'güvenlik'],
      'Savunma (blue team) için tespit, izleme ve müdahale araçlarının listesi. Saldırı listelerinden '
      'farkı sistemleri korumaya ve olayı yakalamaya odaklanması.',
      'A list of detection, monitoring and response tools for the defensive (blue team) side. Unlike '
      'offensive lists it focuses on protecting systems and catching incidents.', 'guvenlik', AL),
    a('https://github.com/infosecB/awesome-detection-engineering', 'Awesome Detection Engineering',
      ['awesome-liste', 'github', 'güvenlik'],
      'Saldırıları yakalayan tespit kurallarını tasarlama ve işletme kaynakları. Hazır araçlardan farkı '
      '“nasıl iyi tespit yazılır” mühendisliğine eğilmesi.',
      'Resources for designing and operating the detection rules that catch attacks. Unlike ready tools '
      'it leans into the engineering of “how to write good detections”.', 'guvenlik', AL),
    a('https://github.com/FonduAI/awesome-prompt-injection', 'Awesome Prompt Injection',
      ['awesome-liste', 'github', 'güvenlik', 'llm'],
      'Dil modellerine özgü “prompt enjeksiyonu” zafiyetine dair araç ve makale listesi. Klasik güvenlik '
      'listelerinden farkı yalnız YZ sistemlerinin yeni saldırı yüzeyine bakması.',
      'A list of tools and papers on the “prompt injection” vulnerability specific to language models. '
      'Unlike classic security lists it looks only at the new attack surface of AI systems.', 'guvenlik', AL),
    a('https://owasp.org/www-project-juice-shop/', 'OWASP Juice Shop', ['güvenlik', 'pratik', 'açık-kaynak', 'öğretici'],
      'Kasıtlı olarak zafiyetlerle dolu, modern bir web uygulaması — güvenlik öğrenmek için hedef. Kuru '
      'anlatımdan farkı gerçek bir uygulamada onlarca açığı elle sömürmeni sağlaması.',
      'A modern web app deliberately full of vulnerabilities — a target for learning security. Unlike dry '
      'material it lets you exploit dozens of flaws by hand in a real application.', 'guvenlik', TS),
    a('https://www.itsecgames.com/', 'bWAPP', ['güvenlik', 'pratik', 'öğretici'],
      '100’den fazla web zafiyeti içeren, indirilebilir kasıtlı-açık uygulama. Çevrimiçi hedeflerden '
      'farkı kendi makinende, izole ve sınırsız denemeye izin vermesi.',
      'A downloadable, deliberately vulnerable app containing 100+ web vulnerabilities. Unlike online '
      'targets it lets you practise on your own machine, isolated and without limits.', 'guvenlik', TS),
    a('https://google-gruyere.appspot.com/', 'Google Gruyere', ['güvenlik', 'pratik', 'öğretici', 'ücretsiz'],
      'Google’ın web uygulama açıklarını öğreten “delikli peynir” kod laboratuvarı. Salt teoriden farkı '
      'her açığı bulup hem sömürüp hem yamayı deneyimletmesi.',
      'Google’s “full of holes” codelab teaching web application flaws. Unlike pure theory it has you '
      'find each flaw and both exploit and patch it.', 'guvenlik', TS),
