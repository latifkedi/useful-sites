# -*- coding: utf-8 -*-
"""Web & Frontend + Medya, Tasarım & Dosya — awesome-project ve komşu listelerden.

Frontend tarafında framework, üretici araç, referans ve ilham; medya tarafında
stok görsel, illüstrasyon, ikon ve düzenleyiciler. Tek tek makaleler ve zaten
dizide olan büyük isimler (dedup) alınmadı.
"""

AP = 'awesomeproj'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, cat, src=AP):
        add(url, name, tags, tr, en, cat, src)

    # =========================================================== WEB & FRONTEND
    a('https://bulma.io/', 'Bulma', ['frontend', 'açık-kaynak', 'ücretsiz'],
      'Flexbox tabanlı, yalnız CSS’ten oluşan (JavaScript yok) modern framework. Bootstrap’tan farkı '
      'JS bileşeni getirmemesi — sınıfları alıp kendi etkileşimini yazıyorsun.',
      'A modern framework built purely from CSS (no JavaScript), based on Flexbox. Unlike Bootstrap it '
      'ships no JS components — you take the classes and write your own interactions.', 'web'),
    a('https://purecss.io/', 'Pure.css', ['frontend', 'açık-kaynak', 'ücretsiz'],
      'Yalnızca birkaç KB olan, küçük ve modüler bir CSS framework’ü (Yahoo). Büyük '
      'framework’lerden farkı sadece ihtiyacın olan modülü alıp sayfayı hafif tutması.',
      'A tiny, modular CSS framework of just a few KB (Yahoo). Unlike large frameworks you take only the '
      'module you need and keep the page light.', 'web'),
    a('https://cssreference.io/', 'CSS Reference', ['frontend', 'referans', 'ücretsiz', 'interaktif'],
      'Her CSS özelliğini görsel örnekle gösteren başvuru. Spesifikasyondan farkı “bu özellik ne yapar”ı '
      'metin yerine canlı bir demoyla anlatması.',
      'A reference showing every CSS property with a visual example. Unlike the spec it explains “what '
      'does this property do” with a live demo rather than text.', 'web'),
    a('https://csslayout.io/', 'CSS Layout', ['frontend', 'referans', 'ücretsiz', 'kopya-kâğıdı'],
      'Sık kullanılan düzen ve bileşenlerin (kart, ortalama, sabit başlık) hazır CSS tarifleri. Aramaktan '
      'farkı her deseni kopyalanabilir, bağımsız bir örnek olarak vermesi.',
      'Ready CSS recipes for common layouts and components (cards, centring, sticky header). Unlike '
      'searching it gives each pattern as a copyable, self-contained example.', 'web'),
    a('https://cssbattle.dev/', 'CSS Battle', ['frontend', 'pratik', 'interaktif', 'ücretsiz'],
      'Verilen hedef görseli en az kodla, CSS ile yeniden üretmeye çalıştığın oyun. Öğreticilerden farkı '
      'beceriyi yarışma ve puanla keskinleştirmesi.',
      'A game where you reproduce a target image with as little CSS code as possible. Unlike tutorials it '
      'sharpens skill through competition and scoring.', 'web'),
    a('https://www.frontendmentor.io/', 'Frontend Mentor', ['frontend', 'pratik', 'freemium'],
      'Gerçekçi tasarım dosyaları verip onu koda dökmeni isteyen alıştırma platformu. Rastgele '
      'projelerden farkı profesyonel tasarım ve topluluk geri bildirimiyle gelmesi.',
      'A practice platform that gives realistic design files and asks you to turn them into code. Unlike '
      'random projects it comes with professional designs and community feedback.', 'web'),
    a('https://www.awwwards.com/', 'Awwwards', ['frontend', 'referans', 'freemium'],
      'Öne çıkan web tasarımlarını ödüllendiren ve sergileyen galeri. Rastgele ilhamdan farkı jüri '
      'değerlendirmesiyle kaliteyi süzmesi.',
      'A gallery that awards and showcases outstanding web design. Unlike random inspiration it filters '
      'quality through jury evaluation.', 'web'),
    a('https://uigradients.com/', 'uiGradients', ['frontend', 'araclar', 'ücretsiz'],
      'Hazır CSS gradyanlarını gösterip kodunu veren araç. Elle renk denemekten farkı güzel geçişleri '
      'seçip doğrudan kopyalayabilmen.',
      'A tool that shows ready CSS gradients and gives their code. Unlike mixing colours by hand you pick '
      'a pleasing transition and copy it straight.', 'web'),
    a('https://www.fontpair.co/', 'FontPair', ['frontend', 'referans', 'ücretsiz'],
      'Birbiriyle iyi giden Google font çiftlerini gösteren araç. Tek tek denemekten farkı uyumlu '
      'başlık-gövde eşleşmelerini örnekle sunması.',
      'A tool showing Google font pairs that go well together. Unlike trying one by one it presents '
      'harmonious heading-body matches with examples.', 'web'),
    a('https://neumorphism.io/', 'Neumorphism.io', ['frontend', 'araclar', 'ücretsiz'],
      'Yumuşak gölgeli “neumorphism” kutuları için CSS üreten araç. Elle gölge yazmaktan farkı iki '
      'yönlü gölgeyi görsel olarak ayarlayıp kodu vermesi.',
      'A tool generating CSS for soft-shadowed “neumorphism” boxes. Unlike writing shadows by hand it '
      'lets you tune the dual shadow visually and gives the code.', 'web'),
    a('https://grid.layoutit.com/', 'Layoutit Grid', ['frontend', 'araclar', 'ücretsiz', 'interaktif'],
      'CSS Grid düzenini sürükle-bırak çizip kodunu üreten araç. Elle grid yazmaktan farkı satır/sütun '
      'yapısını görsel kurup çıktı alması.',
      'A tool to draw a CSS Grid layout by drag-and-drop and generate its code. Unlike writing grid by '
      'hand you build the row/column structure visually and export it.', 'web'),
    a('https://autoprefixer.github.io/', 'Autoprefixer', ['frontend', 'araclar', 'ücretsiz'],
      'CSS’e tarayıcı ön eklerini (‑webkit‑, ‑moz‑) otomatik ekleyen araç. Elle eklemekten farkı hangi '
      'ekin gerektiğini güncel tarayıcı verisinden bilmesi.',
      'A tool that automatically adds browser prefixes (‑webkit‑, ‑moz‑) to CSS. Unlike adding them by '
      'hand it knows which prefix is needed from current browser data.', 'web'),
    a('https://www.chartjs.org/', 'Chart.js', ['frontend', 'javascript', 'açık-kaynak', 'görsel-üretim'],
      'Canvas üstünde sade, duyarlı grafikler çizen JavaScript kütüphanesi. Ağır görselleştirme '
      'kütüphanelerinden farkı birkaç satırda çalışan, hafif olması.',
      'A JavaScript library drawing simple, responsive charts on canvas. Unlike heavy visualisation '
      'libraries it is lightweight and works in a few lines.', 'web'),
    a('https://sweetalert2.github.io/', 'SweetAlert2', ['frontend', 'javascript', 'açık-kaynak'],
      'Tarayıcının çirkin alert kutusunu güzel, özelleştirilebilir modallarla değiştiren kütüphane. '
      'Yerleşik alert’ten farkı biçim, giriş alanı ve söz (promise) desteği vermesi.',
      'A library replacing the browser’s ugly alert box with pretty, customisable modals. Unlike the '
      'built-in alert it supports styling, input fields and promises.', 'web'),
    a('https://react-hook-form.com/', 'React Hook Form', ['frontend', 'javascript', 'açık-kaynak'],
      'React formlarını az yeniden render’la yöneten, doğrulama getiren kütüphane. Kontrollü '
      'bileşenlerden farkı performansı yüksek tutup kodu sadeleştirmesi.',
      'A library managing React forms with minimal re-renders and built-in validation. Unlike controlled '
      'components it keeps performance high and simplifies the code.', 'web'),
    a('https://frontendfoc.us/', 'Frontend Focus', ['frontend', 'referans', 'ücretsiz'],
      'Frontend dünyasındaki haber, yazı ve araçları haftalık derleyen bülten. Dağınık takipten farkı '
      'tek, süzülmüş bir akışta özet vermesi.',
      'A newsletter rounding up frontend news, articles and tools weekly. Unlike scattered following it '
      'gives a single, filtered digest.', 'web'),

    # =========================================================== MEDYA & TASARIM
    a('https://unsplash.com/', 'Unsplash', ['görsel-üretim', 'ücretsiz', 'referans'],
      'Yüksek çözünürlüklü, telifsiz fotoğrafların en büyük ücretsiz kaynağı. Ücretli bankalardan farkı '
      'atıf zorunluluğu olmadan ticari kullanıma açık olması.',
      'The largest free source of high-resolution, royalty-free photographs. Unlike paid banks it is open '
      'to commercial use with no attribution required.', 'medya'),
    a('https://www.pexels.com/', 'Pexels', ['görsel-üretim', 'ücretsiz', 'video'],
      'Ücretsiz fotoğraf ve videoyu bir arada sunan stok kaynağı. Yalnız fotoğraf sitelerinden farkı '
      'aynı arayüzde telifsiz video da vermesi.',
      'A stock source offering free photos and videos together. Unlike photo-only sites it also gives '
      'royalty-free video in the same interface.', 'medya'),
    a('https://pixabay.com/', 'Pixabay', ['görsel-üretim', 'ücretsiz'],
      'Fotoğraf, illüstrasyon, vektör ve videoyu tek yerde toplayan telifsiz banka. Tek türe odaklı '
      'sitelerden farkı çok biçimli medyayı bir aramada vermesi.',
      'A royalty-free bank gathering photos, illustrations, vectors and video in one place. Unlike '
      'single-type sites it returns multi-format media in one search.', 'medya'),
    a('https://picsum.photos/', 'Lorem Picsum', ['görsel-üretim', 'araclar', 'ücretsiz', 'api'],
      'İstediğin boyutta yer tutucu fotoğraf döndüren servis (görsellerin lorem ipsum’u). Sabit '
      'yer tutuculardan farkı URL’ye boyut verip gerçek fotoğraf alman.',
      'A service returning placeholder photos at any size (the lorem ipsum of images). Unlike fixed '
      'placeholders you pass a size in the URL and get a real photo.', 'medya'),
    a('https://undraw.co/illustrations', 'unDraw', ['görsel-üretim', 'ücretsiz'],
      'Rengini kendi markana göre değiştirebildiğin açık lisanslı illüstrasyon seti. Sabit '
      'illüstrasyonlardan farkı ana rengi tek yerden değiştirip tutarlı bir set alman.',
      'An openly licensed illustration set whose colour you can change to your brand. Unlike fixed '
      'illustrations you switch the accent colour in one place and get a consistent set.', 'medya'),
    a('https://www.humaaans.com/', 'Humaaans', ['görsel-üretim', 'ücretsiz'],
      'Parçalarını karıştırıp poz verebildiğin insan illüstrasyonları kütüphanesi. Hazır '
      'illüstrasyonlardan farkı figürü uzuv uzuv birleştirip özgün sahne kurman.',
      'A library of human illustrations whose parts you can mix and pose. Unlike ready illustrations you '
      'assemble the figure limb by limb into an original scene.', 'medya'),
    a('https://www.manypixels.co/gallery', 'ManyPixels Gallery', ['görsel-üretim', 'ücretsiz'],
      'Rengi düzenlenebilen ücretsiz illüstrasyon galerisi. unDraw’a benzer; farkı daha geniş, konu '
      'bazlı bir koleksiyon ve çoklu format sunması.',
      'A free illustration gallery with editable colour. Similar to unDraw; it offers a larger, '
      'topic-based collection and multiple formats.', 'medya'),
    a('https://fontawesome.com/', 'Font Awesome', ['görsel-üretim', 'referans', 'freemium'],
      'Web’in fiili standardı olan ikon ve logo kütüphanesi. Tek tek SVG toplamaktan farkı ikonları '
      'font/CSS sınıfı olarak, tek satırla eklemen.',
      'The de facto icon and logo library of the web. Unlike collecting SVGs one by one you add icons as '
      'a font/CSS class in a single line.', 'medya'),
    a('https://feathericons.com/', 'Feather Icons', ['görsel-üretim', 'açık-kaynak', 'ücretsiz'],
      'Tek çizgi kalınlığında, sade ve tutarlı açık kaynak ikon seti. Büyük kütüphanelerden farkı '
      'minimal bir görsel dil ve küçük dosya boyutu sunması.',
      'A simple, consistent open-source icon set at a single stroke weight. Unlike large libraries it '
      'offers a minimal visual language and small file size.', 'medya'),
    a('https://iconify.design/', 'Iconify', ['görsel-üretim', 'açık-kaynak', 'ücretsiz'],
      '100’den fazla ikon setini tek API/bileşen altında birleştiren kütüphane. Her seti ayrı kurmaktan '
      'farkı hepsini tek arayüzden çekip karıştırabilmen.',
      'A library unifying 100+ icon sets under one API/component. Unlike installing each set separately '
      'you pull and mix them all from one interface.', 'medya'),
    a('https://icons8.com/', 'Icons8', ['görsel-üretim', 'freemium'],
      'İkon, illüstrasyon, fotoğraf ve müziği farklı stillerde sunan geniş varlık kaynağı. Tek türlü '
      'sitelerden farkı aynı görsel dilde çok türü bir arada vermesi.',
      'A broad asset source offering icons, illustrations, photos and music in various styles. Unlike '
      'single-type sites it gives many types in one consistent visual language.', 'medya'),
    a('https://remixicon.com/', 'Remix Icon', ['görsel-üretim', 'açık-kaynak', 'ücretsiz'],
      'Hem çizgi hem dolu biçimde gelen, tutarlı açık kaynak ikon seti. Karışık setlerden farkı her '
      'ikonun iki stilde de bulunması — arayüzde tutarlılık.',
      'A consistent open-source icon set coming in both line and solid styles. Unlike mixed sets every '
      'icon exists in both styles — consistency across a UI.', 'medya'),
    a('https://openmoji.org/', 'OpenMoji', ['görsel-üretim', 'açık-kaynak', 'ücretsiz'],
      'Açık lisanslı, tek tasarım dilinde emoji kütüphanesi. Platform emojilerinden farkı her yerde aynı '
      'görünen, düzenlenebilir SVG emojiler vermesi.',
      'An openly licensed emoji library in one design language. Unlike platform emojis it gives editable '
      'SVG emojis that look the same everywhere.', 'medya'),
    a('https://www.gimp.org/', 'GIMP', ['açık-kaynak', 'ücretsiz', 'masaüstü'],
      'Photoshop’a açık kaynak alternatif olan tam donanımlı görüntü düzenleyici. Ücretli araçlardan '
      'farkı bedava ve eklentiyle genişleyebilir olması.',
      'A full-featured image editor that is the open-source alternative to Photoshop. Unlike paid tools '
      'it is free and extensible with plugins.', 'medya'),
    a('https://pixlr.com/', 'Pixlr', ['görsel-üretim', 'tarayıcı-içi', 'freemium'],
      'Tarayıcıda çalışan, katman destekli görüntü düzenleyici. Masaüstü programlarından farkı kurulum '
      'istemeden hızlı düzenleme yapmana izin vermesi.',
      'A layer-capable image editor that runs in the browser. Unlike desktop programs it lets you do '
      'quick edits with no install.', 'medya'),
    a('https://www.vectorizer.io/', 'Vectorizer', ['görsel-üretim', 'araclar', 'freemium'],
      'PNG/JPG gibi piksel görselleri vektöre (SVG) çeviren araç. Elle çizmekten farkı mevcut logoyu '
      'ölçeklenebilir hâle otomatik dönüştürmesi.',
      'A tool converting pixel images like PNG/JPG into vectors (SVG). Unlike redrawing by hand it '
      'automatically turns an existing logo into a scalable form.', 'medya'),
    a('https://whimsical.com/', 'Whimsical', ['araclar', 'interaktif', 'freemium'],
      'Akış şeması, tel çerçeve, yapışkan not ve zihin haritasını tek tuvalde birleştiren araç. Tek '
      'amaçlı araçlardan farkı hepsini aynı belgede bir arada tutması.',
      'A tool combining flowcharts, wireframes, sticky notes and mind maps on one canvas. Unlike '
      'single-purpose tools it keeps them all together in one document.', 'medya'),
