import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# =====================================================================
# [INITIALIZATION] DEKLARASI VARIABEL GLOBAL (MENCEGAH NOT DEFINED)
# =====================================================================
vectorizer_video = None
model_video = None

vectorizer_komentar = None
model_komentar = None

print("=" * 60)
print(">>> MENYIAPKAN MODEL MACHINE LEARNING <<<")
print("=" * 60)

# ---------------------------------------------------------------------
# 1. SETUP CLASSIFIER UNTUK JUDUL VIDEO (PENDIDIKAN vs BUKAN)
# ---------------------------------------------------------------------
try:
    print("\n>>> 💻 Membaca dataset judul video dari CSV...")
    df_video = pd.read_csv("dataset_judul_video_500.csv")
    df_video = df_video.dropna(subset=['title', 'label'])
    
    vectorizer_video = TfidfVectorizer(stop_words='english')
    X_video_train = vectorizer_video.fit_transform(df_video['title'])
    model_video = MultinomialNB()
    model_video.fit(X_video_train, df_video['label'])
    print(f"   [SUKSES] Model klasifikasi video siap dengan {len(df_video)} data!")
except Exception as e:
    print(f"   [🚨 GAGAL INITIAL] Gagal melatih model video: {e}")
    print("   [INFO] Pastikan file 'dataset_video_keggle.csv' ada di folder dan memiliki kolom 'title' dan 'label'.")

# ---------------------------------------------------------------------
# 2. SETUP CLASSIFIER UNTUK LOGICAL FALLACY KOMENTAR
# ---------------------------------------------------------------------
try:
    print("\n>>> 💻 Membaca dataset logical fallacy dari CSV...")
    df_fallacy = pd.read_csv("dataset_logical_fallacy_500.csv")
    df_fallacy = df_fallacy.dropna(subset=['title', 'label'])
    
    vectorizer_komentar = TfidfVectorizer()
    X_komentar_train = vectorizer_komentar.fit_transform(df_fallacy['title'])
    model_komentar = MultinomialNB()
    model_komentar.fit(X_komentar_train, df_fallacy['label'])
    print(f"   [SUKSES] Model klasifikasi fallacy siap dengan {len(df_fallacy)} data!")
except Exception as e:
    print(f"   [🚨 GAGAL INITIAL] Gagal melatih model komentar: {e}")
    print("   [INFO] Pastikan file 'dataset_fallacy_keggle.csv' ada di folder dan memiliki kolom 'title' and 'label'.")

print("\n" + "=" * 60)
print(">>> PROSES INITIAL SELESAI. JIKA ADA LOG ERROR DI ATAS, HARAP PERIKSA CSV NYA <<<")
print("=" * 60 + "\n")


# =====================================================================
# [INTERFACE] FUNGSI SISTEM UTAMA DENGAN VALIDASI SAFETY CHECK
# =====================================================================

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-z0-9\s\d]', '', text)
    return text.strip()

def ML_klasifikasi_video(judul_video):
    """Prediksi Kategori Video dengan pengecekan ketersediaan model"""
    # Safety Check: Jika model gagal di-load di awal, langsung return default
    if vectorizer_video is None or model_video is None:
        return "Bukan Pendidikan"
        
    try:
        judul_bersih = clean_text(judul_video)
        if not judul_bersih:
            return "Bukan Pendidikan"
            
        vec = vectorizer_video.transform([judul_bersih])
        prediksi = model_video.predict(vec)
        label_asli_csv = prediksi[0]
        
        ai_keywords = ['ai', 'artificial intelligence', 'chatgpt', 'openai', 'llm', 
                       'machine learning', 'deep learning', 'copilot', 'prompting', 'bot']
        contains_ai = any(keyword in judul_bersih for keyword in ai_keywords)
        
        if label_asli_csv == "history":
            return "Pendidikan + AI" if contains_ai else "Pendidikan"
        else:
            return "Pendidikan + AI" if contains_ai else "Bukan Pendidikan"
    except Exception as e:
        print(f"ERROR ML VIDEO : {e}")
        return "Bukan Pendidikan"

def ML_klasfikasi_komentar(teks_komentar):
    """Prediksi Kategori Fallacy dengan pengecekan ketersediaan model"""
    # Safety Check: Jika model gagal di-load di awal, langsung return default
    if vectorizer_komentar is None or model_komentar is None:
        return "Tidak Mengandung Fallacy"
        
    try:
        komentar_bersih = clean_text(teks_komentar)
        if not komentar_bersih:
            return "Tidak Mengandung Fallacy"
            
        vec = vectorizer_komentar.transform([komentar_bersih])
        prediksi = model_komentar.predict(vec)
        return prediksi[0]
    except Exception as e:
        print(f"ERROR ML KOMENTAR : {e}")
        return "Tidak Mengandung Fallacy"