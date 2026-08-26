# -*- coding: utf-8 -*-
"""Records surfaced by Paul Jerimy's security certification roadmap.

The roadmap's HTML carries 479 links across 104 domains, but almost all of
them are individual exam pages -- 51 GIAC certificates, 26 from Mile2. Adding
them one by one would flood the directory and break its own rule, because
"CompTIA Security+ exam page" cannot be given a description that says where it
parts ways with its neighbours.

What is worth having is the bodies behind them. A reader deciding between
certifications needs to know which organisation is vendor-neutral, which is
practical rather than multiple-choice, which is recognised by employers and
which is recognised only by its own marketing. That is a question about
awarding bodies, and there are about forty of them.

These carry src='seccert'.
"""

S = 'seccert'


def load(add):
    def a(url, name, tags, tr, en, cat):
        add(url, name, tags, tr, en, cat, S)

    # ============================================================ THE MAP ITSELF
    a('https://pauljerimy.com/security-certification-roadmap/',
      'Security Certification Roadmap', ['sertifika', 'güvenlik', 'referans', 'ücretsiz'],
      'Güvenlik sertifikalarını on uzmanlık alanına ve dört zorluk kademesine yerleştiren '
      'etkileşimli tablo. Kurumların kendi sayfalarından farkı satıcı bağımsız olması: aynı '
      'seviyedeki rakip sertifikaları yan yana koyuyor, böylece hangisinin gerçekten ileri '
      'seviye olduğunu pazarlama metnine bakmadan görüyorsun.',
      'An interactive chart placing security certifications across ten specialisms and four '
      'difficulty tiers. Unlike each body’s own pages it is vendor-neutral: competing '
      'certifications at the same level sit side by side, so you can see which is genuinely '
      'advanced without reading anyone’s marketing.',
      'guvenlik')
    a('https://github.com/PaulJerimy/SecCertRoadmapHTML',
      'Security Cert Roadmap (kaynak)', ['sertifika', 'github', 'açık-kaynak'],
      'Yol haritasının HTML kaynağı, CC BY-SA lisanslı. Görselin kendisinden farkı veriyi '
      'ayıklanabilir hâlde vermesi — kendi listeni türetmek ya da kapsamı denetlemek için. '
      'Son güncelleme Ağustos 2024, yani tabloda o tarihten sonraki sertifikalar yok.',
      'The roadmap’s HTML source under CC BY-SA. Against the image itself it hands you the data '
      'in extractable form, for deriving your own list or auditing the coverage. Last updated '
      'August 2024, so anything newer is missing from the chart.',
      'referans')

    # ============================================================ VENDOR-NEUTRAL BODIES
    a('https://www.giac.org/', 'GIAC', ['sertifika', 'güvenlik', 'ücretli'],
      'SANS eğitimlerinin sınav kolu; elli küsur sertifikayla alanın en geniş kataloğu. '
      'Diğerlerinden farkı sınavların açık kitap olması ve derinlemesine teknik olması — '
      'karşılığında sektörün en pahalı sertifikaları, çoğu işveren desteği olmadan alınmıyor.',
      'The examination arm of SANS training, with over fifty certificates — the broadest '
      'catalogue in the field. What separates it is open-book exams that go deep technically; '
      'the price is that these are the most expensive certifications around, rarely taken '
      'without an employer paying.',
      'guvenlik')
    a('https://www.sans.org/', 'SANS Institute', ['sertifika', 'güvenlik', 'ücretli', 'müfredat'],
      'Güvenlik eğitiminde fiilî standart kurum; kursları GIAC sınavlarına hazırlıyor. Çevrimiçi '
      'kurs platformlarından farkı eğitmenlerin çoğunun aktif olay müdahale ekiplerinden gelmesi. '
      'Ücretsiz okuma odası (Reading Room) ve posterleri kurs almadan da erişilebilir.',
      'The de facto standard for security training, with courses feeding into GIAC exams. Against '
      'online course platforms, most instructors come from active incident response work. Its '
      'Reading Room papers and cheat-sheet posters are free without taking a course.',
      'guvenlik')
    a('https://www.isc2.org/', 'ISC2', ['sertifika', 'güvenlik', 'ücretli'],
      'CISSP’in sahibi kurum. Teknik sertifikalardan farkı yönetişim ve risk ağırlıklı olması ve '
      'sınavı geçmenin yetmemesi — beş yıl belgelenmiş deneyim ve bir üyenin kefaleti gerekiyor. '
      'Bu yüzden işverenler nezdinde ağırlığı yüksek, ilk sertifika olarak ise uygun değil.',
      'The body behind CISSP. Unlike technical certifications it leans on governance and risk, and '
      'passing is not enough: five years of documented experience and an endorsement are '
      'required. That is why it carries weight with employers and why it is a poor first '
      'certificate.',
      'guvenlik')
    a('https://www.isaca.org/', 'ISACA', ['sertifika', 'güvenlik', 'akademik', 'ücretli'],
      'CISA, CISM ve CRISC’in sahibi; denetim, yönetişim ve risk tarafının kurumu. ISC2 ile farkı '
      'odak: ISC2 güvenlik mimarisine, ISACA iç denetim ve uyum süreçlerine bakıyor. Finans ve '
      'düzenlenmiş sektörlerde CISA çoğu zaman iş ilanında şart olarak geçiyor.',
      'The body behind CISA, CISM and CRISC, covering audit, governance and risk. The split from '
      'ISC2 is focus: ISC2 looks at security architecture, ISACA at internal audit and compliance. '
      'In finance and regulated industries CISA is frequently a hard requirement in job postings.',
      'guvenlik')
    a('https://www.comptia.org/', 'CompTIA', ['sertifika', 'ücretli', 'müfredat'],
      'Security+, Network+ ve A+ ile giriş seviyesinin standart basamağı. Üst düzey '
      'sertifikalardan farkı deneyim şartı olmaması — bu yüzden ilk işe girişte ve ABD savunma '
      'sektöründe (DoD 8570 listesi) sıkça isteniyor. Derinlik beklememek gerekiyor.',
      'The standard entry rung through Security+, Network+ and A+. Unlike senior certifications it '
      'demands no prior experience, which is why it appears in first-job listings and in the US '
      'defence sector’s DoD 8570 list. Do not expect depth.',
      'ogrenme')
    a('https://www.eccouncil.org/', 'EC-Council', ['sertifika', 'güvenlik', 'ücretli'],
      'CEH’in (Certified Ethical Hacker) sahibi. Adı tanınırlığı yüksek ama itibarı tartışmalı: '
      'sınav çoktan seçmeli ve pratik beceriyi ölçmediği yönünde yaygın eleştiri var. İK '
      'süzgeçlerinden geçmek için işe yarıyor, teknik yeterlilik kanıtı olarak OSCP tercih '
      'ediliyor.',
      'The body behind CEH. Name recognition is high but reputation is contested: the exam is '
      'multiple-choice and widely criticised for not measuring practical skill. It works for '
      'getting past HR filters; as evidence of technical competence, OSCP is preferred.',
      'guvenlik')
    a('https://www.offsec.com/', 'OffSec', ['sertifika', 'güvenlik', 'ücretli'],
      'OSCP’nin sahibi, eski adıyla Offensive Security. Çoktan seçmeli sınavlardan farkı tamamen '
      'pratik olması: 24 saat içinde gerçek makineleri ele geçirip rapor yazıyorsun. Sızma testi '
      'işe alımlarında fiilî giriş bileti; zorluğu da itibarının kaynağı.',
      'The body behind OSCP, formerly Offensive Security. Against multiple-choice exams it is '
      'entirely practical: you compromise real machines within 24 hours and write the report. It '
      'is the de facto entry ticket for penetration testing hiring, and its difficulty is the '
      'source of its standing.',
      'guvenlik')
    a('https://www.crest-approved.org/', 'CREST', ['sertifika', 'güvenlik', 'ücretli'],
      'İngiltere merkezli akreditasyon kurumu; hem bireyleri hem sızma testi firmalarını '
      'belgelendiriyor. Diğerlerinden farkı bu kurumsal akreditasyon — Birleşik Krallık kamu '
      'ihalelerinde CREST onaylı firma şartı sıkça aranıyor.',
      'A UK-based accreditation body certifying both individuals and penetration testing firms. '
      'That organisational accreditation is what sets it apart: UK public sector tenders '
      'frequently require a CREST-approved supplier.',
      'guvenlik')
    a('https://www.isecom.org/', 'ISECOM', ['güvenlik', 'açık-kaynak', 'referans'],
      'OSSTMM güvenlik test metodolojisini yayımlayan kâr amacı gütmeyen kurum. Sertifika '
      'kurumlarından farkı asıl ürününün metodoloji olması: nasıl test edileceğini tarif eden, '
      'ücretsiz ve satıcı bağımsız bir standart.',
      'The non-profit publishing the OSSTMM security testing methodology. Unlike the certification '
      'bodies its actual product is the method: a free, vendor-neutral standard describing how '
      'testing should be done.',
      'guvenlik')

    # ============================================================ PRACTICAL / HANDS-ON
    a('https://academy.hackthebox.com/', 'Hack The Box Academy',
      ['sertifika', 'güvenlik', 'interaktif', 'freemium'],
      'Modül tabanlı öğrenme ve CPTS/CBBH gibi pratik sertifikalar. OSCP’den farkı öğrenme '
      'yolunun sınavla aynı platformda olması ve fiyatın belirgin düşük olması; karşılığında '
      'işveren tanınırlığı henüz OSCP düzeyinde değil.',
      'Module-based learning with practical certifications such as CPTS and CBBH. Against OSCP the '
      'learning path lives on the same platform as the exam and costs markedly less; in exchange, '
      'employer recognition is not yet at OSCP’s level.',
      'guvenlik')
    a('https://www.tcm-sec.com/', 'TCM Security', ['sertifika', 'güvenlik', 'ücretli'],
      'PNPT sertifikasının sahibi; sınav beş günlük gerçek bir sızma testi ve ardından rapor ile '
      'sözlü savunma içeriyor. OSCP’den farkı sözlü savunma aşaması ve fiyatın onda biri '
      'civarında olması — bütçesi olmayanlar için pratik sertifikaya en kısa yol.',
      'The body behind PNPT, whose exam is a five-day real engagement followed by a report and a '
      'live debrief. The debrief and a price around a tenth of OSCP’s are the differences — the '
      'shortest route to a practical certificate without a budget.',
      'guvenlik')
    a('https://security.ine.com/', 'INE Security', ['sertifika', 'güvenlik', 'ücretli'],
      'eLearnSecurity’nin devamı; eJPT ve eCPPT gibi pratik sertifikalar veriyor. OSCP’den farkı '
      'eJPT’nin gerçekten giriş seviyesi olması — pratik sınav deneyimini ilk kez yaşamak için '
      'daha yumuşak bir basamak.',
      'The continuation of eLearnSecurity, awarding practical certificates such as eJPT and eCPPT. '
      'Against OSCP, eJPT is genuinely entry-level — a gentler first encounter with a hands-on '
      'exam format.',
      'guvenlik')
    a('https://www.mosse-institute.com/', 'Mossé Cyber Security Institute',
      ['sertifika', 'güvenlik', 'ücretli'],
      'Yüzlerce pratik alıştırmadan oluşan, sınav yerine gönderilen çalışmaların '
      'değerlendirilmesine dayanan program. Sınav odaklı kurumlardan farkı bu: not tek bir günde '
      'değil biriken portföyle veriliyor, abonelik modeliyle çalışıyor.',
      'A programme of hundreds of practical exercises graded on submitted work rather than a sat '
      'exam. That is the break from exam-centred bodies: the assessment accumulates as a '
      'portfolio, on a subscription model.',
      'guvenlik')
    a('https://mile2.com/', 'Mile2', ['sertifika', 'güvenlik', 'ücretli'],
      'EC-Council’a benzer bir katalog sunan alternatif kurum; C)PTE ve C)ISSO gibi sertifikalar. '
      'Farkı fiyat ve ABD kamu tanınırlığı (NSA/CNSS eşlemeleri); dezavantajı sektör içinde '
      'tanınırlığının EC-Council ve GIAC kadar geniş olmaması.',
      'An alternative body with a catalogue resembling EC-Council’s, awarding C)PTE and C)ISSO '
      'among others. It differs on price and US government mappings (NSA/CNSS); the drawback is '
      'recognition narrower than EC-Council’s or GIAC’s.',
      'guvenlik')
    a('https://secops.group/', 'The SecOps Group', ['sertifika', 'güvenlik', 'ücretli'],
      'Uygulama ve API güvenliğine odaklanan pratik sınavlar sunan kurum. Geniş kataloglu '
      'kurumlardan farkı dar kapsamı: web ve mobil uygulama sızma testi becerisini doğrudan '
      'ölçen, kısa ve ucuz sınavlar.',
      'A body offering practical exams focused on application and API security. Against the '
      'broad-catalogue organisations its narrowness is the point: short, inexpensive exams that '
      'measure web and mobile penetration testing directly.',
      'guvenlik')
    a('https://0xdarkvortex.dev/', 'Dark Vortex', ['güvenlik', 'ücretli', 'c-ailesi'],
      'Kötücül yazılım geliştirme ve saldırı aracı yazımı üzerine ileri seviye kurslar. Sızma '
      'testi eğitimlerinden farkı savunma atlatma ve implant geliştirme tarafına inmesi — kırmızı '
      'takım araç geliştiricileri için, sertifika arayanlar için değil.',
      'Advanced courses on malware development and offensive tooling. Unlike penetration testing '
      'training it goes down to evasion and implant development — aimed at red team tool '
      'developers rather than at anyone collecting certificates.',
      'guvenlik')
    a('https://limessecurity.com/', 'Limes Security', ['güvenlik', 'gömülü', 'ücretli'],
      'Endüstriyel kontrol sistemleri ve kritik altyapı güvenliğine odaklanan Avusturya merkezli '
      'firma; OT güvenliği eğitimleri veriyor. Genel güvenlik eğitimlerinden farkı PLC ve SCADA '
      'gibi işletim teknolojisi tarafını ele alması.',
      'An Austrian firm focused on industrial control systems and critical infrastructure, with OT '
      'security training. Against general security training it addresses the operational '
      'technology side — PLCs and SCADA.',
      'guvenlik')

    # ============================================================ GOVERNANCE / PROCESS
    a('https://www.exin.com/', 'EXIN', ['sertifika', 'ücretli', 'referans'],
      'Hollanda merkezli, satıcı bağımsız sınav kurumu; bilgi güvenliği yönetimi (ISO 27001) ve '
      'veri koruma alanında sertifikalar. Eğitim veren kurumlardan farkı yalnızca sınav yapması — '
      'eğitimi kimden aldığın kurumu ilgilendirmiyor.',
      'A Dutch vendor-neutral examination institute certifying in information security management '
      '(ISO 27001) and data protection. Unlike training providers it only examines: where you '
      'learned the material is not its concern.',
      'ogrenme')
    a('https://pecb.com/', 'PECB', ['sertifika', 'ücretli', 'referans'],
      'ISO standartları üzerine denetçi ve uygulayıcı sertifikaları veren kurum; 27001, 22301 ve '
      '9001 dahil. EXIN’den farkı akredite eğitmen ağı üzerinden çalışması ve baş denetçi (lead '
      'auditor) yetkisi vermesi.',
      'A body certifying auditors and implementers against ISO standards including 27001, 22301 '
      'and 9001. Against EXIN it operates through an accredited trainer network and confers lead '
      'auditor status.',
      'ogrenme')
    a('https://www.seco-institute.org/', 'SECO-Institute', ['sertifika', 'güvenlik', 'ücretli'],
      'Avrupa merkezli, güvenlik rollerini kademeli bir yolla belgelendiren kurum. Tek tek sınav '
      'satan kurumlardan farkı role dayalı yol tanımlaması — analistten mimara kadar hangi '
      'sertifikanın hangi sırayla alınacağı belirlenmiş.',
      'A European body certifying security roles along a tiered path. Unlike organisations selling '
      'individual exams it defines role-based tracks — which certificate comes in which order, '
      'from analyst to architect.',
      'ogrenme')
    a('https://www.gaqm.org/', 'GAQM', ['sertifika', 'ücretli'],
      'Geniş bir alanda satıcı bağımsız sertifika veren kurum: proje yönetimi, kalite, güvenlik. '
      'Yerleşik kurumlardan farkı fiyatının düşük ve sınava giriş koşulunun esnek olması; '
      'karşılığında işveren tanınırlığı sınırlı.',
      'A body issuing vendor-neutral certificates across a wide field — project management, '
      'quality, security. Against the established organisations it is cheap with flexible entry '
      'requirements; in exchange, employer recognition is limited.',
      'ogrenme')
    a('https://www.axelos.com/', 'AXELOS', ['sertifika', 'ücretli', 'referans'],
      'ITIL, PRINCE2 ve MSP çerçevelerinin sahibi. Güvenlik kurumlarından farkı hizmet yönetimi ve '
      'proje yönetimi tarafında olması — ITIL, kurumsal BT süreçlerinin ortak dili, güvenlik '
      'ekipleri de olay yönetiminde aynı sözlüğü kullanıyor.',
      'The owner of the ITIL, PRINCE2 and MSP frameworks. Unlike the security bodies it sits on the '
      'service and project management side — ITIL is the shared vocabulary of corporate IT, and '
      'security teams use the same terms for incident handling.',
      'ogrenme')
    a('https://apmg-international.com/', 'APMG International', ['sertifika', 'ücretli'],
      'AXELOS çerçevelerinin ve başka standartların sınavlarını yürüten akreditasyon kurumu. '
      'Çerçeve sahibi kurumlardan farkı bağımsız sınav sağlayıcı olması — aynı ITIL sınavına '
      'birden çok kurumdan girilebiliyor, APMG bunlardan biri.',
      'An accreditation body running examinations for the AXELOS frameworks and others. Unlike the '
      'framework owners it is an independent examination institute — the same ITIL exam is '
      'available through several, and APMG is one of them.',
      'ogrenme')
    a('https://www.pmi.org/certifications', 'PMI', ['sertifika', 'ücretli', 'referans'],
      'PMP’nin sahibi; proje yönetiminin en yaygın sertifikası. PRINCE2’den farkı süreç şablonu '
      'değil bilgi alanları üzerine kurulu olması ve deneyim şartı bulunması — başvurmak için '
      'belgelenmiş proje saati gerekiyor.',
      'The body behind PMP, project management’s most widespread certification. Against PRINCE2 it '
      'is built on knowledge areas rather than a process template, and it requires experience: '
      'documented project hours are needed to apply.',
      'ogrenme')
    a('https://www.scrum.org/', 'Scrum.org', ['sertifika', 'ücretli', 'referans'],
      'Scrum’ın kurucularından Ken Schwaber tarafından kurulan sertifika kurumu. Scrum '
      'Alliance’tan farkı sınava kurs almadan girilebilmesi ve sertifikanın yenileme ücreti '
      'istememesi — bir kez geçtiğinde kalıcı.',
      'The certification body founded by Ken Schwaber, one of Scrum’s originators. Against Scrum '
      'Alliance you can sit the exam without taking a course, and the certificate carries no '
      'renewal fee — pass once and it stands.',
      'ogrenme')
    a('https://www.bcs.org/', 'BCS', ['sertifika', 'akademik', 'ücretli'],
      'Birleşik Krallık’ın kraliyet beratlı bilişim meslek kuruluşu; sertifika verdiği gibi '
      'üniversite programlarını da akredite ediyor. Ticari sınav kurumlarından farkı meslek odası '
      'olması ve mühendislik ünvanı yolunda basamak sayılması.',
      'The UK’s chartered professional body for IT, which certifies and also accredits university '
      'programmes. Unlike commercial examination institutes it is a professional institution, and '
      'a step on the path to chartered engineer status.',
      'ogrenme')
    a('https://www.itgovernance.co.uk/', 'IT Governance', ['sertifika', 'güvenlik', 'ücretli'],
      'ISO 27001, GDPR ve siber dayanıklılık üzerine eğitim, danışmanlık ve araç seti satan '
      'İngiliz firması. Sertifika kurumlarından farkı uygulama tarafını da üstlenmesi — belge '
      'vermekle kalmayıp uyum sürecini yürütüyor.',
      'A UK firm selling training, consultancy and toolkits around ISO 27001, GDPR and cyber '
      'resilience. Unlike a certification body it also takes on the implementation — it does not '
      'just award, it runs the compliance work.',
      'guvenlik')
    a('https://certnexus.com/', 'CertNexus', ['sertifika', 'ücretli', 'llm'],
      'Yeni teknoloji alanlarında satıcı bağımsız sertifikalar veren kurum: siber güvenlik, veri '
      'bilimi, yapay zeka ve IoT. Yerleşik kurumlardan farkı bu yeni alanlara odaklanması — '
      'geleneksel katalogların henüz kapsamadığı konularda ölçüt sunuyor.',
      'A body issuing vendor-neutral certificates in emerging fields: cybersecurity, data science, '
      'AI and IoT. Its difference from the established organisations is that focus — a yardstick '
      'in areas the traditional catalogues have not caught up with.',
      'ogrenme')
    a('https://identitymanagementinstitute.org/', 'Identity Management Institute',
      ['sertifika', 'güvenlik', 'ücretli'],
      'Kimlik ve erişim yönetimine (IAM) adanmış sertifika kurumu. Geniş kapsamlı güvenlik '
      'kurumlarından farkı tek bir alana odaklanması — IAM, güvenliğin en çok iş ilanı çıkan ama '
      'en az sertifikası olan dallarından.',
      'A certification body devoted to identity and access management. Against broad security '
      'organisations it covers one area only — IAM, which produces a great many job postings and '
      'very few certificates.',
      'guvenlik')
    a('https://drii.org/', 'DRI International', ['sertifika', 'ücretli', 'sistem-tasarımı'],
      'İş sürekliliği ve felaket kurtarma alanının sertifika kurumu. Güvenlik sertifikalarından '
      'farkı saldırıya değil kesintiye odaklanması — yangın, sel ve tedarik zinciri kesintisi de '
      'aynı planın konusu.',
      'The certification body for business continuity and disaster recovery. Unlike security '
      'certifications it is concerned with disruption rather than attack — fire, flood and supply '
      'chain failure belong to the same plan.',
      'guvenlik')
    a('https://www.isa.org/certification', 'ISA', ['sertifika', 'gömülü', 'donanım', 'güvenlik'],
      'Otomasyon mühendisliği derneği; IEC 62443 endüstriyel siber güvenlik standardının '
      'sertifikalarını veriyor. BT güvenlik kurumlarından farkı işletim teknolojisine bakması — '
      'bir fabrikada güvenlik önceliği gizlilik değil, sürekliliktir.',
      'The automation engineering society, awarding certificates against the IEC 62443 industrial '
      'cybersecurity standard. Unlike IT security bodies it addresses operational technology, '
      'where the priority is not confidentiality but continuity.',
      'donanim')
    a('https://sabsa.org/', 'SABSA Institute', ['sertifika', 'sistem-tasarımı', 'güvenlik'],
      'İş odaklı güvenlik mimarisi çerçevesi ve sertifikaları. TOGAF gibi genel mimari '
      'çerçevelerinden farkı güvenliğe özgü olması; teknik sertifikalardan farkı ise her güvenlik '
      'kararını bir iş gereksinimine bağlamayı zorunlu kılması.',
      'A business-driven security architecture framework and its certifications. Against general '
      'architecture frameworks like TOGAF it is security-specific; against technical certificates '
      'it insists every security decision trace back to a business requirement.',
      'guvenlik')

    # ============================================================ VENDOR TRACKS
    a('https://www.cisco.com/site/us/en/learn/training-certifications/',
      'Cisco Sertifikasyon', ['sertifika', 'ağ', 'ücretli'],
      'CCNA’dan CCIE’ye uzanan ağ sertifikaları programı. Satıcı bağımsız sertifikalardan farkı '
      'Cisco donanımına özgü olması; buna rağmen CCNA, ağ temellerini öğreten müfredat olarak '
      'marka bağımsız biçimde de değerli sayılıyor.',
      'The networking certification programme from CCNA to CCIE. Unlike vendor-neutral '
      'certificates it is specific to Cisco equipment; even so, CCNA is widely treated as a solid '
      'networking fundamentals curriculum regardless of vendor.',
      'ag')
    a('https://www.juniper.net/us/en/training/certification/', 'Juniper Sertifikasyon',
      ['sertifika', 'ağ', 'ücretsiz'],
      'Junos tabanlı ağ sertifikaları. Cisco programından farkı giriş seviyesi sınavların uzun '
      'süredir ücretsiz sunulması ve eğitim materyalinin açık olması — ağ öğrenmenin maliyetsiz '
      'yolu.',
      'Junos-based networking certifications. Against Cisco’s programme the entry-level exams have '
      'long been offered free and the training material is open — the no-cost route into '
      'networking.',
      'ag')
    a('https://training.fortinet.com/', 'Fortinet Training Institute',
      ['sertifika', 'güvenlik', 'ağ', 'ücretsiz'],
      'NSE programı ve güvenlik eğitimleri. Diğer satıcı programlarından farkı büyük bölümünün '
      'ücretsiz açılmış olması — güvenlik duvarı ve ağ güvenliği temellerini bedelsiz öğrenmek '
      'için en geniş kaynak.',
      'The NSE programme and security training. Against other vendor programmes most of it has '
      'been made free — the broadest no-cost resource for firewall and network security '
      'fundamentals.',
      'ag')
    a('https://www.paloaltonetworks.com/services/education', 'Palo Alto Networks Eğitim',
      ['sertifika', 'güvenlik', 'ağ', 'ücretli'],
      'PCNSA ve PCNSE sertifikaları ile güvenlik duvarı ve bulut güvenliği eğitimleri. '
      'Fortinet’ten farkı kurumsal pazarın üst segmentine odaklanması — sertifika, o ürünleri '
      'işleten kuruluşlarda doğrudan işe yarıyor.',
      'PCNSA and PCNSE certifications with firewall and cloud security training. Against Fortinet '
      'it targets the upper enterprise segment — the certificate pays off directly at '
      'organisations running those products.',
      'ag')
    a('https://training-certifications.checkpoint.com/', 'Check Point Eğitim',
      ['sertifika', 'güvenlik', 'ağ', 'ücretli'],
      'CCSA ve CCSE sertifikaları. Diğer güvenlik duvarı satıcılarından farkı Check Point’in '
      'yönetim mimarisinin ayrı bir bilgi alanı olması — merkezî politika yönetimi eğitimin '
      'ağırlık merkezinde.',
      'The CCSA and CCSE certifications. What differs from other firewall vendors is that Check '
      'Point’s management architecture is its own body of knowledge — centralised policy '
      'management sits at the centre of the training.',
      'ag')
    a('https://www.redhat.com/en/services/certifications', 'Red Hat Sertifikasyon',
      ['sertifika', 'ağ', 'devops', 'ücretli'],
      'RHCSA ve RHCE sertifikaları. Çoktan seçmeli satıcı sınavlarından farkı tamamen pratik '
      'olması — canlı bir sistemde verilen görevleri tamamlıyorsun, bu yüzden Linux tarafında '
      'itibarı yüksek.',
      'The RHCSA and RHCE certifications. Unlike multiple-choice vendor exams these are entirely '
      'practical — you complete tasks on a live system, which is why they carry weight on the '
      'Linux side.',
      'ag')
    a('https://www.lpi.org/', 'Linux Professional Institute',
      ['sertifika', 'ağ', 'açık-kaynak', 'ücretli'],
      'Dağıtım bağımsız Linux sertifikaları (LPIC-1, LPIC-2). Red Hat programından farkı tek bir '
      'dağıtıma bağlı olmaması — Debian, SUSE ya da Arch kullanıyorsan geçerli olan sertifika bu.',
      'Distribution-neutral Linux certifications (LPIC-1, LPIC-2). Against Red Hat’s programme it '
      'is not tied to one distribution — this is the certificate that still applies if you run '
      'Debian, SUSE or Arch.',
      'ag')
    a('https://www.cncf.io/training/certification/', 'CNCF Sertifikasyon',
      ['sertifika', 'devops', 'docker', 'ücretli'],
      'CKA, CKAD ve CKS ile Kubernetes sertifikaları. Bulut sağlayıcı sertifikalarından farkı '
      'satıcı bağımsız olması ve sınavın terminal başında geçmesi — çoktan seçmeli değil, canlı '
      'kümede görev çözüyorsun.',
      'Kubernetes certifications through CKA, CKAD and CKS. Unlike cloud provider certificates '
      'they are vendor-neutral, and the exam happens at a terminal — not multiple choice, but '
      'tasks solved on a live cluster.',
      'devops')
