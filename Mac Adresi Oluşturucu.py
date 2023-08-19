import random
from pathlib import Path

def mac_adresi_olusturucu(ayni_mac_kontrolu):
    sabit_mac = "00:1A:79"
    while True:
        mac_degerleri = [random.randint(0, 255) for _ in range(3)]  # Rastgele 3 bayt değer üretir.
        mac = sabit_mac + ":" + ":".join(f"{value:02X}" for value in mac_degerleri)
        if mac not in ayni_mac_kontrolu:
            ayni_mac_kontrolu.add(mac)
            return mac

def macleri_kaydet(mac_adresleri, dosya_dizini):
    with open(dosya_dizini, "w") as file:
        for mac in mac_adresleri:
            file.write(mac + "\n")  # MAC adreslerini belirtilen dosyaya kaydeder.

def olusturulacak_araligi_belirle(prefix, mac_baslangici, mac_sonu):
    mac_adresleri = []

    for i in range(mac_baslangici, mac_sonu + 1):
        mac_degerleri = format(i, "06X")  # Hex formatında sayıyı alır.
        mac_adresleri.append(f"{prefix}:{mac_degerleri[0:2]}:{mac_degerleri[2:4]}:{mac_degerleri[4:]}")  # MAC adresini oluşturur.

    return mac_adresleri

def get_unused_dosya_dizini_with_index(dosya_ana_adi):
    dosya_index = 0
    while True:
        dosya_dizini = dosya_ana_adi + ".txt" if dosya_index == 0 else dosya_ana_adi + f"({dosya_index}).txt"
        if not Path(dosya_dizini).is_file():
            return dosya_dizini  # Kullanılmamış dosya adını döndür
        dosya_index += 1

def main():
    ayni_mac_kontrolu = set()  # Üretilen MAC adreslerinin benzersiz olmasını kontrol etmek için.

    while True:
        print("[1] Rastgele MAC üret.")
        print("[2] Üreteceğin MAC aralığını kendin belirle.")
        choice = input("\nSeçiminizi yapın (Enter tuşuna basarak çıkabilirsiniz): ")

        if choice == "":
            break
        elif choice == "1":
            try:
                uretilecek_random_adres_sayisi = int(input("\nKaç adet MAC adresi üretmek istersiniz? "))
                mac_adresleri = [mac_adresi_olusturucu(ayni_mac_kontrolu) for _ in range(uretilecek_random_adres_sayisi)]
                dosyanin_adi = f"RANDOM{uretilecek_random_adres_sayisi}"
                dosya_dizini = get_unused_dosya_dizini_with_index(r"DİZİNİ BELİRLE" + dosyanin_adi) # Bu kısma, dosyayı kaydedeceğiniz dizini girin.
                macleri_kaydet(mac_adresleri, dosya_dizini)
                print(f"\nTamamdır. Dosya adı: {dosya_dizini}\n\n------------------------------\n")
            except ValueError:
                print("Hatalı giriş. Lütfen bir sayı girin.")
        elif choice == "2":
            try:
                mac_baslangici = int(input("Başlangıç değerini girin (0-FFFFFF): "), 16)
                mac_sonu = int(input("Bitiş değerini girin (0-FFFFFF): "), 16)
                if 0 <= mac_baslangici <= 0xFFFFFF and 0 <= mac_sonu <= 0xFFFFFF and mac_sonu >= mac_baslangici:
                    mac_adresleri = olusturulacak_araligi_belirle("00:1A:79", mac_baslangici, mac_sonu)
                    dosyanin_adi = f"{mac_baslangici:06X}-{mac_sonu:06X}"
                    dosya_dizini = get_unused_dosya_dizini_with_index(r"DİZİNİ BELİRLE" + dosyanin_adi) # Bu kısma, dosyayı kaydedeceğiniz dizini girin.
                    macleri_kaydet(mac_adresleri, dosya_dizini)
                    print(f"\nTamamdır. Dosya adı: {dosya_dizini}\n\n------------------------------\n")
                else:
                    print("Geçersiz değer aralığı.")
            except ValueError:
                print("Hatalı giriş. Geçerli bir sayı girin.")
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
