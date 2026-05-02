# 🛡️ VAD Manipülasyon Aracı (Anti-VAD Shield PID, Sys)

Adli bilişim süreçleri için bellek yapılarını ( Virtual Address Descriptor ) maskeleyerek, analiz araçlarına ve debugger'lara karşı geliştirilmiş gizlilik ve güvenlik sağlayan profesyonel bir manipülasyon aracıdır.

---

## Anti-VAD Öncesi:
![Before](https://i.hizliresim.com/lgpjc2v.png)
## Anti-VAD Sonrası:
![After](https://i.hizliresim.com/rkxz1br.png)

---

## 🛠️ Teknik:

Proje, Ring-3 seviyesinden kernel yapılarına müdahale eden hibrit bir mimari üzerine inşa edilmiştir.

### 1. Çekirdek Motor (Memory Manipulation Engine)
*   **Dinamik Link ve WinAPI :** Python `ctypes` kütüphanesi üzerinden `kernel32.dll` ve `ntdll.dll` kütüphanelerine doğrudan çağrılar yapılarak, işletim sistemi seviyesinde bellek yönetimi sağlanmaktadır.
*   **VAD (Virtual Address Descriptor) Maskeleme:** Hedef prosesin sanal bellek ağacı üzerinde iterasyon yapılarak, `PAGE_EXECUTE_READWRITE` (0x40) gibi riskli flag'ler, analiz araçlarını yanıltmak amacıyla `PAGE_GUARD` (0x100) koruma moduna dinamik olarak çekilmektedir.
*   **Güvenlik:** `OpenProcess` çağrılarında `PROCESS_ALL_ACCESS` (0x1F0FFF) yetkisiyle tutarlı handle yönetimi ve asenkron sonlandırma protokolleri uygulanmaktadır.

### 2. Host Mimarisi (Electron & Node.js)
*   **Inter-Process Communication:** Ana süreç ve arayüz arasındaki veri iletimi, `contextIsolation` ve `preload` köprüleri kullanılarak "Sandboxed" bir yapıda gerçekleştirilir; bu sayede DOM üzerinden sistem seviyesinde izinsiz komut çalıştırılması engellenir.
*   **Alt Süreç Yönetimi:** Python çekirdeği, Electron ana süreci tarafından `child_process.spawn` ile izole bir thread olarak başlatılır ve STDIO streamleri üzerinden gerçek zamanlı telemetri verisi sağlar.

### 3. Güvenlik ve Kod Sertleştirme (Hardening)
*   **AST (Abstract Syntax Tree) Manipülasyonu:** JavaScript kodları, `javascript-obfuscator` kullanılarak "Control Flow Flattening" ve "String Array Encryption" teknikleriyle statik analize karşı korunmaktadır.
*   **Binary Hardening:** Python servisleri, `PyInstaller` ile bağımsız binary formatına dönüştürülerek kaynak kod gizliliği ve taşınabilirlik optimize edilmiştir. Projeyi başka bir cihazdan derleyerek taşıyınız yada derledikten sonra klasörü kalıcı olarak temizleyiniz.

---

![Ana Görsel](https://i.hizliresim.com/1y0iq17.png)

---

## 📦 Kurulum ve Geliştirme Ortamı:

👉🏻 **Kurulum Dosyası:** ✅
[v1 Setup.exe](https://github.com/DoctorMemotaz/vad-pid-manipulasyon-araci/releases/download/v1/vad-manipulasyon-araci-Setup-1.0.0.exe)

---

### 👨🏻‍💻 Geliştiriciler için:

**Gereksinimler:**
*   [Node.js](https://nodejs.org/) (v18+)
*   [Python 3.x+](https://www.python.org/)
*   [PyInstaller](https://pyinstaller.org/) (`pip install pyinstaller`)

### 1. Yöntem: Git ile Klonlayın
Terminal veya komut istemcisini açıp şu komutu yapıştırın:
```bash
git clone [https://github.com/DoctorMemotaz/vad-pid-manipulasyon-araci.git](https://github.com/DoctorMemotaz/vad-pid-manipulasyon-araci.git)
```

### 2. Yöntem: ZIP Olarak İndir
Projeyi manuel olarak indirmek için aşağıdaki butonu veya bağlantıyı kullanın:
[Projeyi İndir (.zip)](https://github.com/DoctorMemotaz/vad-pid-manipulasyon-araci/archive/refs/heads/main.zip)

### 🔧 Build Adımları:

Projenin ana dizininde iken çalıştırmanız gereken terminal kodları:

```bash
npm install
```

```bash
npm run build:py
```

```bash
npm run build:js
```

```bash
npx electron-builder
```

**Dipnot 1:**

*  npm start ile test ortamında çalıştırmak için package.json dosyasında yer alan main alanı stage yerine core olması gerekmektedir. Geliştirme süreciniz tamamlandıktan sonra prod build'ini almak için yeniden stage yapmanız gerekir.

**Dipnot 2:**

*  Program kapatıldıktan sonra arka planda "kernel.exe" 'yi çalıştırmaya devam edebilir. Programı kapattıktan sonra görev yöneticisinden kernel.exe 'yi bulup işlemi sonlandırabilirsiniz.

---

Bu proje eğitim ve araştırma amaçlı geliştirilmiştir. Kullanımından doğacak tüm sorumluluk son kullanıcıya aittir.

---
