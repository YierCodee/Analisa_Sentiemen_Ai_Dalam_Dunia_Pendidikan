import pandas as pd

from youtube_helper import get_channel, get_video_ids, get_video_details
from package.automatic_komentar_model import commentator_model

def automatic_mode(channel_id_user):
    """Menggabungkan alur otomatis berdasarkan input manual ID channel dari user"""
    print(f"\n--- 🚀 Memulai Mode Otomatis untuk Channel: {channel_id_user} ---")
    try:
        # 1. Ambil data informasi channel awal berdasarkan input manual tadi
        hasil = get_channel(channel_id_user)
        if not hasil or 'items' not in hasil or len(hasil['items']) == 0:
            print("[Gagal] Channel tidak ditemukan atau API mengembalikan data kosong.")
            return
            
        playlist_id_uploads = hasil['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # 2.Panggil fungsi helper video, BUKAN memanggil automatic_mode lagi!
        print("\nMengambil daftar ID video dari playlist uploads...")
        daftar_video_ids = get_video_ids(playlist_id_uploads, target_count=100) 
        
        if not daftar_video_ids:
            print("[Gagal] Tidak ada video yang ditemukan di channel ini.")
            return
            
        print("Mengambil detail statistik untuk seluruh video...")
        df_video_lengkap = get_video_details(daftar_video_ids)
        
        if df_video_lengkap is None or df_video_lengkap.empty:
            print("[Gagal] Data detail statistik video tidak ditemukan, proses otomatis dihentikan.")
            return

        # 3. Cari video teramai berdasarkan jumlah komentar
        print("\n--- 🔎 Mencari Video Teramai untuk Dikupas Komentarnya ---")
        df_video_lengkap["commentCount"] = pd.to_numeric(df_video_lengkap["commentCount"], errors='coerce').fillna(0).astype(int)
        df_video_lengkap = df_video_lengkap.sort_values(by="commentCount", ascending=False)
       
        id_video_target = df_video_lengkap['video_id'].iloc[0]
        judul_video_target = df_video_lengkap['title'].iloc[0]
        
        print(f"🎯 Video Teramai Ditemukan: '{judul_video_target}' (ID: {id_video_target})")
        print(f"💬 Jumlah Komentar: {df_video_lengkap['commentCount'].iloc[0]} komentar.")
        
        # 4. 🎯 PERBAIKAN FATAL: Oper ke fungsi commentator_model milikmu, BUKAN ke automatic_mode!
        print("\n>>> Mentransfer data ke pengolah komentar...")
        commentator_model(id_video_target, judul_video_target)
        print("\n[SUKSES] Mode otomatis selesai dieksekusi total!")
        print("\n" + "!" * 60)
        print("⚠️  PERINGATAN SISTEM (MACHINE LEARNING DISCLAIMER):")
        print("   Hasil klasifikasi di bawah ini sepenuhnya diproses oleh model ML.")
        print("   Model Machine Learning tidak selalu 100% benar dan berpotensi")
        print("   mengalami bias atau salah prediksi (False Positive/Negative).")
        print("   Mohon lakukan pengecekan kembali secara manual pada hasil Excel!")
        print("!" * 60 + "\n")
                
    except Exception as e:
        print(f"\n[Sistem Error] Terjadi kesalahan tak terduga pada mode otomatis: {e}")