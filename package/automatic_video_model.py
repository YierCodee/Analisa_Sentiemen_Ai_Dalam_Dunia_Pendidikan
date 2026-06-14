import os 
import pandas as pd
import pprint 
import googleapiclient.errors

from data_cleaner import ML_klasifikasi_video
from youtube_helper import get_video_ids, get_video_details, get_channel

def video_models(playlis_id_uploads = None, channel_id_user=None):
    print("\n Sedang mengambil data video")
    try:
        if channel_id_user:
            hasil = get_channel(channel_id_user)
            playlis_id_uploads = hasil['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        #Cek ke dua jika input benar" kosong
        elif not playlis_id_uploads:
            hasil = get_channel()
            playlis_id_uploads = hasil['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        print("\n Sedang Mengambil detail video")
        daftar_video = get_video_ids(playlis_id_uploads, target_count=100)
        df_video_lengkap = get_video_details(daftar_video)
        
        #KLASIFIKASI DENGAN MACHINE LEARNING
        print("\n>>> 🤖 Melakukan Klasifikasi dengan machine learning")
        df_video_lengkap['Kategori Video'] = df_video_lengkap["title"].apply(ML_klasifikasi_video)
        print(df_video_lengkap.to_string(index = False))

        #EXPORT DATA KE DALAM EXCEL
        print("\n Export--Data Ke Excel----")
        nama_folder = "Run"
        os.makedirs(nama_folder, exist_ok=True)
        nama_file_video = "Data Video.xlsx"
        path_simpan_video = os.path.join(nama_folder, nama_file_video)
        df_video_lengkap.to_excel(path_simpan_video, index=False)
        print(f"Data berhasil disimpan ke EXCEL '{path_simpan_video}")

        print("\n" + "!" * 60)
        print("⚠️  PERINGATAN SISTEM (MACHINE LEARNING DISCLAIMER):")
        print("   Hasil klasifikasi di bawah ini sepenuhnya diproses oleh model ML.")
        print("   Model Machine Learning tidak selalu 100% benar dan berpotensi")
        print("   mengalami bias atau salah prediksi (False Positive/Negative).")
        print("   Mohon lakukan pengecekan kembali secara manual pada hasil Excel!")
        print("!" * 60 + "\n")

        return df_video_lengkap
    except Exception as e:
        print(f"\n[Error Dalam Mengoalah Video] Gagal memproses video : {e}")
        return None