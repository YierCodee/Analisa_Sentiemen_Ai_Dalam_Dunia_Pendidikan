import pandas as pd
import googleapiclient.errors
from IPython.display import JSON
import json
import time 
import pprint
from dateutil import parser

#visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
import warnings



def tampilan_menu():
    print("\n" + "="*50)
    print("🤖 TOOL ANALISIS LOGICAL FALLACY YOUTUBE 🤖")
    print("="*50)
    print("[1] 🚀 Mode Otomatis (Cari Video Teramai + Ambil Komen + Analisis AI)")
    print("[2] 📹 Mode Manual: Hanya Tarik Daftar Video Channel (Cari ID Video)")
    print("[3] 💬 Mode Manual: Hanya Ambil Komen & Analisis AI (Masukkan ID Video)")
    print("[4] ❌ Keluar")
    print("="*50)

def main():
    while True:
        tampilan_menu()
        pilihan = input("Pilih mode (1/2/3/4): ").strip()
        
        if pilihan == '1':
            print("\n--🚀 Mode Otomatis--")
            username = input("Masukkan ID Channel : ").strip()
        elif pilihan == '2':
             print("Generate Data Vdeo")
             username = input("Masukkan ID Video").strip()
             print(f"\n Sedang Menarik data video mohon tunggu sebentar {username}").strip()
        elif pilihan == "3":
             print("Ambil Komen dan analisa machine learning")
             video_id = input("Masukkan ID Youtube").strip()
             print(f"\nMenarik komentar dan menjalakan fallcy dengan machine learing")
        else:
            print(f"\nTerima kasih telah menggunakan tools ini")
             

            
            