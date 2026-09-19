# -*- coding: utf-8 -*-
"""AI - Agents, RAG & Infrastructure"""

C = 'yz_altyapi'


def load(add):
    # ---------------------------------------------------------- frameworks
    add('https://www.langchain.com/', 'LangChain', ['açık-kaynak', 'python', 'çatı', 'mit'],
        'Model, vektör deposu ve araç sağlayıcıları ortak arayüz altında toplayan çatı. '
        'Entegrasyon sayısı en büyük kozu; soyutlama katmanının kalınlığı da en sık gelen şikâyet.',
        'Wraps model, vector store and tool providers behind common interfaces. The integration count is its '
        'strongest card; the thickness of the abstraction layer is the most frequent complaint.', C)
    add('https://docs.langchain.com/oss/python/langchain/overview', 'LangChain Dokümantasyonu', ['dokümantasyon', 'python'],
        'Güncel doküman, eski zincir kavramlarını bırakıp `create_agent` etrafında sadeleşmiş bir API anlatıyor. '
        'Eski öğreticilerdeki `LLMChain` örnekleri artık geçerli değil.',
        'The current docs drop the old chain vocabulary for a slimmer API built around `create_agent`. '
        'The `LLMChain` examples in older tutorials no longer apply.', C)
    add('https://www.langchain.com/langgraph', 'LangGraph', ['açık-kaynak', 'python', 'agent', 'durum-makinesi'],
        'Agent akışını düğüm ve kenarlardan oluşan bir durum grafiği olarak tanımlıyorsun. '
        'Döngü, koşullu dallanma ve akışı durdurup insan onayı bekleme (interrupt) buradan çıkıyor; düz zincirde bunlar yok.',
        'You define agent flow as a state graph of nodes and edges, which is where loops, conditional branching '
        'and pausing for human approval (interrupts) come from. A flat chain has none of that.', C)
    add('https://python.langchain.com/docs/tutorials/agents/', 'LangChain Agents (öğretici)', ['dokümantasyon', 'öğretici', 'agent'],
        'Araç tanımlama, model bağlama ve döngüyü kurma adımlarını sırayla gösteren resmî başlangıç. '
        'Araç çağırma protokolünün nasıl işlediğini görmek için en kısa yol.',
        'The official walkthrough of defining tools, binding a model and wiring the loop — '
        'the shortest way to see how the tool-calling protocol actually works.', C)
    add('https://www.llamaindex.ai/', 'LlamaIndex', ['açık-kaynak', 'python', 'rag', 'mit'],
        'Belge yükleme, parçalama, indeksleme ve sorgu aşamalarının her birini ayrı ayrı değiştirilebilir kılıyor. '
        'Genel amaçlı bir çatı değil; alma (retrieval) hattını ince ayarlamak isteyen için tasarlanmış.',
        'Makes each stage — loading, chunking, indexing, querying — independently swappable. '
        'Not a general-purpose framework: it is built for someone tuning a retrieval pipeline.', C)
    add('https://docs.llamaindex.ai/en/stable/module_guides/workflow/', 'LlamaIndex Workflows', ['dokümantasyon', 'agent', 'async'],
        'Adımların olay yayıp olay dinlediği asenkron bir çalışma zamanı. Graf kurmak yerine '
        '`@step` ile fonksiyon işaretliyorsun; paralel dallar doğal şekilde çıkıyor.',
        'An async runtime where steps emit and listen for events. Instead of building a graph you mark '
        'functions with `@step`, and parallel branches fall out naturally.', C)
    add('https://www.crewai.com/', 'CrewAI', ['açık-kaynak', 'python', 'agent', 'çoklu-agent'],
        'Her agent’a rol, hedef ve arka plan veriyorsun; görevler sıralı ya da hiyerarşik olarak dağıtılıyor. '
        'Kavramsal olarak sade ama akış üzerinde LangGraph kadar ince denetim vermiyor.',
        'You give each agent a role, goal and backstory; tasks are dispatched sequentially or hierarchically. '
        'Conceptually simple, but it gives less fine control over flow than LangGraph.', C)
    add('https://microsoft.github.io/autogen/', 'Microsoft AutoGen', ['açık-kaynak', 'python', 'agent', 'araştırma'],
        'Agent’lar bir grup sohbetinde konuşarak iş çözüyor; konuşma sırasını bir yönetici agent belirliyor. '
        'Araştırma kökenli, bu yüzden API’si sürümler arasında sertçe değişebiliyor.',
        'Agents solve tasks by talking in a group chat, with a manager agent deciding who speaks next. '
        'Research-rooted, so the API can shift sharply between versions.', C)
    add('https://learn.microsoft.com/en-us/agent-framework/', 'Microsoft Agent Framework', ['dokümantasyon', 'agent', 'azure'],
        'AutoGen’in deney tarafıyla Semantic Kernel’in kurumsal tarafını tek çatıda birleştiren yeni hat. '
        'Azure kimlik doğrulama ve izleme altyapısına baştan bağlı geliyor.',
        'The new line merging AutoGen’s experimental side with Semantic Kernel’s enterprise side. '
        'It arrives pre-wired to Azure identity and monitoring.', C)
    add('https://strandsagents.com/', 'AWS Strands Agents', ['açık-kaynak', 'python', 'agent', 'aws'],
        'Akışı elle kurmuyorsun: modele araç listesini veriyorsun, planlamayı o yapıyor. '
        'Az kod isteyen bir yaklaşım, karşılığında hata ayıklarken kararın nereden geldiğini izlemek zorlaşıyor.',
        'You do not wire the flow — you hand the model a tool list and it plans. Less code to write, '
        'at the cost of harder debugging when you need to trace where a decision came from.', C)
    add('https://www.camel-ai.org/', 'CAMEL-AI', ['açık-kaynak', 'python', 'araştırma', 'çoklu-agent'],
        'Rol oynayan agent’ların birbirini yönlendirdiği toplum simülasyonu üzerine araştırma çatısı. '
        'Ölçekli deney ve sentetik veri üretimi için elverişli, ürün altyapısı olarak değil.',
        'A research framework for societies of role-playing agents steering each other. '
        'Suited to scaled experiments and synthetic data generation, not to production plumbing.', C)
    add('https://www.agno.com/', 'Agno', ['açık-kaynak', 'python', 'agent', 'performans'],
        'Bellek, araç ve bilgi tabanı desteği çekirdeğe gömülü; ek soyutlama katmanı yok. '
        'Agent örnekleme süresi mikrosaniye mertebesinde olduğu için çok agent’lı senaryolarda hafif kalıyor.',
        'Memory, tools and knowledge base are built into the core with no extra abstraction layer. '
        'Agent instantiation lands in the microsecond range, which keeps it light in many-agent scenarios.', C)
    add('https://openai.github.io/openai-agents-python/', 'OpenAI Agents SDK', ['açık-kaynak', 'python', 'agent', 'sdk'],
        'Dört kavramla yetiniyor: agent, araç, devretme (handoff) ve koruma bandı. '
        'İzleme (tracing) kutudan çıkıyor; öğrenme eğrisi çatıların en düşüğü.',
        'Settles for four concepts: agents, tools, handoffs and guardrails. Tracing ships built in, '
        'and the learning curve is the shallowest of the frameworks here.', C)
    add('https://ai.pydantic.dev/', 'Pydantic AI', ['açık-kaynak', 'python', 'agent', 'tip-güvenli'],
        'Model çıktısını Pydantic şemasına göre doğruluyor, uymazsa modele geri gönderip düzelttiriyor. '
        'Sonuçta serbest metin değil, tipi garanti edilmiş bir nesne alıyorsun.',
        'Validates model output against a Pydantic schema and sends it back for correction when it fails. '
        'What you get out is a type-guaranteed object, not free text.', C)
    add('https://learn.microsoft.com/semantic-kernel/', 'Semantic Kernel', ['dokümantasyon', 'dotnet', 'python', 'agent'],
        'C#, Python ve Java için tek API sunan agent SDK’sı. Kurumsal .NET yığınında yaşıyorsan '
        'Python ağırlıklı alternatiflerden çok daha az sürtünme çıkarıyor.',
        'An agent SDK exposing one API across C#, Python and Java. If you live in an enterprise .NET stack '
        'it creates far less friction than the Python-centric alternatives.', C)
    add('https://adk.dev/', 'Agent Development Kit (ADK)', ['açık-kaynak', 'python', 'agent', 'google'],
        'Google’ın agent kiti; değerlendirme koşumu ve Cloud Run’a dağıtım komutları kutudan çıkıyor. '
        'Agent2Agent protokolüyle farklı çatılardaki agent’ları konuşturabiliyor.',
        'Google’s agent kit, shipping an evaluation harness and Cloud Run deployment commands out of the box. '
        'The Agent2Agent protocol lets agents from different frameworks talk.', C)
    add('https://aws.amazon.com/bedrock/agents/', 'AWS Bedrock Agents', ['saas', 'ücretli', 'agent', 'aws'],
        'Agent tanımı, araç şeması ve bilgi tabanı AWS konsolundan yapılandırılıyor; çalışma zamanını AWS işletiyor. '
        'Kendi çatını işletmemenin bedeli, akışın AWS’in belirlediği kalıba sığması.',
        'Agent definition, tool schema and knowledge base are configured in the console; AWS runs the runtime. '
        'The price of not operating your own framework is fitting the flow into AWS’s shape.', C)
    add('https://learn.microsoft.com/azure/ai-foundry/', 'Azure AI Foundry', ['saas', 'ücretli', 'azure', 'platform'],
        'Model kataloğu, agent servisi, değerlendirme ve içerik filtresi tek portalda. '
        'Uyumluluk ve bölge denetimi gerektiren kurumsal dağıtımlar için toplanmış bir yığın.',
        'Model catalogue, agent service, evaluation and content filtering in one portal — '
        'a stack assembled for enterprise deployments that need compliance and region control.', C)

    # ---------------------------------------------------------- RAG
    add('https://haystack.deepset.ai/', 'Haystack', ['açık-kaynak', 'python', 'rag', 'pipeline'],
        'Bileşenleri açıkça birbirine bağlıyorsun; hattın hangi adımda ne yaptığı okunabilir kalıyor. '
        'Hata ayıklarken bu şeffaflık LangChain’in örtük akışına karşı gözle görülür bir kazanç.',
        'You wire components together explicitly, so what happens at each stage stays readable. '
        'When debugging, that transparency is a visible win over LangChain’s implicit flow.', C)
    add('https://dspy.ai/', 'DSPy', ['açık-kaynak', 'python', 'optimizasyon', 'araştırma'],
        'İstem metni yazmıyorsun; giriş-çıkış imzası tanımlıyor, örnek veri veriyorsun, optimizer istemleri '
        've few-shot örneklerini kendisi üretiyor. Prompt ayarını derleyiciye devreden bir yaklaşım.',
        'You do not write prompt text — you declare input/output signatures and supply examples, and an optimiser '
        'generates the prompts and few-shot demonstrations. Prompt tuning handed to a compiler.', C)
    add('https://ragflow.io/', 'RAGFlow', ['açık-kaynak', 'self-hosted', 'rag', 'docker'],
        'Derin belge ayrıştırma üstüne kurulu: karmaşık PDF düzenlerini, tabloları ve şekilleri tanıyıp '
        'anlamlı parçalara ayırıyor. Kütüphane değil, Docker ile kurduğun tam bir servis.',
        'Built on deep document parsing: it recognises complex PDF layouts, tables and figures before chunking. '
        'Not a library but a full service you stand up with Docker.', C)
    add('https://microsoft.github.io/graphrag/', 'GraphRAG', ['açık-kaynak', 'python', 'rag', 'bilgi-grafiği'],
        'Belgelerden varlık ve ilişki çıkarıp bilgi grafiği kuruyor, sonra topluluk özetleri üretiyor. '
        '“Bu külliyatın ana temaları neler” gibi bütüne dair sorular parça-getir yöntemiyle cevaplanamıyor; bu onun için var.',
        'Extracts entities and relations into a knowledge graph, then builds community summaries. '
        'Corpus-wide questions like “what are the main themes here” cannot be answered by chunk retrieval; this exists for those.', C)
    add('https://unstructured.io/', 'Unstructured', ['açık-kaynak', 'python', 'ayrıştırma', 'etl'],
        'PDF, DOCX, HTML, e-posta ve sunumları ortak bir belge öğesi modeline indiriyor. '
        'RAG hatlarında en çok vakit yiyen ve en sık bozulan ilk adım burasıdır.',
        'Reduces PDF, DOCX, HTML, email and slides to a shared document-element model. '
        'This first step is where RAG pipelines lose the most time and break most often.', C)
    add('https://github.com/Graphify-Labs/graphify', 'Graphify', ['açık-kaynak', 'github', 'kod', 'bilgi-grafiği'],
        'Kod tabanını AST çözümlemesiyle gezip dokümanları, SQL şemalarını ve PDF’leri de katarak '
        'sorgulanabilir bir grafiğe çeviriyor. Kod asistanına bağlam beslemek için tasarlanmış.',
        'Walks a codebase via AST analysis and folds in docs, SQL schemas and PDFs to build a queryable graph. '
        'Designed to feed context to a coding agent.', C)
    add('https://github.com/headroomlabs-ai/headroom', 'Headroom', ['açık-kaynak', 'github', 'optimizasyon', 'proxy'],
        'Araç çıktısı, günlük ve RAG parçalarını modele ulaşmadan sıkıştırıyor. '
        'Kütüphane, vekil ya da MCP sunucusu olarak çalışabiliyor — JSON ağırlıklı yüklerde kazanç en yüksek.',
        'Compresses tool output, logs and RAG chunks before they reach the model. Runs as a library, a proxy '
        'or an MCP server; the gain is largest on JSON-heavy payloads.', C)

    # ---------------------------------------------------------- embedding
    add('https://platform.openai.com/docs/guides/embeddings', 'OpenAI Embeddings', ['dokümantasyon', 'embedding', 'api'],
        'text-embedding-3 ailesinin boyut, fiyat ve kullanım referansı. '
        'Matryoshka desteği sayesinde vektör boyutunu isteğe göre kısaltıp depolama maliyetini düşürebiliyorsun.',
        'Reference for the text-embedding-3 family — dimensions, pricing, usage. Matryoshka support lets you '
        'truncate vector dimensions on demand and cut storage cost.', C)
    add('https://cohere.com/embed', 'Cohere Embed', ['api', 'ücretli', 'embedding', 'çok-dilli'],
        '100’den fazla dili tek vektör uzayında temsil ediyor; Türkçe sorguyla İngilizce belge bulmak mümkün. '
        'Sorgu ve belge için ayrı giriş tipi almasi eşleşme kalitesini artırıyor.',
        'Represents 100+ languages in one vector space, so a Turkish query can retrieve an English document. '
        'Taking separate input types for query and document lifts match quality.', C)
    add('https://www.voyageai.com/', 'Voyage AI', ['api', 'ücretli', 'embedding', 'alan-özel'],
        'Hukuk, kod ve finans için ayrı ayrı eğitilmiş gömme modelleri. '
        'Dar alanlarda genel amaçlı modelleri geçtiğini iddia ediyor; karşılaştırmayı kendi verinle yapmak gerekiyor.',
        'Embedding models trained separately for law, code and finance. It claims to beat general-purpose models '
        'inside those domains — a claim worth testing on your own data.', C)
    add('https://sbert.net/', 'Sentence Transformers', ['açık-kaynak', 'python', 'embedding', 'yerel-model'],
        'Gömme üretiminin standart Python kütüphanesi. Model yerelde çalışır, veri makineden çıkmaz, '
        'API faturası olmaz; karşılığında GPU ve bellek yönetimi sana kalır.',
        'The standard Python library for producing embeddings. Models run locally, data stays put and there is '
        'no API bill; in exchange GPU and memory management are yours.', C)
    add('https://huggingface.co/BAAI', 'BGE Modelleri', ['açık-ağırlık', 'embedding', 'model'],
        'Açık gömme modellerinin en yaygın ailesi. MTEB sıralamasında ücretli API’lere yakın duruyor '
        've çoğu sürüm MIT lisanslı, yani ticari kullanımda engel yok.',
        'The most widely used family of open embedding models. It sits close to paid APIs on the MTEB leaderboard '
        'and most releases are MIT, so commercial use is unblocked.', C)
    add('https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings', 'Vertex AI Embeddings', ['dokümantasyon', 'embedding', 'gcp'],
        'GCP içindeki gömme servisi. Veriyi BigQuery’de tutuyorsan gömmeyi de aynı sınırlar içinde üretmek '
        'ağ maliyeti ve veri yerleşimi açısından anlamlı oluyor.',
        'The embedding service inside GCP. If your data sits in BigQuery, generating vectors within the same '
        'boundary makes sense for both egress cost and data residency.', C)
    add('https://learn.microsoft.com/azure/ai-services/openai/', 'Azure OpenAI Service', ['dokümantasyon', 'api', 'azure'],
        'OpenAI modelleri, Azure’un bölge seçimi ve özel ağ desteğiyle. '
        'Model sürümleri OpenAI’dan geriden geliyor; uyumluluk kazancının bedeli bu gecikme.',
        'OpenAI models with Azure’s region selection and private networking. Model versions lag OpenAI’s own '
        'releases — that lag is the price of the compliance gain.', C)

    # ---------------------------------------------------------- MCP
    add('https://modelcontextprotocol.io/', 'Model Context Protocol', ['açık-kaynak', 'mcp', 'standart', 'json-rpc'],
        'JSON-RPC üzerine kurulu, modellere araç ve veri kaynağı açmak için açık protokol. '
        'Sunucuyu bir kez yazıyorsun, MCP konuşan her istemci onu kullanabiliyor.',
        'An open protocol over JSON-RPC for exposing tools and data sources to models. '
        'Write the server once and any MCP-speaking client can use it.', C)
    add('https://gofastmcp.com/', 'FastMCP', ['açık-kaynak', 'python', 'mcp', 'sdk'],
        'Dekoratörle fonksiyon işaretleyip MCP aracına çeviriyorsun; şema tip ipuçlarından üretiliyor. '
        'Ham SDK’da elle yazdığın kalıp kodun neredeyse tamamını siliyor.',
        'Decorate a function and it becomes an MCP tool, with the schema derived from type hints. '
        'It erases nearly all the boilerplate you would hand-write against the raw SDK.', C)
    add('https://registry.modelcontextprotocol.io/', 'MCP Registry', ['ücretsiz', 'mcp', 'dizin'],
        'Resmî sunucu kayıt defteri; makine tarafından okunabilir olduğu için istemciler kurulumu '
        'otomatikleştirebiliyor. Dağınık GitHub listelerinin yerini almak üzere kuruldu.',
        'The official server registry. Being machine-readable lets clients automate installation — '
        'it exists to replace scattered GitHub lists.', C)
    add('https://github.com/github/github-mcp-server', 'GitHub MCP Server', ['açık-kaynak', 'github', 'mcp', 'go'],
        'Depo, konu, PR ve Actions işlemlerini araç olarak açan resmî sunucu. '
        'İnce taneli izin kapsamı seçilebiliyor, yani asistana yalnızca okuma yetkisi verebilirsin.',
        'The official server exposing repo, issue, PR and Actions operations as tools. '
        'Permission scopes are fine-grained, so you can hand an assistant read-only access.', C)
    add('https://github.com/modelcontextprotocol/servers', 'MCP Sunucu Koleksiyonu', ['açık-kaynak', 'github', 'mcp', 'referans'],
        'Dosya sistemi, PostgreSQL, Slack, Git ve fetch için referans uygulamalar. '
        'Kendi sunucunu yazmadan önce protokolün nasıl kullanıldığını buradan okumak en hızlısı.',
        'Reference implementations for filesystem, PostgreSQL, Slack, Git and fetch. '
        'Reading these is the fastest way to see the protocol in use before writing your own.', C)
    add('https://mcpmarket.com/tools/skills', 'MCP Market · Agent Skills', ['ücretsiz', 'mcp', 'dizin'],
        'Topluluk yetenek ve sunucu pazarı. Resmî kayıt defterinden geniş, buna karşılık denetimi zayıf — '
        'kurmadan önce kaynağa bakmak gerekir.',
        'A community marketplace of skills and servers. Broader than the official registry but weakly vetted — '
        'read the source before installing.', C)
    add('https://composio.dev/', 'Composio', ['saas', 'freemium', 'agent', 'oauth'],
        'Bin küsur uygulama için hazır araç tanımı ve devredilmiş OAuth akışı sağlıyor. '
        'Her SaaS için kimlik doğrulama yazmak yerine yetkilendirmeyi ona devrediyorsun.',
        'Ships ready tool definitions and delegated OAuth for a thousand-odd apps. '
        'Instead of writing auth per SaaS, you hand the authorisation off to it.', C)

    # ---------------------------------------------------------- safety
    add('https://github.com/NVIDIA/NeMo-Guardrails', 'NeMo Guardrails', ['açık-kaynak', 'github', 'guardrail', 'python'],
        'Colang adlı bir DSL ile izin verilen konuşma akışlarını tanımlıyorsun. '
        'Denetim çıktının içeriğinde değil diyaloğun gidişatında; konu sapmasını girişte kesiyor.',
        'You declare permitted conversation flows in a DSL called Colang. The control sits in the dialogue’s '
        'trajectory rather than the output text, cutting topic drift at the entrance.', C)
    add('https://www.guardrailsai.com/', 'Guardrails AI', ['açık-kaynak', 'python', 'guardrail', 'doğrulama'],
        'Çıktıyı şema ve doğrulayıcı zincirine sokuyor; başarısız olursa yeniden deniyor ya da düzeltiyor. '
        'NeMo diyaloğu tutuyor, bu ise üretilen metnin biçim ve içeriğini.',
        'Runs output through a chain of schemas and validators, retrying or repairing on failure. '
        'NeMo holds the dialogue; this holds the shape and content of the generated text.', C)
    add('https://microsoft.github.io/presidio/', 'Microsoft Presidio', ['açık-kaynak', 'python', 'gizlilik', 'pii'],
        'Metin ve görselde kişisel veriyi (TC kimlik, IBAN, e-posta gibi) tanıyıp maskeliyor. '
        'Tanıyıcılar özelleştirilebilir; modele veri göndermeden önceki anonimleştirme adımı için.',
        'Detects and redacts personal data — national IDs, IBANs, emails — in text and images. '
        'Recognisers are customisable; it belongs in the anonymisation step before data reaches a model.', C)
    add('https://www.lakera.ai/', 'Lakera Guard', ['saas', 'ücretli', 'guardrail', 'prompt-injection'],
        'İstem enjeksiyonu ve jailbreak tespitine odaklı API. Saldırı örüntülerini Gandalf adlı '
        'oyunlaştırılmış deneyden toplanan gerçek veriyle besliyor.',
        'An API focused on prompt injection and jailbreak detection, fed by real attack data harvested from '
        'its gamified Gandalf experiment.', C)
    add('https://www.prompt.security/', 'Prompt Security', ['saas', 'ücretli', 'gizlilik', 'kurumsal'],
        'Çalışanların hangi YZ aracına ne veri gönderdiğini görünür kılıyor ve politikaya göre engelliyor. '
        'Gölge YZ kullanımını ölçmek isteyen kurumlar için.',
        'Surfaces which AI tools employees send what data to, and blocks by policy. '
        'Aimed at organisations that need to measure shadow AI use.', C)
    add('https://protectai.com/', 'Prisma AIRS (Protect AI)', ['saas', 'ücretli', 'tedarik-zinciri', 'mlops'],
        'Model dosyalarını zararlı yük için tarıyor — pickle serileştirmesi keyfî kod çalıştırabildiği için '
        'indirilen bir checkpoint gerçek bir saldırı yüzeyi. Protect AI 2025’te Palo Alto Networks’e katıldı; '
        'ürün artık Prisma AIRS çatısı altında.',
        'Scans model files for malicious payloads. Because pickle deserialisation can execute arbitrary code, '
        'a downloaded checkpoint is a real attack surface. Protect AI joined Palo Alto Networks in 2025; the '
        'product now lives under the Prisma AIRS umbrella.', C)
    add('https://azure.microsoft.com/products/ai-services/ai-content-safety', 'Azure AI Content Safety', ['saas', 'ücretli', 'guardrail', 'azure'],
        'Metin ve görseli dört zarar kategorisinde önem derecesiyle puanlayan sınıflandırıcı. '
        'Eşikleri kendin ayarlıyorsun; kendi moderasyon modelini eğitmeye alternatif.',
        'A classifier scoring text and images across four harm categories with severity levels. '
        'You set the thresholds yourself — an alternative to training your own moderation model.', C)
    add('https://aws.amazon.com/bedrock/guardrails/', 'AWS Bedrock Guardrails', ['saas', 'ücretli', 'guardrail', 'aws'],
        'İçerik filtresi, yasaklı konu listesi ve kişisel veri maskeleme; Bedrock dışındaki modellere de '
        'bağımsız API olarak uygulanabiliyor.',
        'Content filters, denied-topic lists and PII redaction — and it can be applied as a standalone API '
        'to models outside Bedrock too.', C)

    # ---------------------------------------------------------- observability
    add('https://smith.langchain.com/', 'LangSmith', ['saas', 'freemium', 'tracing', 'eval'],
        'Her zincir adımının girdi, çıktı, gecikme ve jeton sayısını ayrı ayrı gösteriyor. '
        'LangChain’e bağlı değil ama en sıkı entegrasyonu orada.',
        'Shows input, output, latency and token count for every chain step separately. '
        'Not tied to LangChain, though that is where the integration is tightest.', C)
    add('https://langfuse.com/', 'Langfuse', ['açık-kaynak', 'self-hosted', 'tracing', 'mit'],
        'Çatı bağımsız izleme ve değerlendirme; OpenTelemetry uyumlu. '
        'Kendi sunucunda çalıştırabildiğin için istem ve yanıt verisi dışarı çıkmıyor.',
        'Framework-agnostic tracing and evaluation, OpenTelemetry-compatible. '
        'Because you can self-host it, prompt and response data never leaves your infrastructure.', C)
    add('https://phoenix.arize.com/', 'Arize Phoenix', ['açık-kaynak', 'python', 'tracing', 'not-defteri'],
        'Not defterinin içinde çalışıp izleri yerelde gösteriyor. '
        'Gömme uzayını görselleştirip alma hatasının nereden geldiğini kümelenmeye bakarak buldurabiliyor.',
        'Runs inside a notebook and renders traces locally. It can visualise the embedding space so you find '
        'the source of a retrieval failure by looking at clustering.', C)
    add('https://wandb.ai/site/weave/', 'W&B Weave', ['saas', 'freemium', 'tracing', 'mlops'],
        'Weights & Biases’ın LLM tarafı. Zaten W&B ile eğitim izliyorsan, çıkarım izleri de '
        'aynı proje altında toplanıyor.',
        'The LLM side of Weights & Biases. If you already track training there, inference traces land under '
        'the same project.', C)
    add('https://www.trulens.org/', 'TruLens', ['açık-kaynak', 'python', 'eval', 'rag'],
        'RAG üçlemesini ölçüyor: bağlam alaka düzeyi, cevabın bağlama sadakati, cevabın soruya uygunluğu. '
        'Bu üçü ayrı ölçüldüğü için hatanın alma tarafında mı üretim tarafında mı olduğu ayrışıyor.',
        'Measures the RAG triad — context relevance, groundedness, answer relevance. Measuring them separately '
        'is what tells you whether the failure sits in retrieval or generation.', C)
    add('https://docs.ragas.io/', 'Ragas', ['açık-kaynak', 'python', 'eval', 'rag'],
        'RAG hatları için ölçüt kütüphanesi; referans cevap olmadan da çalışabilen metrikleri var. '
        'Sentetik test kümesi üretip değerlendirmeyi CI’ya bağlayabiliyorsun.',
        'A metrics library for RAG pipelines, including metrics that work without reference answers. '
        'It can generate a synthetic test set so evaluation runs in CI.', C)
    add('https://www.promptfoo.dev/', 'Promptfoo', ['açık-kaynak', 'cli', 'eval', 'ci'],
        'İstem ve modelleri YAML’de tanımlanmış test kümesine karşı yan yana koşuyor. '
        'Model sürümü değiştiğinde çıktının bozulup bozulmadığını CI adımında yakalıyor.',
        'Runs prompts and models side by side against a test set declared in YAML. '
        'It catches output regressions in a CI step when a model version changes.', C)
    add('https://www.helicone.ai/', 'Helicone', ['açık-kaynak', 'proxy', 'tracing', 'maliyet'],
        'Taban URL’yi değiştirmen yeterli; istekler üzerinden geçerken kaydediliyor. '
        'Kod değişikliği istememesi, mevcut bir projeye sonradan takmayı kolaylaştırıyor.',
        'Change the base URL and requests are logged as they pass through. Requiring no code change makes it '
        'easy to bolt onto a project after the fact.', C)

    # ---------------------------------------------------------- bellek
    add('https://mem0.ai/', 'Mem0', ['saas', 'freemium', 'bellek', 'agent'],
        'Konuşmadan çıkarılan olguları saklıyor, çelişenleri güncelliyor, alakasızları eliyor. '
        'Ham geçmişi biriktirmek yerine neyin hatırlanmaya değer olduğuna karar veren bir katman.',
        'Stores facts extracted from conversation, updates contradictions and drops the irrelevant. '
        'A layer that decides what is worth remembering instead of accumulating raw history.', C)
    add('https://github.com/mem0ai/mem0', 'Mem0 (kaynak)', ['açık-kaynak', 'github', 'python', 'bellek'],
        'Mem0’ın kendi altyapında çalıştırılabilen sürümü. Embedchain projesi de bu depoda birleşti, '
        'yani eski Embedchain bağlantıları buraya çıkıyor.',
        'The self-hostable version of Mem0. The Embedchain project was merged into this repository, '
        'so older Embedchain links land here.', C)
    add('https://www.getzep.com/', 'Zep', ['açık-kaynak', 'bellek', 'bilgi-grafiği'],
        'Zamansal bilgi grafiği tutuyor: bir olgunun ne zaman doğru olduğunu ve ne zaman geçersizleştiğini '
        'kaydediyor. Düz vektör belleği bu ayrımı yapamıyor.',
        'Maintains a temporal knowledge graph, recording when a fact held and when it was invalidated. '
        'Flat vector memory cannot make that distinction.', C)
    add('https://www.letta.com/', 'Letta', ['açık-kaynak', 'python', 'bellek', 'agent'],
        'MemGPT araştırmasının ürünleşmiş hâli. Bağlam penceresini işletim sistemi gibi yönetiyor: '
        'sıcak bilgiyi pencerede tutup gerisini harici depoya sayfalıyor.',
        'The productised form of the MemGPT research. It manages the context window like an operating system, '
        'keeping hot state in the window and paging the rest to external storage.', C)
    add('https://langchain-ai.github.io/langgraph/concepts/memory/', 'LangGraph Memory', ['dokümantasyon', 'bellek'],
        'Kısa vadeli (thread içi durum) ve uzun vadeli (thread’ler arası store) belleğin ayrımını '
        've hangisinin ne zaman kullanılacağını anlatan kavram sayfası.',
        'The concept page separating short-term memory (in-thread state) from long-term (a cross-thread store), '
        'and when each applies.', C)
    add('https://github.com/breferrari/obsidian-mind', 'Obsidian Mind', ['açık-kaynak', 'github', 'bellek', 'markdown'],
        'Kod asistanının belleğini bir Obsidian kasasında düz Markdown olarak tutuyor. '
        'Bellek servisi çalıştırmıyorsun; not dosyalarını kendin okuyup düzeltebiliyorsun.',
        'Keeps a coding agent’s memory as plain Markdown in an Obsidian vault. No memory service to run, '
        'and you can read and correct the notes yourself.', C)

    # ---------------------------------------------------------- vector & data stores
    add('https://www.pinecone.io/', 'Pinecone', ['saas', 'ücretli', 'vektör-db'],
        'Tam yönetilen vektör veritabanı; sunucusuz katmanında kapasite planlaması yapmıyorsun. '
        'İşletme yükü en düşük seçenek, buna karşılık verinin nerede durduğu üzerinde denetimin yok.',
        'A fully managed vector database whose serverless tier removes capacity planning. '
        'The lowest operational burden here, at the cost of control over where the data sits.', C)
    add('https://weaviate.io/', 'Weaviate', ['açık-kaynak', 'vektör-db', 'graphql'],
        'Gömme üretimini modül olarak içinde barındırabiliyor, yani ayrı bir gömme adımı kurmadan '
        'ham metin yazabiliyorsun. Sorgu arayüzü GraphQL.',
        'Can host embedding generation as a module, so you write raw text without standing up a separate '
        'embedding step. Its query interface is GraphQL.', C)
    add('https://qdrant.tech/', 'Qdrant', ['açık-kaynak', 'rust', 'vektör-db', 'apache-2'],
        'Rust ile yazılmış; yüklü meta veri filtrelemesini vektör aramasıyla birlikte yürütüyor. '
        'Bellek ayak izi düşük olduğu için küçük bir VPS’te ciddi koleksiyon taşıyabiliyor.',
        'Written in Rust, executing heavy metadata filtering alongside the vector search itself. '
        'Its low memory footprint lets a small VPS carry a serious collection.', C)
    add('https://milvus.io/', 'Milvus', ['açık-kaynak', 'vektör-db', 'k8s', 'ölçek'],
        'Depolama ve hesaplamayı ayıran dağıtık mimari; milyar ölçekli koleksiyonlar için tasarlanmış. '
        'Kubernetes gerektiriyor, küçük projelerde kurulum maliyeti kazancından büyük.',
        'A distributed architecture separating storage from compute, built for billion-scale collections. '
        'It wants Kubernetes; on a small project the setup cost exceeds the gain.', C)
    add('https://www.trychroma.com/', 'Chroma', ['açık-kaynak', 'python', 'vektör-db', 'gömülü'],
        'Uygulamanın içine gömülü çalışıyor, sunucu süreci yok — `pip install` sonrası kullanmaya başlıyorsun. '
        'Prototip için en hızlısı, üretim ölçeğinde başkasına devretmen gerekiyor.',
        'Runs embedded in your application with no server process — usable straight after `pip install`. '
        'Fastest for a prototype; at production scale you will hand off to something else.', C)
    add('https://github.com/pgvector/pgvector', 'pgvector', ['açık-kaynak', 'github', 'postgres', 'vektör-db'],
        'PostgreSQL’e vektör tipi ve HNSW/IVFFlat indeksleri ekleyen uzantı. '
        'Vektörü ilişkisel veriyle aynı işlemde (transaction) tutabilmek ayrı bir sistem işletmeye bedel.',
        'An extension adding a vector type plus HNSW and IVFFlat indexes to PostgreSQL. '
        'Keeping vectors in the same transaction as relational data is worth a lot against running a second system.', C)
    add('https://www.elastic.co/elasticsearch', 'Elasticsearch', ['freemium', 'arama', 'hibrit'],
        'BM25 anahtar kelime aramasıyla vektör aramasını tek sorguda birleştirip (hibrit arama) sonuçları '
        'RRF ile harmanlayabiliyor. Saf vektör veritabanlarının eksiği tam olarak bu ilk yarı.',
        'Combines BM25 keyword search with vector search in a single query and fuses the results with RRF. '
        'That keyword half is exactly what pure vector databases lack.', C)
    add('https://www.mongodb.com/products/platform/atlas-vector-search', 'Atlas Vector Search', ['saas', 'ücretli', 'vektör-db', 'nosql'],
        'Vektör indeksi belgelerin yanında duruyor, ayrı bir depoya kopyalama ve senkron tutma derdi kalkıyor. '
        'Yalnızca Atlas’ta, kendi kurduğun MongoDB’de yok.',
        'The vector index sits beside your documents, removing the copy-and-sync burden of a separate store. '
        'Atlas only — it is not in a self-managed MongoDB.', C)
    add('https://redis.io/', 'Redis', ['açık-kaynak', 'önbellek', 'veritabanı'],
        'Bellek içi veri yapısı deposu. YZ tarafında oturum durumu, hız sınırlama sayaçları ve '
        'yanıt önbelleği için kullanılıyor; vektör araması da modülle geliyor.',
        'An in-memory data structure store, used on the AI side for session state, rate-limit counters and '
        'response caching. Vector search arrives as a module.', C)
    add('https://www.postgresql.org/', 'PostgreSQL', ['açık-kaynak', 'sql', 'veritabanı'],
        'JSONB, tam metin arama ve pgvector ile birlikte tek bir veritabanının üç ayrı sistemin işini '
        'görebildiği noktaya gelmiş durumda. Erken aşamada mimariyi ciddi ölçüde sadeleştiriyor.',
        'With JSONB, full-text search and pgvector it now does the work of three separate systems. '
        'Early on, that simplifies architecture considerably.', C)
    add('https://neo4j.com/', 'Neo4j', ['freemium', 'graf-db', 'cypher'],
        'İlişkiler tabloda yabancı anahtar değil, birinci sınıf veri. Cypher sorgu diliyle çok adımlı '
        'ilişki gezinmeleri, SQL’de yazılacak iç içe JOIN’lere göre hem kısa hem hızlı.',
        'Relationships are first-class data, not foreign keys. Multi-hop traversals in Cypher are both shorter '
        'and faster than the nested JOINs the same question needs in SQL.', C)

    # ---------------------------------------------------------- otomasyon
    add('https://n8n.io/', 'n8n', ['açık-kaynak', 'self-hosted', 'otomasyon', 'docker'],
        'Görsel düğüm editörü; kendi sunucunda çalıştırdığında çalıştırma sayısı sınırsız. '
        'Düğüm içine JavaScript yazabiliyorsun, yani no-code duvarına toslamıyorsun.',
        'A visual node editor with unmetered executions when self-hosted. You can drop JavaScript into a node, '
        'so you do not hit the usual no-code wall.', C)
    add('https://docs.n8n.io/', 'n8n Dokümantasyonu', ['dokümantasyon', 'otomasyon'],
        'Düğüm referansı, kendi sunucuna kurulum ve kimlik bilgisi yönetimi. '
        'Kuyruk kipiyle ölçekleme bölümü üretimde çalıştıracaklar için önemli.',
        'Node reference, self-hosting and credential management. The queue-mode scaling section matters '
        'for anyone running it in production.', C)
    add('https://zapier.com/', 'Zapier', ['saas', 'freemium', 'otomasyon'],
        'En geniş entegrasyon kataloğu — bağlanmak istediğin niş SaaS büyük ihtimalle burada var. '
        'Fiyatlandırma görev başına, yani hacim arttıkça hızla pahalılaşıyor.',
        'The widest integration catalogue — the niche SaaS you want is probably already there. '
        'Pricing is per task, so it gets expensive quickly as volume grows.', C)
    add('https://www.make.com/', 'Make', ['saas', 'freemium', 'otomasyon'],
        'Senaryolar dallanma, döngü ve hata işleme taşıyabiliyor; Zapier’in doğrusal adım modeline göre '
        'karmaşık akışlarda daha rahat. Öğrenme eğrisi de buna paralel olarak dik.',
        'Scenarios carry branching, loops and error handling, which makes complex flows easier than Zapier’s '
        'linear steps. The learning curve is correspondingly steeper.', C)
    add('https://www.microsoft.com/power-platform/products/power-automate', 'Power Automate', ['saas', 'ücretli', 'otomasyon'],
        'SharePoint, Teams ve Dataverse bağlayıcıları yerleşik. Kurum zaten Microsoft 365’teyse '
        'lisans çoğu zaman ödenmiş oluyor — asıl tercih sebebi bu.',
        'SharePoint, Teams and Dataverse connectors are native. If the organisation is already on Microsoft 365 '
        'the licence is usually paid for — which is the real reason it gets chosen.', C)
    add('https://temporal.io/', 'Temporal', ['açık-kaynak', 'orkestrasyon', 'dayanıklı'],
        'İş akışı durumunu olay geçmişi olarak kaydediyor; süreç çökerse aynı noktadan devam ediyor. '
        'Günlerce süren ve yeniden başlatılamayan işlemler için tasarlanmış.',
        'Records workflow state as an event history, so a crashed process resumes at the same point. '
        'Built for multi-day operations that cannot simply be restarted.', C)
    add('https://airflow.apache.org/', 'Apache Airflow', ['açık-kaynak', 'python', 'orkestrasyon', 'etl'],
        'DAG’ları Python’da tanımlayıp zamanlıyorsun. Toplu veri hattında fiilî standart; '
        'olay güdümlü ve düşük gecikmeli işlerde hantal kalıyor.',
        'You define DAGs in Python and schedule them. The de facto standard for batch data pipelines, '
        'and clumsy for event-driven, low-latency work.', C)
    add('https://www.prefect.io/', 'Prefect', ['açık-kaynak', 'python', 'orkestrasyon'],
        'Akış sıradan bir Python fonksiyonu; dekoratör ekleyip orkestrasyona dahil ediyorsun. '
        'Airflow’un ayrı DSL’ini öğrenmeden yerel kodu üretime taşımak daha kısa.',
        'A flow is an ordinary Python function you decorate into orchestration. Moving local code to production '
        'is shorter than learning Airflow’s separate DSL.', C)
    add('https://kestra.io/', 'Kestra', ['açık-kaynak', 'orkestrasyon', 'yaml'],
        'Akışlar YAML’de bildirimsel olarak tanımlanıyor; dil bağımsız olduğu için Python olmayan '
        'ekiplerde de çalışıyor. Sürüm kontrolüyle iyi geçiniyor.',
        'Flows are declared in YAML, and being language-agnostic it works for teams that are not on Python. '
        'It sits well in version control.', C)
    add('https://pipedream.com/', 'Pipedream', ['saas', 'freemium', 'otomasyon', 'kod'],
        'Her adım Node.js ya da Python kodu olabiliyor ve npm/PyPI paketi çekebiliyor. '
        'Görsel otomasyonla gerçek kod arasındaki boşluğu kapatan seçenek.',
        'Any step can be Node.js or Python and can pull an npm or PyPI package. '
        'The option that closes the gap between visual automation and real code.', C)

    # ---------------------------------------------------------- agent tools & skills
    add('https://github.com/affaan-m/everything-claude-code', 'Everything Claude Code', ['açık-kaynak', 'github', 'agent', 'yapılandırma'],
        'Kod asistanları için yetenek, kural, bellek düzeni ve güvenlik ayarlarını tek pakette toplayan '
        'yapılandırma seti. Sıfırdan kurmak yerine üzerine budayarak başlanacak türden.',
        'A configuration bundle of skills, rules, memory layout and security settings for coding agents. '
        'The kind of thing you start from and prune, rather than assemble from scratch.', C)
    add('https://github.com/ComposioHQ/awesome-claude-skills', 'Awesome Claude Skills', ['github', 'awesome-liste', 'agent'],
        'Claude yeteneklerinin derlenmiş listesi. Neyin zaten yazıldığını görüp aynı şeyi '
        'ikinci kez yazmamak için bakılacak yer.',
        'A curated list of Claude skills — the place to check what already exists before writing the same thing twice.', C)
    add('https://github.com/obra/superpowers', 'Superpowers', ['açık-kaynak', 'github', 'agent', 'metodoloji'],
        'Agent’a serbest istem yerine adımlı bir geliştirme disiplini dayatan yetenek çatısı. '
        'Planlama, uygulama ve doğrulama aşamalarını ayırıyor.',
        'A skills framework imposing a stepwise development discipline instead of free-form prompting, '
        'separating planning, implementation and verification.', C)
    add('https://github.com/gsd-build/get-shit-done', 'Get Shit Done', ['açık-kaynak', 'github', 'agent', 'spec-driven'],
        'Şartname güdümlü geliştirme sistemi: önce spec yazdırıyor, sonra ona karşı kod ürettiriyor. '
        'Amaç, üretilen kodun ne yapması gerektiğini yazılı bir referansa bağlamak.',
        'A spec-driven development system: it has the agent write a spec first and generate code against it, '
        'so what the code should do is anchored to a written reference.', C)
    add('https://github.com/HKUDS/OpenSpace', 'OpenSpace', ['açık-kaynak', 'github', 'agent', 'bağlam'],
        'Hangi yeteneğin ne zaman yükleneceğine karar veren yönetim katmanı. '
        'Tüm yetenekleri bağlama doldurmak yerine seçici yükleyerek jeton maliyetini düşürüyor.',
        'A management layer deciding which skill loads when. Selective loading instead of stuffing every skill '
        'into context is where the token saving comes from.', C)
    add('https://github.com/blader/humanizer', 'Humanizer', ['açık-kaynak', 'github', 'yazım'],
        'Metinden yapay zeka yazımına özgü kalıpları (aşırı paralel yapı, gereksiz geçiş cümleleri, '
        'tekdüze ritim) temizleyen dar kapsamlı yetenek.',
        'A narrow skill stripping the tells of AI writing — over-parallel structure, filler transitions, '
        'uniform rhythm — from a text.', C)
    add('https://github.com/DietrichGebert/ponytail', 'Ponytail', ['açık-kaynak', 'github', 'agent'],
        'Agent’ı gereksiz soyutlama ve erken genelleme yapmaktan alıkoyan yetenek. '
        'Kod üretme eğilimini kısıtlayarak çıktının bakım maliyetini düşürmeyi hedefliyor.',
        'A skill that stops an agent inventing needless abstraction and premature generalisation, '
        'restraining its urge to produce code in order to lower maintenance cost.', C)
    add('https://github.com/shanraisshan/claude-code-best-practice', 'Claude Code Best Practice', ['github', 'rehber', 'agent'],
        'Kod asistanıyla çalışırken işe yarayan ve yaramayan yaklaşımları derleyen depo. '
        'Resmî doküman değil, saha notu niteliğinde.',
        'A repo collecting what does and does not work when pairing with a coding agent — field notes rather than official docs.', C)
    add('https://github.com/mvanhorn/last30days-skill', 'last30days', ['açık-kaynak', 'github', 'araştırma'],
        'Bir konuda son otuz günün Reddit, X ve YouTube içeriğini tarayan yetenek. '
        'Modelin eğitim kesim tarihiyle bugün arasındaki boşluğu kapatmak için.',
        'A skill sweeping the last thirty days of Reddit, X and YouTube on a topic — '
        'aimed at the gap between a model’s training cutoff and today.', C)
    add('https://github.com/evermind-ai/raven', 'Raven', ['açık-kaynak', 'github', 'agent', 'bellek'],
        'Bellek öncelikli agent koşum takımı; oturumlar arası öğrenmeyi ve kendi yapılandırmasını '
        'iyileştirmeyi merkeze alıyor.',
        'A memory-first agent harness centred on cross-session learning and refining its own configuration.', C)
    add('https://github.com/diegosouzapw/OmniRoute', 'OmniRoute', ['açık-kaynak', 'github', 'gateway', 'mit'],
        'Tek OpenAI uyumlu uç noktadan yüzlerce sağlayıcıya yönlendiriyor; birçoğu ücretsiz katmanlı. '
        'Sağlayıcı düşerse otomatik yedeğe geçmesi, tek bir API’ye bağımlılığı kırıyor.',
        'Routes one OpenAI-compatible endpoint to hundreds of providers, many with free tiers. '
        'Automatic failover when a provider drops is what breaks single-API dependence.', C)
    add('https://github.com/lyogavin/airllm', 'AirLLM', ['açık-kaynak', 'github', 'yerel-model', 'bellek'],
        '70B modeli 4 GB GPU’da çalıştırıyor: katmanları tek tek yükleyip işledikten sonra bellekten atıyor. '
        'Nicemlemeden farkı, ağırlıkların hassasiyetini düşürmemesi — bedeli ise yavaşlık.',
        'Runs a 70B model on a 4 GB GPU by loading one layer at a time and discarding it after use. '
        'Unlike quantisation it does not reduce weight precision; the cost is speed.', C)
    add('https://github.com/microsoft/BitNet', 'BitNet', ['açık-kaynak', 'github', 'araştırma', 'nicemleme'],
        'Ağırlıkları 1.58 bite (üç değere) indiren çıkarım çatısı. '
        'Çarpma işlemleri toplamaya dönüştüğü için CPU üzerinde kabul edilebilir hızda çalışıyor.',
        'An inference framework reducing weights to 1.58 bits (three values). Multiplications collapse into '
        'additions, which is why it runs at acceptable speed on CPU.', C)
    add('https://github.com/microsoft/call-center-ai', 'Call Center AI', ['açık-kaynak', 'github', 'ses', 'örnek'],
        'API çağrısıyla telefon araması başlatan agent örneği; konuşma tanıma, model ve sentez '
        'zincirini uçtan uca gösteriyor. Sesli agent mimarisi için çalışan bir referans.',
        'An agent that places phone calls from an API call, showing the speech-recognition → model → synthesis '
        'chain end to end. A working reference for voice-agent architecture.', C)
    add('https://amilabs.xyz/', 'AMI Labs', ['araştırma', 'dünya-modeli'],
        'Dil yerine fiziksel dünyayı modelleyen sistemler üzerine çalışan araştırma şirketi; '
        'robotik ve endüstriyel denetim tarafına bakıyor.',
        'A research company building systems that model the physical world rather than language, '
        'aimed at robotics and industrial control.', C)
    add('https://www.youtube.com/playlist?list=PL4cUxeGkcC9g4YJeBqChhFJwKQ9TRiivY', 'Agent Geliştirme (oynatma listesi)', ['video', 'ücretsiz', 'agent'],
        'Agent kurmayı adım adım gösteren video serisi; okumak yerine izleyerek başlamak isteyenler için.',
        'A video series building agents step by step, for people who would rather watch than read.', C)
