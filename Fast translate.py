import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import keyboard
import mouse
import pyperclip
import time
from deep_translator import GoogleTranslator
import json
import os
import threading
import subprocess
import webbrowser
import sys
import winreg as reg
import requests

import pystray
from PIL import Image, ImageOps, ImageDraw

# --- AYARLAR VE VERİLER ---
AYAR_DOSYASI = 'ayarlar.json'
MEVCUT_SURUM = "6.2" 
GUNCELLEME_URL = "https://raw.githubusercontent.com/Metehan6634/FastTranslate/main/version.txt" 
ILETISIM_MAIL = "metehancakiriletisim@gmail.com" 

TUSLAR_1 = ["alt", "ctrl", "shift", "F1", "F2", "F3", "F4", "F5", "Mouse 4", "Mouse 5"] + list("abcdefghijklmnopqrstuvwxyz")
TUSLAR_2 = ["Yok"] + list("abcdefghijklmnopqrstuvwxyz") + ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
TUM_DILLER = ["auto", "tr", "en", "de", "fr", "ru", "es", "it", "ja", "ko", "zh-CN"]

DIL_METINLERI = {
    "tr": {
        "from": "Hangi Dilden:", "to": "Hangi Dile:", "key1": "1. Tuş:", "key2": "2. Tuş:",
        "voice": "Seslendirmen:", "speed": "Hız:", "read_aloud": "Sesli Oku",
        "save": "Kaydet", "waiting": "Bekleniyor...", "hide": "↘️ Gizle",
        "auto": "Otomatik Algıla", "saved": "Kaydedildi!",
        "settings_title": "Sistem ve Kişiselleştirme", "help_title": "Yardım",
        "help_text": "Tuşlarını seç ve kaydet.\nOyunda yazını yaz.\nEnter'a basmadan kısayoluna bas!",
        "about": "Hakkında", "update_check": "Güncellemeleri Otomatik Denetle"
    },
    "en": {
        "from": "From Language:", "to": "To Language:", "key1": "Key 1:", "key2": "Key 2:",
        "voice": "Voice Actor:", "speed": "Speed:", "read_aloud": "Read Aloud",
        "save": "Save", "waiting": "Waiting...", "hide": "↘️ Hide",
        "auto": "Auto Detect", "saved": "Saved!",
        "settings_title": "System & Personalization", "help_title": "Help",
        "help_text": "Select keys and save.\nType your text in game.\nPress your hotkey before hitting Enter!",
        "about": "About", "update_check": "Check for Updates Automatically"
    }
}

def kaynak_yolu(goreceli_yol):
    try: taban_yol = sys._MEIPASS
    except Exception: taban_yol = os.path.abspath(".")
    return os.path.join(taban_yol, goreceli_yol)

def ikon_yukle(dosya_adi, boyut=(22, 22)):
    tam_yol = kaynak_yolu(dosya_adi)
    try:
        orijinal_resim = Image.open(tam_yol).convert("RGBA")
        r, g, b, a = orijinal_resim.split()
        rgb_resim = Image.merge('RGB', (r, g, b))
        beyaz_rgb = ImageOps.invert(rgb_resim)
        r2, g2, b2 = beyaz_rgb.split()
        beyaz_resim = Image.merge('RGBA', (r2, g2, b2, a))
        return ctk.CTkImage(light_image=orijinal_resim, dark_image=beyaz_resim, size=boyut)
    except Exception as e: return None

def gercek_sesleri_bul():
    try:
        komut = 'powershell -Command "Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.GetInstalledVoices() | Foreach-Object { $_.VoiceInfo.Name }"'
        sonuc = subprocess.check_output(komut, shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        sesler = [satir.strip() for satir in sonuc.split('\n') if satir.strip()]
        return sesler if sesler else ["Microsoft Zira Desktop"]
    except: return ["Microsoft Zira Desktop"]

GERCEK_SES_LISTESI = gercek_sesleri_bul()

def ayarlari_yukle():
    varsayilan = {
        "tus1": "alt", "tus2": "t", "kaynak_dil": "auto", "hedef_dil": "en", 
        "okuma_hizi": 150, "ses_tipi": GERCEK_SES_LISTESI[0], "tema": "Dark", "renk_temasi": "blue",
        "arayuz_dili": "tr", "bildirim_goster": True, "baslangicta_calistir": False, 
        "seffaflik": 1.0, "yazi_boyutu": 12, "sesli_mod_aktif": False, "guncelleme_kontrol": True
    }
    if os.path.exists(AYAR_DOSYASI):
        try:
            with open(AYAR_DOSYASI, 'r') as dosya:
                ayarlar = json.load(dosya)
                for key in varsayilan:
                    if key not in ayarlar: ayarlar[key] = varsayilan[key]
                if ayarlar["kaynak_dil"] in ["Otomatik Algıla", "Auto Detect"]:
                    ayarlar["kaynak_dil"] = "auto"
                return ayarlar
        except: pass
    return varsayilan

ayarlar = ayarlari_yukle()
mevcut_arayuz_dili = ayarlar["arayuz_dili"]
APP_FONT = ("Arial", ayarlar["yazi_boyutu"])

def guncelleme_kontrolu():
    if not ayarlar.get("guncelleme_kontrol", True): return
    try:
        busting_url = f"{GUNCELLEME_URL}?t={time.time()}"
        response = requests.get(busting_url, timeout=3)
        if response.status_code == 200:
            en_yeni_surum = response.text.strip()
            if float(en_yeni_surum) > float(MEVCUT_SURUM):
                btn_guncelle.configure(text=f"🔥 v{en_yeni_surum} Güncellemesi Çıktı! Tıkla")
                btn_guncelle.pack(side="right", padx=10)
    except: pass 

def linke_git(): webbrowser.open("https://github.com/Metehan6634/FastTranslate")

tray_icon = None
def dummy_icon_olustur():
    image = Image.new('RGB', (64, 64), color = (43, 43, 43))
    d = ImageDraw.Draw(image)
    d.text((10,20), "FT", fill=(255,255,255))
    return image

def pencereyi_goster(icon, item):
    icon.stop()
    pencere.after(0, pencere.deiconify)

def programi_kapat_tray(icon, item):
    icon.stop()
    os._exit(0)

def sag_alta_gizle():
    pencere.withdraw()
    global tray_icon
    menu = pystray.Menu(
        pystray.MenuItem('Arayüzü Göster / Show UI', pencereyi_goster, default=True),
        pystray.MenuItem('Çıkış / Exit', programi_kapat_tray)
    )
    try: tepsi_ikonu = Image.open(kaynak_yolu("freepik__hızlı_çeviri_programım_var_ve_bunun_için_icon.ico"))
    except: tepsi_ikonu = dummy_icon_olustur()
    
    tray_icon = pystray.Icon("FastTranslate", tepsi_ikonu, "Fast Translate", menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()

def baslangic_ayarini_uygula(aktif_mi):
    try:
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        key = reg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        open_key = reg.OpenKey(key, sub_key, 0, reg.KEY_ALL_ACCESS)
        if aktif_mi: reg.SetValueEx(open_key, "FastTranslate", 0, reg.REG_SZ, exe_path)
        else:
            try: reg.DeleteValue(open_key, "FastTranslate")
            except: pass
        reg.CloseKey(open_key)
    except: pass

def arayuzu_guncelle():
    metin = DIL_METINLERI[mevcut_arayuz_dili]
    lbl_kaynak.configure(text=metin["from"])
    lbl_hedef.configure(text=metin["to"])
    lbl_tus1.configure(text=metin["key1"])
    lbl_tus2.configure(text=metin["key2"])
    lbl_ses.configure(text=metin["voice"])
    lbl_hiz.configure(text=metin["speed"])
    sesli_mod_aktif.configure(text=metin["read_aloud"])
    btn_kaydet.configure(text=metin["save"])
    btn_tepsi.configure(text=metin["hide"])
    
    mevcut_diller = TUM_DILLER.copy()
    mevcut_diller[0] = metin["auto"]
    kaynak_dil_secimi.configure(values=mevcut_diller)
    if ayarlar["kaynak_dil"] == "auto": kaynak_dil_secimi.set(metin["auto"])
    else: kaynak_dil_secimi.set(ayarlar["kaynak_dil"])
    if "Bekleniyor" in durum_etiketi.cget("text") or "Waiting" in durum_etiketi.cget("text"):
        durum_etiketi.configure(text=metin["waiting"])

def arayuz_dilini_degistir(dil_kodu):
    global mevcut_arayuz_dili
    mevcut_arayuz_dili = dil_kodu
    ayarlari_kaydet(sessiz=True)
    arayuzu_guncelle()

def ayarlari_kaydet(sessiz=False):
    global ayarlar, APP_FONT
    APP_FONT = ("Arial", ayarlar.get("yazi_boyutu", 12))
    kaynak_secim = kaynak_dil_secimi.get()
    if kaynak_secim in ["Otomatik Algıla", "Auto Detect"]: kaynak_kodu = "auto"
    else: kaynak_kodu = kaynak_secim

    ayarlar = {
        "tus1": tus1_secimi.get(), "tus2": tus2_secimi.get(),
        "kaynak_dil": kaynak_kodu, "hedef_dil": hedef_dil_secimi.get(),
        "okuma_hizi": int(hiz_kaydirici.get()), "ses_tipi": ses_secimi.get(),
        "tema": ctk.get_appearance_mode(), "renk_temasi": ayarlar.get("renk_temasi", "blue"),
        "arayuz_dili": mevcut_arayuz_dili,
        "bildirim_goster": ayarlar.get("bildirim_goster", True),
        "baslangicta_calistir": ayarlar.get("baslangicta_calistir", False),
        "seffaflik": ayarlar.get("seffaflik", 1.0), "yazi_boyutu": ayarlar.get("yazi_boyutu", 12),
        "sesli_mod_aktif": sesli_mod_aktif.get(),
        "guncelleme_kontrol": ayarlar.get("guncelleme_kontrol", True)
    }
    with open(AYAR_DOSYASI, 'w') as dosya: json.dump(ayarlar, dosya)
    if not sessiz:
        guncel_saat = time.strftime("%H:%M")
        mesaj = f"{DIL_METINLERI[mevcut_arayuz_dili]['saved']} ({guncel_saat})"
        durum_etiketi.configure(text=mesaj, text_color="#00ff00")
    kisayolu_guncelle()

def tema_degistir(secim):
    if secim in ["Dark", "Light"]:
        ctk.set_appearance_mode(secim)
        ayarlar["tema"] = secim
    ayarlari_kaydet(sessiz=True)

def yardim_goster():
    metin = DIL_METINLERI[mevcut_arayuz_dili]
    messagebox.showinfo(metin["help_title"], metin["help_text"])

def ayarlari_ac():
    metin = DIL_METINLERI[mevcut_arayuz_dili]
    ayar_win = ctk.CTkToplevel(pencere)
    ayar_win.title(metin["settings_title"])
    ayar_win.geometry("450x420") 
    ayar_win.attributes("-topmost", True)
    
    tabview = ctk.CTkTabview(ayar_win)
    tabview.pack(padx=10, pady=10, fill="both", expand=True)
    tab_genel = tabview.add("Genel Sistem")
    tab_gorunum = tabview.add("Görünüm & Tema")
    
    def start_up_toggle():
        ayarlar["baslangicta_calistir"] = cb_baslangic.get()
        baslangic_ayarini_uygula(cb_baslangic.get())
        ayarlari_kaydet(sessiz=True)
    cb_baslangic = ctk.CTkCheckBox(tab_genel, text="Windows Başladığında Arka Planda Çalıştır", command=start_up_toggle)
    if ayarlar.get("baslangicta_calistir", False): cb_baslangic.select()
    cb_baslangic.pack(pady=10, anchor="w", padx=20)
    
    def bildirim_toggle():
        ayarlar["bildirim_goster"] = cb_bildirim.get()
        ayarlari_kaydet(sessiz=True)
    cb_bildirim = ctk.CTkCheckBox(tab_genel, text="Oyun İçi Şeffaf Bildirimleri Aç", command=bildirim_toggle)
    if ayarlar.get("bildirim_goster", True): cb_bildirim.select()
    cb_bildirim.pack(pady=10, anchor="w", padx=20)

    def guncelleme_toggle():
        ayarlar["guncelleme_kontrol"] = cb_guncelleme.get()
        ayarlari_kaydet(sessiz=True)
        if not cb_guncelleme.get(): btn_guncelle.pack_forget() 
        else: threading.Thread(target=guncelleme_kontrolu, daemon=True).start()

    cb_guncelleme = ctk.CTkCheckBox(tab_genel, text=metin.get("update_check", "Güncellemeleri Otomatik Denetle"), command=guncelleme_toggle)
    if ayarlar.get("guncelleme_kontrol", True): cb_guncelleme.select()
    cb_guncelleme.pack(pady=10, anchor="w", padx=20)

    ctk.CTkLabel(tab_gorunum, text="Cam Efekti (Şeffaflık):").pack(pady=(10,0))
    def saydamlik_ayarla(deger):
        pencere.attributes("-alpha", float(deger))
        ayarlar["seffaflik"] = float(deger)
    slider = ctk.CTkSlider(tab_gorunum, from_=0.3, to=1.0, command=saydamlik_ayarla)
    slider.set(ayarlar["seffaflik"])
    slider.pack(pady=5)

    ctk.CTkLabel(tab_gorunum, text="Yazı Tipi Boyutu:").pack(pady=(10,0))
    def yazi_guncelle(v):
        ayarlar["yazi_boyutu"] = int(v)
        yeni_font = ("Arial", int(v))
        for widget in icerik.winfo_children():
            try: widget.configure(font=yeni_font)
            except: pass
    slider_yazi = ctk.CTkSlider(tab_gorunum, from_=10, to=20, number_of_steps=10, command=yazi_guncelle)
    slider_yazi.set(ayarlar.get("yazi_boyutu", 12))
    slider_yazi.pack(pady=5)

    ctk.CTkButton(ayar_win, text=metin["save"], command=lambda: [ayarlari_kaydet(sessiz=True), ayar_win.destroy()]).pack(pady=10)

def ekran_bildirimi_goster(metin):
    bildirim = ctk.CTkToplevel()
    bildirim.overrideredirect(True)
    bildirim.attributes("-topmost", True)
    bildirim.attributes("-transparentcolor", "black")
    bildirim.configure(fg_color="black")
    ekran_g, ekran_y = bildirim.winfo_screenwidth(), bildirim.winfo_screenheight()
    bildirim.geometry(f"+{ekran_g//2 - 200}+{ekran_y - 150}")
    ctk.CTkLabel(bildirim, text=metin, font=("Arial", 20, "bold"), text_color="#00ff00", bg_color="black").pack()
    bildirim.after(3500, bildirim.destroy)

def metni_seslendir(okunacak_metin, hiz, secilen_ses):
    try:
        win_hiz = int((hiz - 150) / 15)
        temiz_metin = okunacak_metin.replace("'", "").replace('"', "")
        komut = f'''powershell -Command "Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $v = $s.GetInstalledVoices() | Where-Object {{ $_.VoiceInfo.Name -eq '{secilen_ses}' }}; if($v) {{ $s.SelectVoice($v[0].VoiceInfo.Name) }}; $s.Rate = {win_hiz}; $s.Speak('{temiz_metin}')"'''
        subprocess.run(komut, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

# --- EFSANEVİ A BUG'INI ÇÖZEN YENİ ÇEVİRİ FONKSİYONU ---
def cevir_ve_yapistir():
    # 1. Aşama: Kullanıcının basılı tuttuğu tuşları (Alt, Ctrl, Shift) sanal olarak iptal et
    keyboard.release('alt')
    keyboard.release('ctrl')
    keyboard.release('shift')
    
    # Kısayol için atanmış tuşları da garanti olsun diye serbest bırakıyoruz
    try: keyboard.release(ayarlar.get("tus1", "alt"))
    except: pass
    try: keyboard.release(ayarlar.get("tus2", "t"))
    except: pass
    
    time.sleep(0.1) # Windows'un tuşları bıraktığımızı algılaması için mini bekleme

    kaynak_kodu = ayarlar.get("kaynak_dil", "auto")
    hedef_kodu = ayarlar.get("hedef_dil", "en")
    
    # 2. Aşama: Olası hatalara karşı eski panoyu (clipboard) hafızaya al
    eski_pano = pyperclip.paste()
    pyperclip.copy("") # Çeviri için panoyu tamamen sıfırla
    
    # 3. Aşama: Yazıyı seç ve kopyala
    keyboard.send('ctrl+a')
    time.sleep(0.05)
    keyboard.send('ctrl+c')
    time.sleep(0.1) # Kopyalamanın panoya düşmesi için ufak bir gecikme
    
    text = pyperclip.paste()
    
    # Eğer kopyalanan yazı boşsa, eski panoyu geri ver ve işlemi durdur (æ yazmasını önler)
    if not text or text.isspace():
        pyperclip.copy(eski_pano)
        return

    try:
        # 4. Aşama: Çeviriyi yap ve Yapıştır
        translation = GoogleTranslator(source=kaynak_kodu, target=hedef_kodu).translate(text)
        pyperclip.copy(translation)
        
        keyboard.send('backspace') # Bazen seçili metni silmez üstüne yazar, silmeyi garanti ediyoruz
        time.sleep(0.05)
        keyboard.send('ctrl+v')
        
        if ayarlar.get("bildirim_goster", True):
            ekran_bildirimi_goster(f"Çevrildi: {translation}")
            
        if sesli_mod_aktif.get():
            threading.Thread(target=metni_seslendir, args=(translation, hiz_kaydirici.get(), ses_secimi.get())).start()
    except Exception as e:
        pyperclip.copy(eski_pano) # Eğer internet koparsa veya çeviri çökerse, eski panoyu bozma

def kisayolu_guncelle():
    keyboard.unhook_all()
    t1, t2 = ayarlar.get("tus1", "alt"), ayarlar.get("tus2", "t")
    kombinasyon = t1 if t2 == "Yok" else f"{t1}+{t2}"
    try: keyboard.add_hotkey(kombinasyon.lower(), cevir_ve_yapistir)
    except: pass

# --- ARAYÜZ ---
pencere = ctk.CTk()
pencere.title("Fast Translate")
pencere.geometry("400x640") 
pencere.resizable(False, False)
pencere.attributes("-alpha", ayarlar["seffaflik"])
ctk.set_appearance_mode(ayarlar.get("tema", "Dark"))

img_tema = ikon_yukle("night-mode.png")
img_dil = ikon_yukle("language.png")
img_yardim = ikon_yukle("help-web-button.png")
img_ayar = ikon_yukle("setting.png")

ust_bar = ctk.CTkFrame(pencere, fg_color="transparent", height=40)
ust_bar.pack(fill="x", padx=10, pady=10)

btn_guncelle = ctk.CTkButton(ust_bar, text="", fg_color="#ff4757", hover_color="#ff6b81", command=linke_git)

btn_tema = ctk.CTkButton(ust_bar, text="" if img_tema else "🎨", image=img_tema, width=35, height=35, fg_color="transparent", hover_color=("gray80", "gray20"))
btn_tema.pack(side="left", padx=2)
t_menu = tk.Menu(pencere, tearoff=0, bg="#2b2b2b", fg="white", borderwidth=0)
t_menu.add_command(label="Karanlık Mod", command=lambda: tema_degistir("Dark"))
t_menu.add_command(label="Aydınlık Mod", command=lambda: tema_degistir("Light"))
btn_tema.configure(command=lambda: t_menu.post(btn_tema.winfo_rootx(), btn_tema.winfo_rooty() + 40))

btn_dil = ctk.CTkButton(ust_bar, text="" if img_dil else "🌐", image=img_dil, width=35, height=35, fg_color="transparent", hover_color=("gray80", "gray20"))
btn_dil.pack(side="left", padx=2)
d_menu = tk.Menu(pencere, tearoff=0, bg="#2b2b2b", fg="white", borderwidth=0)
d_menu.add_command(label="Türkçe Arayüz", command=lambda: arayuz_dilini_degistir("tr"))
d_menu.add_command(label="English UI", command=lambda: arayuz_dilini_degistir("en"))
btn_dil.configure(command=lambda: d_menu.post(btn_dil.winfo_rootx(), btn_dil.winfo_rooty() + 40))

btn_yardim = ctk.CTkButton(ust_bar, text="" if img_yardim else "❓", image=img_yardim, width=35, height=35, fg_color="transparent", hover_color=("gray80", "gray20"))
btn_yardim.pack(side="left", padx=2)
y_menu = tk.Menu(pencere, tearoff=0, bg="#2b2b2b", fg="white", borderwidth=0)
y_menu.add_command(label="Nasıl Kullanılır? / Help", command=yardim_goster)
y_menu.add_separator()
y_menu.add_command(label="✉️ Geri Bildirim / Feedback", command=lambda: webbrowser.open(f"mailto:{ILETISIM_MAIL}?subject=Fast Translate Geri Bildirim"))
y_menu.add_command(label="Hakkında", command=lambda: messagebox.showinfo("Hakkında", "Fast Translate v6.2\nCreated by Metehan"))
btn_yardim.configure(command=lambda: y_menu.post(btn_yardim.winfo_rootx(), btn_yardim.winfo_rooty() + 40))

btn_ayar = ctk.CTkButton(ust_bar, text="" if img_ayar else "⚙️", image=img_ayar, width=35, height=35, fg_color="transparent", hover_color=("gray80", "gray20"), command=ayarlari_ac)
btn_ayar.pack(side="left", padx=2)

icerik = ctk.CTkFrame(pencere, fg_color="transparent")
icerik.pack(fill="both", expand=True, padx=20)

fnt = ("Arial", ayarlar["yazi_boyutu"])

lbl_kaynak = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_kaynak.pack(pady=5)
kaynak_dil_secimi = ctk.CTkComboBox(icerik, values=TUM_DILLER, font=fnt, state="readonly")
kaynak_dil_secimi.pack()

lbl_hedef = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_hedef.pack(pady=5)
hedef_dil_secimi = ctk.CTkComboBox(icerik, values=TUM_DILLER, font=fnt, state="readonly")
hedef_dil_secimi.set(ayarlar["hedef_dil"])
hedef_dil_secimi.pack()

lbl_tus1 = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_tus1.pack(pady=5)
tus1_secimi = ctk.CTkComboBox(icerik, values=TUSLAR_1, font=fnt, state="readonly")
tus1_secimi.set(ayarlar["tus1"])
tus1_secimi.pack()

lbl_tus2 = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_tus2.pack(pady=5)
tus2_secimi = ctk.CTkComboBox(icerik, values=TUSLAR_2, font=fnt, state="readonly")
tus2_secimi.set(ayarlar["tus2"])
tus2_secimi.pack()

lbl_ses = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_ses.pack(pady=5)
ses_secimi = ctk.CTkComboBox(icerik, values=GERCEK_SES_LISTESI, font=fnt, state="readonly")
ses_secimi.set(ayarlar["ses_tipi"])
ses_secimi.pack()

lbl_hiz = ctk.CTkLabel(icerik, text="", font=fnt)
lbl_hiz.pack(pady=5)
hiz_kaydirici = ctk.CTkSlider(icerik, from_=30, to=300, number_of_steps=9)
hiz_kaydirici.set(ayarlar["okuma_hizi"])
hiz_kaydirici.pack()

sesli_mod_aktif = ctk.CTkCheckBox(icerik, text="", font=fnt)
if ayarlar.get("sesli_mod_aktif", False):
    sesli_mod_aktif.select()
sesli_mod_aktif.pack(pady=10)

btn_kaydet = ctk.CTkButton(icerik, text="", command=ayarlari_kaydet, font=fnt)
btn_kaydet.pack(pady=10)

durum_etiketi = ctk.CTkLabel(icerik, text="", font=fnt)
durum_etiketi.pack()

alt_frame = ctk.CTkFrame(pencere, fg_color="transparent")
alt_frame.pack(side="bottom", fill="x", padx=15, pady=10)

imza_etiketi = ctk.CTkLabel(alt_frame, text="Created by Metehan", font=("Arial", 10, "italic"), text_color="gray")
imza_etiketi.pack(side="left")

btn_tepsi = ctk.CTkButton(alt_frame, text="", width=50, height=24, fg_color="transparent", text_color="gray", hover_color=("gray80", "gray20"), command=sag_alta_gizle)
btn_tepsi.pack(side="right")

arayuzu_guncelle()
kisayolu_guncelle()

threading.Thread(target=guncelleme_kontrolu, daemon=True).start()

pencere.mainloop()
