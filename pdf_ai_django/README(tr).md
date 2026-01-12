# PDF AI Assistant

PDF AI Assistant, PDF'i yükledikten sonra sana onun hakkında özet çıkartan, ve yüklenen PDF/doc hakkında sana soru sormana izin veren yapay zeka destekli bir sitedir.

# Bilinmesi Gerekenler
- Ollama kullanılarak yapıldı
- Site tasarımı ClaudeAI sayesinde güncellenmiştir

# Lazım olanlar
- Python 3.11 ya da 3.12 (diğerleri sıkıntı çıkartabiliyor)

- Ollama

- 8GB+ RAM 

- 5GB+ boş disk alanı

# Nasıl Çalıştırılır?

**Önce:** requirments.txt dosyasında bulunan her şeyi indirin 
``` pip install -r requirements.txt ```

**İlk bash:**
```
python manage.py makemigrations documents
```

**İkinci bash:**
```
python manage.py migrate
```

**Son bash:**
```
python manage.py runserver
```

**Ekstra:** 
``` 
python manage.py createsuperuser 
```

# Özellikler
- PDF yükleyebilme (100MB kadar)
- Dosya adına göre otomatik başlık oluşturma
- Sayfa & chunk tracking
- Kolay belge yönetimi

# AI Destekli Özellikler

- **Otomatik Özet Oluşturma:** eğer dökümanı yüklediğin zaman soru sorarak yüklemiyorsan, sistem direkt PDF'in özetini çıkartarak başlıyor.

- **Soru cevap özelliği:** Sisteme soru sorduğun zaman, yüklediğin PDF hakkında, PDF'te bulunan bilgilerle cevap alırsın.


# Sohbet Arayüzü

- Pop-AI sitesinden esinlenmiş bir Chatbot konuşma paneli var.

- Gerçek zamanlı sohbet balonları: Tıpkı mesajlaşmak gibi

- Soru geçmişi takibi: Eski sorduğun sorulara ve konuşmalara bakabilirsin



# Admin Paneli

- Django admin 
- Tüm belgeleri yönetme
- Tüm soruları görüntüleme

# Site Nasıl kullanılır?

- Öncellikle herhangi bir PDF dosyasını, sitede solda bulunan **"Upload&Process"** kısmına yükleyin ve butona basın
- Yapay zekanın size cevap vermesini bekleyin
- Eğer sorunuz varsa, çıkan konuşma paneline yazabilirsiniz
- **Ask Questions** kısmında chunk sayısı ayarlanabiliyor
- Eğer PDF dosyasını yollamadan önce **Ask Questions** kısmına soru yazarak yollarsanız, özet yerine sorunuzun cevabı gelir