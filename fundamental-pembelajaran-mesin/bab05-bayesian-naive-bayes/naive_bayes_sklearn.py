"""Naive Bayes multinomial dengan scikit-learn (Bab 5, Kode 5.3)."""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

teks = ["menang hadiah gratis", "gratis hadiah klik sekarang", "klik gratis menang",
        "rapat besok pagi", "jadwal rapat proyek", "kirim laporan proyek besok"]
label = ["spam", "spam", "spam", "bukan", "bukan", "bukan"]

model = make_pipeline(CountVectorizer(), MultinomialNB(alpha=1.0))  # alpha=1: Laplace
model.fit(teks, label)

uji = ["gratis klik hadiah", "gratis rapat besok"]
print(model.classes_)
print(model.predict_proba(uji).round(3))

# Kata dengan bukti terkuat untuk kelas spam: selisih log P(w|spam) - log P(w|bukan)
vek, nb = model.named_steps["countvectorizer"], model.named_steps["multinomialnb"]
i_spam = list(nb.classes_).index("spam")
selisih = nb.feature_log_prob_[i_spam] - nb.feature_log_prob_[1 - i_spam]
kata = vek.get_feature_names_out()
for j in selisih.argsort()[::-1][:3]:
    print(f"{kata[j]:10s} {selisih[j]:+.2f}")
