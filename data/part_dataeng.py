# -*- coding: utf-8 -*-
"""Veri Mühendisliği — DataExpert-io/data-engineer-handbook'tan.

Kaynakta veri mühendisliği içeriğiyle birlikte çok sayıda YouTube/TikTok/podcast
bağlantısı ve yanlış sınıflanmış LLM reposu vardı. Buraya alanın çekirdek
araçları, platformları, listeleri ve birkaç kanonik öğrenme kaynağı alındı.
"""

D = 'dataeng'
AL = 'awesomelist'
K = 'kedi'


def load(add):
    def a(url, name, tags, tr, en, src=D):
        add(url, name, tags, tr, en, 'veri_muh', src)

    # ---------------------------------------------------------- işleme motorları
    a('https://spark.apache.org/', 'Apache Spark', ['açık-kaynak', 'veri-bilimi', 'otomasyon'],
      'Büyük veriyi bellek üstünde dağıtık işleyen motor — toplu ve akış işleme. Tek makine '
      'kütüphanelerinden farkı terabaytları küme üzerinde bölüştürüp paralel işlemesi.',
      'An engine that processes big data in a distributed, in-memory way — batch and streaming. Unlike '
      'single-machine libraries it splits terabytes across a cluster and processes them in parallel.'),
    a('https://flink.apache.org/', 'Apache Flink', ['açık-kaynak', 'otomasyon'],
      'Gerçek zamanlı akış işleme motoru; olayları geldikçe, düşük gecikmeyle işler. Spark’ın toplu '
      'kökeninden farkı akışı birinci sınıf model olarak alması.',
      'A real-time stream-processing engine that handles events as they arrive, with low latency. Unlike '
      'Spark’s batch roots it treats streaming as the first-class model.'),
    a('https://kafka.apache.org/', 'Apache Kafka', ['açık-kaynak', 'otomasyon', 'backend'],
      'Olay akışlarını dayanıklı bir günlük olarak taşıyan dağıtık mesaj platformu. Klasik kuyruklardan '
      'farkı mesajı okunduktan sonra silmeyip tekrar oynatılabilir tutması.',
      'A distributed messaging platform carrying event streams as a durable log. Unlike classic queues '
      'it keeps messages replayable rather than deleting them once read.'),

    # ---------------------------------------------------------- dönüşüm & orkestrasyon
    a('https://www.getdbt.com/', 'dbt', ['açık-kaynak', 'veritabanı', 'otomasyon'],
      'Veri ambarındaki dönüşümleri SQL + sürüm kontrolü + test ile yöneten araç. El yazımı SQL '
      'betiklerinden farkı bağımlılık grafiği, belge ve testi bir yazılım projesi gibi getirmesi.',
      'A tool managing data-warehouse transformations with SQL + version control + tests. Unlike '
      'hand-written SQL scripts it brings a dependency graph, docs and tests like a software project.'),
    a('https://airflow.apache.org/', 'Apache Airflow', ['açık-kaynak', 'otomasyon', 'python'],
      'Veri boru hatlarını Python’la tanımlanan yönlü grafik (DAG) olarak zamanlayan orkestratör. Cron’dan '
      'farkı bağımlılık, yeniden deneme ve geçmiş çalıştırma görünürlüğü sunması.',
      'An orchestrator scheduling data pipelines as Python-defined directed graphs (DAGs). Unlike cron it '
      'offers dependencies, retries and visibility into historical runs.'),
    a('https://dagster.io/', 'Dagster', ['açık-kaynak', 'otomasyon', 'python'],
      'Veri varlıklarını merkeze alan orkestratör; her tabloyu bir “varlık” olarak izliyor. Airflow’dan '
      'farkı görevden çok üretilen veriye odaklanıp veri kalitesini yerleşik tutması.',
      'An orchestrator centred on data assets, tracking each table as an “asset”. Unlike Airflow it '
      'focuses on the data produced rather than the task, with data quality built in.'),
    a('https://github.com/dagworks-inc/hamilton', 'Hamilton', ['açık-kaynak', 'github', 'python'],
      'Veri dönüşümlerini fonksiyonlardan bir grafik olarak kuran hafif Python kütüphanesi. Ağır '
      'orkestratörlerden farkı tek dosyada, altyapı gerektirmeden bağımlılık grafiği vermesi.',
      'A lightweight Python library that builds data transformations as a graph from functions. Unlike '
      'heavy orchestrators it gives a dependency graph in a single file with no infrastructure.'),

    # ---------------------------------------------------------- platform & ambar
    a('https://www.databricks.com/', 'Databricks', ['veri-bilimi', 'freemium', 'otomasyon'],
      'Spark üstüne kurulu, veri gölü ile ambarı birleştiren (“lakehouse”) bulut platformu. Ayrı ambar '
      've göl kurmaktan farkı ikisini tek yönetişim ve defter arayüzünde toplaması.',
      'A cloud platform built on Spark that merges the data lake and warehouse (“lakehouse”). Unlike '
      'running a separate warehouse and lake it unites them under one governance and notebook interface.'),
    a('https://duckdb.org/', 'DuckDB', ['açık-kaynak', 'veritabanı', 'veri-bilimi'],
      'Süreç içinde çalışan analitik veritabanı — kurulum yok, dosyayı doğrudan sorguluyor. Sunucu '
      'gerektiren ambarlardan farkı tek makinede, Parquet/CSV üstünde “SQLite hızında OLAP” olması.',
      'An in-process analytical database — no server, it queries files directly. Unlike server-based '
      'warehouses it is “OLAP at SQLite speed” on one machine, over Parquet/CSV.'),
    a('https://iceberg.apache.org/', 'Apache Iceberg', ['açık-kaynak', 'veritabanı'],
      'Büyük analitik tablolar için açık tablo biçimi; şema evrimi, zaman yolculuğu ve atomik yazma verir. '
      'Ham Parquet dizininden farkı tabloyu tutarlı, sürümlenebilir bir birim gibi yönetmesi.',
      'An open table format for large analytical tables, giving schema evolution, time travel and atomic '
      'writes. Unlike a raw Parquet directory it manages the table as a consistent, versioned unit.'),

    # ---------------------------------------------------------- öğrenme & referans
    a('https://github.com/DataTalksClub/data-engineering-zoomcamp',
      'Data Engineering Zoomcamp', ['müfredat', 'ücretsiz', 'github'],
      'Veri mühendisliğini uçtan uca (Docker, dbt, Spark, Kafka, bulut) öğreten ücretsiz, projeli kurs. '
      'Dağınık öğreticilerden farkı gerçek bir boru hattını baştan sona kurdurması.',
      'A free, project-based course teaching data engineering end to end (Docker, dbt, Spark, Kafka, '
      'cloud). Unlike scattered tutorials it has you build a real pipeline from start to finish.', K),
    a('https://github.com/igorbarinov/awesome-data-engineering', 'Awesome Data Engineering',
      ['awesome-liste', 'github', 'referans'],
      'Veri mühendisliğinin tüm katmanlarını — alım, depolama, işleme, orkestrasyon — araçlarıyla toplayan '
      'liste. Tek araca bağlı listelerden farkı yığının bütününü haritalaması.',
      'A list gathering every layer of data engineering — ingestion, storage, processing, orchestration — '
      'with tools. Unlike single-tool lists it maps the whole stack.', AL),
    a('https://github.com/awesome-spark/awesome-spark', 'Awesome Spark', ['awesome-liste', 'github', 'açık-kaynak'],
      'Apache Spark ekosistemi için paket, öğretici ve örnek listesi. Resmî dokümandan farkı topluluk '
      'kütüphanelerini ve gerçek dünya örneklerini toplaması.',
      'A list of packages, tutorials and examples for the Apache Spark ecosystem. Unlike the official docs '
      'it gathers community libraries and real-world examples.', AL),
    a('https://github.com/JerryLead/SparkInternals', 'Spark Internals', ['github', 'öğretici', 'referans'],
      'Apache Spark’ın içeride nasıl çalıştığını — zamanlama, karıştırma, bellek — anlatan derin belge. '
      'Kullanım kılavuzundan farkı motorun altını açması, performans ayarı için.',
      'A deep document on how Apache Spark works inside — scheduling, shuffle, memory. Unlike a usage '
      'guide it opens up the engine, for performance tuning.', AL),
    a('https://learn.microsoft.com/en-us/training/career-paths/data-engineer', 'Microsoft · Data Engineer Path',
      ['müfredat', 'ücretsiz'],
      'Bulut veri mühendisliğini modül modül öğreten Microsoft öğrenme patikası. Ürün dokümanından farkı '
      'sınavla ölçülen, sıralı bir beceri yolu olarak kurgulanması.',
      'A Microsoft learning path teaching cloud data engineering module by module. Unlike product docs it '
      'is framed as an ordered, exam-measured skill path.', K),
