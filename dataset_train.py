# =====================================================================
# DATASET LATIHAN UNTUK JUDUL VIDEO (PENDIDIKAN vs BUKAN)
# =====================================================================
JUDUL_TRAIN = [
    # Tema Pendidikan / Sains / Sejarah
    "Is Alexander the Great's tomb finally discovered by archaeologists",
    "El Niño has officially arrived and it is going to change weather",
    "Severe storms and climate change triggers natural disaster",
    "New scientific study reveals how human brain processes memory",
    "Ancient Egyptian history secrets found inside hidden pyramid",
    "Deep space telescope captures birth of a new planet",
    
    # Tema Bukan Pendidikan
    "MTG calls Trump traitor for Epstein files handling",
    "US bases face second round of retaliatory Iranian strikes",
    "Donald Trump wins the presidential election debate",
    "Taylor Swift concert tickets breaking new world records",
    "Knicks pull off stunning victory in NBA playoffs last night",
    "Unboxing iPhone 17 Pro Max review and first impressions",
    "Iranians tell CNN how war has caused prices to increase"
]

KATEGORI_VIDEO_TRAIN = [
    "Pendidikan", "Pendidikan", "Pendidikan", "Pendidikan", "Pendidikan", "Pendidikan",
    "Bukan Pendidikan", "Bukan Pendidikan", "Bukan Pendidikan", "Bukan Pendidikan", "Bukan Pendidikan", "Bukan Pendidikan", "Bukan Pendidikan"
]

# =====================================================================
# DATASET LATIHAN UNTUK LOGICAL FALLACY KOMENTAR
# =====================================================================
KOMENTAR_TRAIN = [
    # Ad Hominem
    "Halah mukanya aja kayak gitu, paling nilainya bagus karena hoki",
    "Gak usah sok pintar deh, lu aja kuliah telat lulus dasar bodoh",
    "Argumenmu gak valid karena kamu kan cuma mahasiswa miskin",
    
    # Hasty Generalization
    "Temenku pake AI jadi males, emang semua generasi sekarang rusak karena AI",
    "Kemarin ketemu satu dosen pelit, emang semua dosen di kampus ini ga bener",
    "Netizen sekarang tuh emang suka langsung pukul rata semuanya salah",
    
    # False Dilemma
    "Kita harus pilih: mau melarang total AI atau membiarkan mahasiswa jadi bodoh",
    "Kalau kamu gak setuju sama pendapat menteri, berarti kamu musuh negara",
    "Pilihannya cuma dua: kuliah di top 10 atau masa depanmu suram total",
    
    # Appeal to Authority
    "Kata menteri kan AI bagus, jadi lu ga usah banyak protes",
    "Dia kan profesor terkenal, jadi apa pun yang dia omongin pasti bener",
    "Ikut kata rektor aja ga usah dipertanyakan lagi logikanya",
    
    # Tidak Mengandung Fallacy
    "Penggunaan ChatGPT bisa membantu asalkan kita tetap verifikasi manual hasilnya",
    "Menurut saya argumen itu masuk akal karena didukung oleh data statistik",
    "Diskusi yang sehat harusnya fokus pada topik, bukan menyerang personal orang lain"
]

KATEGORI_FALLACY_TRAIN = [
    "Ad Hominem", "Ad Hominem", "Ad Hominem",
    "Hasty Generalization", "Hasty Generalization", "Hasty Generalization",
    "False Dilemma", "False Dilemma", "False Dilemma",
    "Appeal to Authority", "Appeal to Authority", "Appeal to Authority",
    "Tidak Mengandung Fallacy", "Tidak Mengandung Fallacy", "Tidak Mengandung Fallacy"
]