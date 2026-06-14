import os
import pandas as pd

# Import fungsi-fungsi helper dari package kamu
from data_cleaner import ML_klasfikasi_komentar, clean_text
from youtube_helper import get_video_comments

def commentator_model(id_video_target, judul_video_target = "ID Video"):
    print("\n" + "=" * 50)
    print(f"--- 💬 MANUAL MODE (ENGLISH): Mengolah Komentar untuk ID: {id_video_target} ---")
    print("=" * 50)
    print("Sedang mengambil maksimal 2000 komentar dari video ini, mohon tunggu...")

    try:
        # 1. Ambil data komentar mentah bahasa Inggris dari YouTube API
        list_komentar_mentah = get_video_comments(id_video_target, target_count=2000)
        df_komentar = pd.DataFrame(list_komentar_mentah)

        if not df_komentar.empty:
            print(f"Sukses mengambil {len(df_komentar)} komentar mentah")

            print("Sedang membersihkan teks komentar bahasa Inggris...")
            df_komentar["Komentar Bersih"] = df_komentar["comment_mentah"].apply(clean_text)
               
            # 3. Klasifikasi Logical Fallacy Menggunakan Model ML
            print("\n>>> Melakukan Klasifikasi oleh Machine Learning (English Model)")
            df_komentar["Kategoti Fallcy"] = df_komentar["Komentar Bersih"].apply(ML_klasfikasi_komentar)

            # 4. EXPORT DATA KE DALAM EXCEL
            print("\n Export--Data Ke Excel----")
            nama_folder = "Run"
            os.makedirs(nama_folder, exist_ok=True)
            nama_file_video = "Data Komentar.xlsx"
            path_simpan_video = os.path.join(nama_folder, nama_file_video)
            df_komentar.to_excel(path_simpan_video, index=False)
            print(f"Data berhasil disimpan ke EXCEL '{path_simpan_video}'")

            print("\n" + "!" * 60)
            print("⚠️  PERINGATAN SISTEM (MACHINE LEARNING DISCLAIMER):")
            print("   Hasil klasifikasi di bawah ini sepenuhnya diproses oleh model ML.")
            print("   Model Machine Learning tidak selalu 100% benar dan berpotensi")
            print("   mengalami bias atau salah prediksi (False Positive/Negative).")
            print("   Mohon lakukan pengecekan kembali secara manual pada hasil Excel!")
            print("!" * 60 + "\n")
            
        else:
            print("🚨 Tidak ada komentar yang berhasil diambil. Pastikan ID Video benar dan video tidak privat.")
    
    except Exception as e:
         print(f"\n[Error Olah Komentar] Gagal memproses komentar: {e}")