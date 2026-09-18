# -*- coding: utf-8 -*-
"""Java — Vedenin/useful-java-links'ten kanonik ekosistem.

Kaynak 300’den fazla tek tek kütüphane sayıyordu; hepsini listelemek dizini
boğardı. Buraya dili ve ekosistemi tanımlayan çekirdek — resmî kaynak, derleme,
test, öğrenme ve en yaygın kütüphaneler — alındı.
"""

J = 'javalinks'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, src=J):
        add(url, name, tags, tr, en, 'diller', src)

    a('https://dev.java/learn/', 'Dev.java · Learn', ['öğretici', 'ücretsiz', 'dokümantasyon'],
      'Oracle’ın güncel, resmî Java öğrenme portalı. Eski Java Tutorials’tan farkı modern sürümlere '
      'göre yenilenmiş, konu konu düzenlenmiş olması.',
      'Oracle’s current, official Java learning portal. Unlike the old Java Tutorials it is refreshed for '
      'modern versions and organised topic by topic.', K),
    a('https://www.baeldung.com/', 'Baeldung', ['öğretici', 'ücretsiz', 'referans'],
      'Java ve Spring için çözümlü, güncel öğreticilerin en geniş arşivi. Resmî dokümandan farkı '
      '“şunu nasıl yaparım” sorusuna çalışan kod örnekleriyle cevap vermesi.',
      'The largest archive of worked, up-to-date tutorials for Java and Spring. Unlike the official docs '
      'it answers “how do I do this” with working code examples.', K),
    a('https://openjdk.org/', 'OpenJDK', ['açık-kaynak', 'dokümantasyon'],
      'Java platformunun açık kaynak referans uygulaması — dilin ve JVM’in geliştiği yer. Satıcı '
      'dağıtımlarından farkı standardın kendisinin burada tanımlanması.',
      'The open-source reference implementation of the Java platform — where the language and JVM are '
      'developed. Unlike vendor distributions the standard itself is defined here.'),
    a('https://spring.io/projects/spring-boot', 'Spring Boot', ['backend', 'açık-kaynak', 'api'],
      'Spring uygulamalarını yapılandırma yükü olmadan, çalışır hâlde başlatan çatı. Ham Spring’den '
      'farkı akıllı varsayılanlar ve gömülü sunucuyla “tek komutla ayağa kalkması”.',
      'A framework that starts Spring applications running with no configuration burden. Unlike raw '
      'Spring it brings sensible defaults and an embedded server — “up with one command”.', K),
    a('https://spring.io/', 'Spring Framework', ['backend', 'açık-kaynak', 'api'],
      'Kurumsal Java’nın fiili standardı olan uygulama çatısı — bağımlılık enjeksiyonu, web, veri. '
      'Kütüphane yığmaktan farkı bunları tek tutarlı programlama modelinde birleştirmesi.',
      'The application framework that is the de facto standard for enterprise Java — dependency '
      'injection, web, data. Unlike stacking libraries it unifies them in one consistent model.', K),
    a('https://maven.apache.org/', 'Apache Maven', ['açık-kaynak', 'otomasyon', 'dokümantasyon'],
      'Java için bağımlılık yönetimi ve derlemeyi standart bir proje düzeniyle yapan araç. Elle jar '
      'toplamaktan farkı bağımlılıkları merkezî depodan çözüp yaşam döngüsünü tanımlaması.',
      'A tool doing dependency management and builds for Java with a standard project layout. Unlike '
      'collecting jars by hand it resolves dependencies from a central repository and defines a lifecycle.', K),
    a('https://gradle.org/', 'Gradle', ['açık-kaynak', 'otomasyon'],
      'Java ve Android için betiklenebilir, artımlı derleme aracı. Maven’in XML’inden farkı derleme '
      'mantığını gerçek kodla (Kotlin/Groovy) yazıp yalnız değişeni yeniden derlemesi.',
      'A scriptable, incremental build tool for Java and Android. Unlike Maven’s XML it writes build '
      'logic in real code (Kotlin/Groovy) and rebuilds only what changed.', K),
    a('https://junit.org/junit5/', 'JUnit 5', ['açık-kaynak', 'dokümantasyon'],
      'Java’nın standart birim test çatısı; test yazımı ve çalıştırmanın temeli. Elle main’de denemekten '
      'farkı iddialar, yaşam döngüsü kancaları ve parametreli testler getirmesi.',
      'Java’s standard unit-testing framework; the base of writing and running tests. Unlike trying things '
      'in main it brings assertions, lifecycle hooks and parameterised tests.', K),
    a('https://github.com/akullpp/awesome-java', 'Awesome Java', ['awesome-liste', 'github', 'referans'],
      'Java kütüphane ve çerçevelerini konuya göre düzenleyen liste. Maven Central aramasından farkı '
      'seçilmiş, kategorilenmiş ve bakımı yapılan bir başlangıç haritası olması.',
      'A list organising Java libraries and frameworks by topic. Unlike a Maven Central search it is a '
      'curated, categorised and maintained starting map.', K),
    a('https://github.com/google/guava', 'Guava', ['açık-kaynak', 'github'],
      'Google’ın Java için çekirdek yardımcı kütüphanesi — koleksiyonlar, önbellek, fonksiyonel ekler. '
      'Standart kütüphaneyi elle doldurmaktan farkı bu boşlukları test edilmiş biçimde kapatması.',
      'Google’s core utility library for Java — collections, caching, functional extras. Unlike filling '
      'the standard library’s gaps by hand it closes them in a tested way.', K),
    a('https://github.com/FasterXML/jackson', 'Jackson', ['açık-kaynak', 'github', 'api'],
      'Java’da JSON’u nesneye ve nesneyi JSON’a çeviren fiili standart kütüphane. El yazımı '
      'ayrıştırmadan farkı akış, ağaç ve veri-bağlama modlarını tek çatıda vermesi.',
      'The de facto library for turning JSON into objects and back in Java. Unlike hand-written parsing '
      'it offers streaming, tree and data-binding modes under one roof.', K),
    a('https://projectlombok.org/', 'Project Lombok', ['açık-kaynak'],
      'Getter/setter, yapıcı gibi tekrar eden Java kodunu ek açıklamalarla derleme anında üreten araç. '
      'Elle yazmaktan farkı sınıfı kısa tutup gürültüyü derleyiciye bırakması.',
      'A tool that generates repetitive Java code like getters/setters and constructors from annotations '
      'at compile time. Unlike writing it by hand it keeps the class short and leaves the noise to the '
      'compiler.', K),
    a('https://hibernate.org/', 'Hibernate', ['açık-kaynak', 'veritabanı'],
      'Java nesnelerini ilişkisel veritabanı satırlarına eşleyen ORM. Ham JDBC’den farkı SQL’i büyük '
      'ölçüde soyutlayıp nesne grafiğini kalıcılaştırması.',
      'An ORM mapping Java objects to relational database rows. Unlike raw JDBC it largely abstracts the '
      'SQL and persists the object graph.', K),
    a('https://sdkman.io/', 'SDKMAN!', ['cli', 'açık-kaynak', 'otomasyon'],
      'JDK ve JVM araçlarının birden çok sürümünü kurup değiştiren komut satırı yöneticisi. Elle PATH '
      'ayarlamaktan farkı proje bazında sürüm geçişini tek komuta indirmesi.',
      'A command-line manager to install and switch between multiple versions of the JDK and JVM tools. '
      'Unlike editing PATH by hand it reduces per-project version switching to one command.', K),
    a('https://github.com/vavr-io/vavr', 'Vavr', ['açık-kaynak', 'github'],
      'Java’ya kalıcı koleksiyonlar ve fonksiyonel kontrol yapıları getiren kütüphane. Standart '
      'koleksiyonlardan farkı değişmezliği ve Try/Either gibi tipleri öne alması.',
      'A library bringing persistent collections and functional control structures to Java. Unlike the '
      'standard collections it foregrounds immutability and types like Try/Either.'),
    a('https://github.com/openjdk/jmh', 'JMH', ['açık-kaynak', 'github'],
      'JVM’de mikro-ölçüm için OpenJDK aracı; ölçümü bozan JIT etkilerini hesaba katar. Elle zamanlamadan '
      'farkı ısınma, ölü kod eleme gibi tuzakları doğru kurgulaması.',
      'An OpenJDK tool for microbenchmarking on the JVM that accounts for JIT effects that distort '
      'measurement. Unlike timing by hand it correctly handles traps like warmup and dead-code '
      'elimination.'),
