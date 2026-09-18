# -*- coding: utf-8 -*-
"""Matematik — understanding-math ve komşu listelerden, birkaç kanonik ekle.

Kaynak listenin büyük kısmı Wikipedia notasyon/sözlük sayfası ve tek tek PDF
idi; onlar alınmadı. Buraya sezgi kuran, öğreten ya da görselleştiren canlı
kaynaklar ile alanı temsil eden birkaç kanonik yer (3Blue1Brown, Khan) girdi.
"""

M = 'mathlinks'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, src=M, cat='matematik'):
        add(url, name, tags, tr, en, cat, src)

    # ---------------------------------------------------------- sezgi & görsel
    a('https://www.3blue1brown.com/', '3Blue1Brown', ['video', 'ücretsiz', 'interaktif'],
      'Grant Sanderson’ın matematiği animasyonla anlatan kanalı ve sitesi — lineer cebir, kalkülüs, '
      'analiz. Ders anlatımlarından farkı formülü değil ardındaki resmi göstermesi.',
      'Grant Sanderson’s channel and site explaining mathematics through animation — linear algebra, '
      'calculus, analysis. Unlike lectures it shows the picture behind the formula, not just the formula.',
      K),
    a('https://www.khanacademy.org/math', 'Khan Academy · Matematik', ['ücretsiz', 'interaktif', 'müfredat'],
      'İlkokuldan üniversiteye kadar matematiği alıştırmalı, sıralı biçimde öğreten ücretsiz platform. '
      'Dağınık videolardan farkı önceki konuya bağlı ilerleyen tam bir müfredat sunması.',
      'A free platform teaching mathematics from primary school to university, with exercises in order. '
      'Unlike scattered videos it offers a full curriculum that builds on prior topics.', K),
    a('https://seeing-theory.brown.edu/', 'Seeing Theory', ['interaktif', 'ücretsiz', 'veri-bilimi'],
      'Olasılık ve istatistiği tümüyle etkileşimli görsellerle anlatan Brown Üniversitesi projesi. '
      'Ders kitabından farkı kavramı kaydırıp deneyerek görmen — dağılımı elle oynatıyorsun.',
      'A Brown University project teaching probability and statistics entirely through interactive '
      'visuals. Unlike a textbook you see the concept by dragging and trying — you move the distribution '
      'by hand.'),
    a('https://betterexplained.com/', 'BetterExplained', ['öğretici', 'ücretsiz'],
      'Matematiği ezber yerine sezgiyle anlatan yazı dizisi — üstel fonksiyon, Euler formülü, kalkülüs. '
      'Resmî anlatımdan farkı “neden böyle” sorusuna analoji ve resimle cevap vermesi.',
      'A set of essays explaining maths by intuition rather than memorisation — exponentials, Euler’s '
      'formula, calculus. Unlike formal treatments it answers “why is it like this” with analogy and '
      'pictures.'),

    # ---------------------------------------------------------- ders & notlar
    a('https://tutorial.math.lamar.edu/', 'Paul’s Online Math Notes', ['öğretici', 'ücretsiz', 'referans'],
      'Cebir, kalkülüs ve diferansiyel denklemler için çözümlü, temiz ders notları (Lamar Üniversitesi). '
      'Ders kitabından farkı sınav öncesi hızlı tazeleme için birebir olması.',
      'Clean, worked lecture notes for algebra, calculus and differential equations (Lamar University). '
      'Unlike a textbook it is ideal for a quick refresh before an exam.'),
    a('https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/',
      'MIT · Mathematics for Computer Science', ['müfredat', 'ücretsiz', 'akademik'],
      'Bilgisayar bilimi için gereken ayrık matematiği — mantık, sayma, graf, olasılık — tek derste '
      'toplayan MIT dersi. Genel matematik derslerinden farkı doğrudan CS’e yönelmesi.',
      'An MIT course gathering the discrete mathematics a computer scientist needs — logic, counting, '
      'graphs, probability — in one place. Unlike general maths courses it aims straight at CS.'),
    a('https://www.openintro.org/book/os/', 'OpenIntro Statistics', ['kitap', 'ücretsiz', 'akademik'],
      'Giriş istatistiği için ücretsiz, açık ders kitabı; veri, çıkarım ve regresyonu örnekle anlatıyor. '
      'Ticari kitaplardan farkı bedava olması ve alıştırma/slayt setiyle gelmesi.',
      'A free, open textbook for introductory statistics, covering data, inference and regression by '
      'example. Unlike commercial texts it is free and comes with exercises and slides.'),

    # ---------------------------------------------------------- programcı için matematik
    a('https://jeremykun.com/', 'Math ∩ Programming', ['öğretici', 'ücretsiz', 'algoritma'],
      'Jeremy Kun’un matematiği çalışan kodla buluşturan blogu — kriptografi, graf, makine öğrenmesi '
      'matematiği. Salt teoriden farkı her kavramı uygulamayla kapatması.',
      'Jeremy Kun’s blog joining mathematics with working code — cryptography, graphs, the maths of '
      'machine learning. Unlike pure theory it closes each concept with an implementation.'),
    a('https://github.com/Jam3/math-as-code', 'math-as-code', ['referans', 'github', 'kopya-kâğıdı'],
      'Matematik notasyonunun karşılığını okunur kodla veren kopya kâğıdı: sigma toplamı, nokta çarpımı. '
      'Sembol sözlüklerinden farkı formülün programcı için ne demek olduğunu göstermesi.',
      'A cheat sheet mapping mathematical notation to readable code: sigma sums, dot products. Unlike '
      'symbol glossaries it shows what the formula means to a programmer.'),
    a('https://www.math.ubc.ca/~carrell/NB.pdf', 'Fundamentals of Linear Algebra (UBC)',
      ['kitap', 'ücretsiz', 'akademik'],
      'Lineer cebiri temelden kuran ücretsiz UBC ders metni. Kısa notlardan farkı ispatlarıyla tam bir '
      'kaynak olması — dersin arkasını görmek isteyene.',
      'A free UBC text building linear algebra from the ground up. Unlike short notes it is a complete, '
      'proof-carrying resource for those who want the reasoning behind the course.'),
    a('https://cs229.stanford.edu/section/cs229-linalg.pdf', 'Stanford CS229 · Linear Algebra Review',
      ['referans', 'ücretsiz', 'veri-bilimi'],
      'Makine öğrenmesi için gereken lineer cebiri özetleyen Stanford referansı. Tam bir dersten farkı '
      'yalnız ML’de kullanılan parçaya odaklanan hızlı bir hatırlatma olması.',
      'A Stanford reference summarising the linear algebra needed for machine learning. Unlike a full '
      'course it is a quick refresher focused only on the parts ML uses.'),

    # ---------------------------------------------------------- soru & referans
    a('https://math.stackexchange.com/', 'Mathematics Stack Exchange', ['ücretsiz', 'interaktif', 'referans'],
      'Matematik soru-cevap sitesi; takıldığın adımı uzmanlara sorabildiğin yer. Foruma göre farkı '
      'oylamayla en açık çözümün öne çıkması.',
      'A mathematics Q&A site where you can ask experts about the step you are stuck on. Unlike a forum, '
      'voting surfaces the clearest solution.'),
    a('https://www.intmath.com/', 'Interactive Mathematics', ['interaktif', 'ücretsiz', 'öğretici'],
      'Konu konu etkileşimli grafik ve çözümlü örneklerle matematik anlatan site. Statik notlardan farkı '
      'grafiği yerinde oynatıp sonucu görebilmen.',
      'A site teaching mathematics topic by topic with interactive graphs and worked examples. Unlike '
      'static notes you can move the graph in place and see the result.'),
    a('https://github.com/rossant/awesome-math', 'Awesome Math', ['awesome-liste', 'github', 'referans'],
      'Matematik kaynaklarını dala göre (cebir, analiz, topoloji) düzenleyen liste. Tek bir dersten farkı '
      'nereden başlanacağının haritasını çıkarması.',
      'A list organising mathematics resources by branch (algebra, analysis, topology). Unlike a single '
      'course it maps out where to start.'),
    a('https://www.wzchen.com/probability-cheatsheet', 'Probability Cheatsheet', ['kopya-kâğıdı', 'ücretsiz', 'referans'],
      'Olasılık dersinin dağılım, beklenti ve teoremlerini tek sayfaya sıkıştıran kopya kâğıdı. Ders '
      'kitabından farkı sınav anında tek bakışta taranabilir olması.',
      'A cheat sheet compressing a probability course’s distributions, expectations and theorems onto one '
      'page. Unlike a textbook it can be scanned at a glance during an exam.'),
    a('https://abstractmath.org/', 'abstractmath.org', ['öğretici', 'ücretsiz', 'referans'],
      'Soyut matematiğe geçişte takılınan yerleri — tanım okuma, ispat dili, notasyon — açan kaynak. '
      'Konu kitaplarından farkı matematiğin “nasıl düşünüldüğünü” hedef alması.',
      'A resource opening the places people get stuck moving into abstract mathematics — reading '
      'definitions, the language of proof, notation. Unlike topic books it targets how mathematics is '
      'thought.'),
