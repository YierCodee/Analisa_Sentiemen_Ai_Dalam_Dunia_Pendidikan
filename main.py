import pandas as pd
import googleapiclient.errors
from IPython.display import JSON
import json
import time 
import pprint
from dateutil import parser
import os

#visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

from youtube_helper import get_channel, get_video_comments, get_video_ids, get_video_details, api_key
from data_cleaner import clean_text, ML_klasifikasi_video, ML_klasfikasi_komentar

if __name__ == "__main__":
    print("--- Memulai Proses Pengambilan Data YouTube ---")
    
    if not api_key or api_key == "MASUKKAN_API_KEY_GOOGLE_KAMU_DISINI":
        print("\n[Peringatan] Kamu belum memasukkan API Key!")
    else:
        try:
            # 1. Ambil data mentah dari API
            hasil = get_channel()
            print("\n--- Koneksi Sukses! Mengekstrak Data ke Tabel... ---")
            
            # 2. Proses Pengekstrakkan Data (Kode kamu ditaruh di sini)
            data_all = []
            playlist_id_uploads = ""
            for item in hasil['items']:
                playlist_id_uploads = item['contentDetails']['relatedPlaylists']['uploads'] # Ambil playlist ID untuk nanti digunakan mengambil video terbaru
                data = {
                    'channelName': item['snippet']['title'],
                    'subscribers': item['statistics']['subscriberCount'],
                    'views': item['statistics']['viewCount'],
                    'totalVideo': item['statistics']['videoCount'],
                    'playlistID': playlist_id_uploads
                }
                data_all.append(data)
            
            # Pandas
            df_channel= pd.DataFrame(data_all)
            # Tabel Terminal
            print("\n --- Data Channel YouTube ---")
            print(df_channel.to_string(index=False)) # Menggunakan to_string() agar tercetak rapi bentuk tabelnya
            print("-" * 50)

            #Mengambil 50 ID 
            print ("\n--- Mengambil 50 Video Terbaru dari Channel ---")
            playlistID = df_channel['playlistID'][0] # Ambil playlist ID dari Data

            daftar_video = get_video_ids(playlistID)
            print(f"\nBerhasil mengambil {len(daftar_video)} video terbaru dari channel")
            print ("\n--- Daftar Video IDs ---")
            pprint.pprint(daftar_video)

            #detail video
            print("\n--- Mengambil Detail Video ---")
            daftar_video = get_video_ids(playlist_id_uploads)
            print("\nMengambil detail data statistik dari 50 video...")
            df_video_lengkap = get_video_details(daftar_video)
            # -------------------------------------------------------------
            #  video classification by machine learning
            # -------------------------------------------------------------
            print("\n>>>  🤖 : Mengklasifikasikan Kategori Video...")
            df_video_lengkap["Kategori Video"] = df_video_lengkap["title"].apply(ML_klasifikasi_video)
            print("\n--- HASIL DATA DETAIL VIDEO ---")
            print(df_video_lengkap.to_string(index=False))  

            #Export Ke Excel
            print("\n--- Export To Excel ---")
            nama_folder = "Run"
            nama_file_video = "data_video_lengkap.xlsx"
            path_simpan_video = os.path.join(nama_folder, nama_file_video)
            df_video_lengkap.to_excel(path_simpan_video, index=False)
            print(f"Data berhasil diekspor ke '{path_simpan_video}'")
            
            # -------------------------------------------------------------
            # TAHAP B: KOMENTAR (KUPAS DARI VIDEO TERPOPULER)
            # -------------------------------------------------------------
            #FUNGSI UNTUK MENGOLAH KOMENTAR
            print ("\n" + "=" *50)
            print("\n--- Mengolah Komentar ---")
            print("=" *50)
            print("\n--- Sedang Mengolah Komentar Mohon Tunggu Sebentar ---")
            
            #Sorting video berdasarkan jumlah komentar terbanyak
            df_video_lengkap["commentCount"] = pd.to_numeric(df_video_lengkap["commentCount"], errors='coerce').fillna(0).astype(int) # Pastikan commentCount dalam bentuk numerik
            df_video_lengkap = df_video_lengkap.sort_values(by="commentCount", ascending=False)
           
            #Mengambi ID video
            id_video_target = df_video_lengkap['video_id'].iloc[0] # Ambil ID video pertama sebagai contoh
            judul_video_target = df_video_lengkap['title'].iloc[0] # Ambil judul video pertama sebagai contoh
            print (f"Target Video: {judul_video_target} (ID: {id_video_target})")
            print("Sedang mengambil maksimal 1000 komentar dari video ini")
            
            # Ambil komentar video
            list_komentar_mentah = get_video_comments(id_video_target, target_count=3000)
            df_komentar = pd.DataFrame(list_komentar_mentah)
            if not df_komentar.empty:
                print(f"Sukses mengambil {len(df_komentar)} komentar mentah")

                #CLEANING TEXT 
                print("Sedang membersihkan teks komentar...")
                df_komentar["Komentar Bersih"] = df_komentar["comment_mentah"].apply(clean_text)

                # -------------------------------------------------------------
                # KLASIFIKASI LOGICAL FALLACY 
                # -------------------------------------------------------------
                print("\n>>> ML Lokal: Mendeteksi Logical Fallacy")
                df_komentar["Kategori Fallacy"] = df_komentar["Komentar Bersih"].apply(ML_klasfikasi_komentar)

                #EKSPOR DATA KOMENTAR KE EXCEL
                nama_folder = "Run"
                nama_file_komentar = "DATA_KOMENTAR_BERSIH.xlsx"
                path_simpan = os.path.join(nama_folder, nama_file_komentar)
                df_komentar.to_excel(path_simpan, index=False)
                print(f"Data komentar berhasil diekspor ke '{path_simpan}'")
            else:
                print("Tidak ada komentar yang berhasil diambil untuk video ini.")
            
                # Validasi ERROR
        except googleapiclient.errors.HttpError as http_err:
            print(f"\n[API Error] Terjadi kesalahan pada layanan YouTube API: {http_err}")
        except Exception as e:
            print(f"\n[Sistem Error] Terjadi kesalahan tak terduga: {e}")

        