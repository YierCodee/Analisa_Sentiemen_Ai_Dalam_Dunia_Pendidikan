import pandas as pd
import googleapiclient.errors
from IPython.display import JSON

#visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

from package.automatic_model import automatic_mode
from package.automatic_video_model import video_models
from package.automatic_komentar_model import commentator_model

def tampilan_menu():
    print("\n" + "="*50)
    print("🤖 TOOL ANALISIS LOGICAL FALLACY YOUTUBE 🤖")
    print("="*50)
    print("[1] 🚀 Mode Otomatis (Cari Video Teramai + Ambil Komen + Analisis Sentimen)")
    print("[2] 📹 Mode Manual: Hanya Ambil Daftar Video Channel (Cari ID Video)")
    print("[3] 💬 Mode Manual: Hanya Ambil Komen & Analisis AI (Masukkan ID Video)")
    print("[4] ❌ Keluar")
    print("="*50)

def main():
    while True:
        tampilan_menu()
        pilihan = input("Pilih mode (1/2/3/4): ").strip()
        if pilihan == '1':
            print("\n--🚀 Mode Otomatis--")
            channel_input = input("Masukkan ID Channel Disini : ").strip()
            if channel_input:
               automatic_mode(channel_id_user=channel_input)
            else:
                print("❌ ID Channel tidak boleh kosong!")       
            print(f"\n Sedang Menarik data video mohon tunggu sebentar")
        elif pilihan == '2':
             print("Generate Data Video")
             channel_input = input("Masukkan ID Channel Disini : ").strip()
             if channel_input:
                video_models(channel_id_user=channel_input)
             else:
                print("❌ ID Channel tidak boleh kosong!")       
             
             print(f"\n Sedang Menarik data video mohon tunggu sebentar")
        
        elif pilihan == "3":
             print("Generate komentar dan analisa machine learning")
             id_input = input("Masukkan ID Video : ").strip()
             if id_input:
                commentator_model(id_input)
             else:
                 print ("ID video tidak ada")
             print(f"\nMenarik komentar dan menjalakan fallcy dengan machine learing")
        elif pilihan == '4':
             print("\n👋 Terima kasih telah menggunakan tool ini. Sampai jumpa")
             break
        else:
            print(f"\nTerima kasih telah menggunakan tools ini") 
if __name__ == "__main__":
    main()

            
            