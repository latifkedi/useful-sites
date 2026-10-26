# Hakkında

<!-- ABOUT.md'nin Türkçesi: data/sitepages.py k/about.html sayfasını bundan, k/en/about.html sayfasını ABOUT.md'den üretir. Birini değiştiren ötekini de değiştirmeli. -->

## Neyi çözüyor

Bir bağlantının adı ve adresi ne olduğunu söylemez. `regex101.com` yazan bir
satır, site açılana kadar hiçbir şey anlatmaz. Oysa şu satır, açmaya değip
değmediğine saniyeler içinde karar verdirir:

> Bir düzenli ifadeyi parça parça açıklıyor; hata ayıklayıcısı eşleşmenin tam
> olarak nerede koptuğunu gösteriyor.

Dizindeki her kayıt bunu taşır: **kaynağın ne yaptığı** ve **benzerlerinden
nerede ayrıldığı.** Asıl yük ikincisinde. Aynı sorunu çözen birkaç araç
arasında seçim yapmak bir özellik listesi değil, aralarındaki ayrım çizgisini
ister.

## Kimin emeği

Bağlantılar elle seçildi ve derlendi. Açıklamalar, başlık düzeni, etiket
sözlüğü ve sitenin kendisi yapay zekâ yardımıyla üretildi ve yayımlanmadan önce
gözden geçirildi: metinler **makine yardımıyla yazılmış, insan tarafından
gözden geçirilmiştir.**

Bu, dizinin iddiası yüzünden önemli. Her kayıt bir karşılaştırma yargısı taşır
— "daha hafif", "aksine", "karşılığında" — ve bu yargılar insanın yazdığı değil,
makinenin üretip insanın gözden geçirdiği yargılardır. Projelerin kendi
belgelerine ve sitelerden alınan üst verilere dayanırlar, uydurma değildirler;
ama yine de yargıdırlar. Hüküm değil başlangıç noktası olarak okuyun; yanlış
olanı bir issue ile bildirin.

## Kim bakıyor

Dizine deponun sahibi, GitHub'da [latifkedi](https://github.com/latifkedi)
bakıyor. Arkasında bir kurum, sponsor ya da reklam yok; site izleyici ve
analitik taşımıyor.

## Kayıtlar nereden geliyor

Her kayıt onu getiren kaynağı taşır; kaynak kayıtta görünür ve süzgeç olarak
sunulur. Üç katman var ve aynı ölçüye tabi değiller:

- **Derleyenin kendi arşivi** — tek tek elden geçirilmiş bir yer imi
  koleksiyonu; her açıklama projenin kendi belgelerine bakılarak yazıldı.
- **Yayımlanmış derlemeler** — awesome-list benzeri herkese açık listeler.
  Yalnız kapsam içi, canlı ve kayda değer olanlar alındı; her biri denetlendi
  ve açıklaması kopyalanmadan burada yazıldı, ama özgün arşivin parçası değildi
  ve daha az ilk elden kullanım taşır.
- **Topluluk önerileri** — issue formuyla gelen öneriler. Hiçbiri kendiliğinden
  yayımlanmaz: bir kişi issue'yu okur, açıklamayı yazar ve kapsama uyup
  uymadığına karar verir.

Bunları eşitmiş gibi sunmak dizini olduğundan farklı gösterirdi; bu yüzden
ayrı tutuluyorlar. Derleme sırasında dışarıda bırakılanlar:

- Hesap isteyen paneller; okura bir yararları yok
- Arama motoru sonuç adresleri
- Kişisel dosya paylaşımları
- Canlılık denetiminden geçemeyen bağlantılar

## Kapsam

Bu bir "en iyi araçlar" listesi değil. Her başlıkta iki üç kayıt başlangıç
noktası olarak işaretli; anlamı "bu alanda yeniysen buradan başla", "mevcut
olanın en iyisi bu" değil.

## Bağlantılar nasıl denetleniyor

Bağlantı dizinlerinin ortak hastalığı çürümektir: bir süre sonra kayda değer
bir kısmı açılmaz olur ve derlemenin değeri gider.

Buna karşı üç düzenek çalışıyor.

Her hafta zamanlanmış bir iş bütün bağlantıları ister. Yanıt veren sayfa o
tarihte doğrulanmış sayılır ve tarih kayıtta gösterilir. 404, 410 ya da artık
çözülmeyen bir alan adı bağlantının aleyhine sayılır, ama onu ölü işaretlemek
için arka arkaya iki tarama gerekir: siteler bir öğleden sonra çökebilir.
Diğer hatalar — zaman aşımı, reddedilen bağlantı, bot görünce 403 dönen siteler
— ölü değil şüpheli olarak kaydedilir. İşaretlenen bir bağlantıyı bir kişi
tarayıcıda açıp sağlam bulduysa bu karar kaydedilir ve tarama onu bozamaz; ama
altı ay sonra yeniden bakılmak üzere sıraya girer. Böyle bir bağlantı ve tarayıcının geri çevrildiği bağlantılar,
insan kontrolünün değil, son taramanın tarihini gösterir.

Bağlantı verilen GitHub depoları ayrıca denetlenir, çünkü bir depo hiç 404
dönmeden bakımsız kalabilir — buradaki bir kayıt tam olarak böyle: sayfaları
hâlâ açılan, 76.000 yıldızlı ve Kasım 2025'te arşivlenmiş bir derleme. Bağlantı
denetimi bunu göremez; depo denetimi görür. Deposu arşivlenmiş, silinmiş ya da
iki yıldır güncellenmemiş kayıtlar bunu söyleyen bir rozet taşır.

Taramanın ölü bulduğu her şey sitenin kendisinde işaretlenir; ziyaretçi
bağlantıya tıkladıktan sonra değil, önce uyarılır. Her kayıt ayrıca bir Wayback
Machine bağlantısı taşır; hedefi kalıcı olarak gittiğinde de bir değeri kalır.

Bilerek çıkarılanlar ve gerekçeleri, haftalık özetlerle birlikte değişiklikler
sayfasında listeleniyor.

## Katkı ve sorun bildirmek

Sitedeki **Bağlantı Öner** düğmesi tek bir kaydı formla alır ya da bir yer imi
dışa aktarımını (`.html`, `.json`, `.csv`) okuyup dizinde zaten olanları ayıklar,
yalnız yenileri bırakır. Dosya tarayıcıda okunur ve hiçbir yere yüklenmez;
yüklenecek bir sunucu da yok.

Öneriler GitHub issue'su olarak açılır. Hiçbiri siteye kendiliğinden ulaşmaz:
issue okunur, açıklama yazılır ve kapsama uyuyorsa kayıt bir sonraki derlemeye
girer.

Öneri formu bir "farkı ne" alanı ister. Bilinmiyorsa öyle demek yeterli,
araştırılır — ama boş bırakılırsa kayıt dizinin var olma sebebini taşımaz.

Ölü bir bağlantı, yanlış bir açıklama ya da yerinde olmayan bir karşılaştırma en
iyi [GitHub'da bir issue](https://github.com/latifkedi/useful-sites/issues/new/choose)
olarak bildirilir; uygulamadaki her kayıtta formu doldurup açan bir "sorun
bildir" bağlantısı var.

---

*Derleme betikleri, veri düzeni ve kayıt ekleme yordamı:
[data/README.md](data/README.md).*
