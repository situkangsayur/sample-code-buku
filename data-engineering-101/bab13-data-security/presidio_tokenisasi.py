"""Tokenisasi HMAC untuk kolom terstruktur dan pembersihan teks bebas dengan Presidio.
Persiapan: pip install presidio-analyzer && python -m spacy download en_core_web_lg
"""
import hashlib
import hmac
import os

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer

# PHONE_NUMBER bawaan Presidio memakai wilayah US, GB, DE, FR, IL, IN, CA, BR,
# sehingga nomor HP Indonesia "08..." tidak dikenali. Tambahkan recognizer pola sendiri
# (alternatif: PhoneRecognizer(supported_regions=["ID"])).
nik = PatternRecognizer(supported_entity="NIK",
                        patterns=[Pattern("nik", r"\b\d{16}\b", 0.6)])
hp = PatternRecognizer(supported_entity="NO_HP", patterns=[
         Pattern("hp", r"(?<![\d+])(?:\+62|0)8\d{8,11}\b", 0.6)])
an = AnalyzerEngine()
an.registry.add_recognizer(nik)
an.registry.add_recognizer(hp)
# Key HMAC wajib dari variabel lingkungan (diisi Vault/secret manager), tidak ditulis di kode.
# Untuk mencoba: export TOKEN_KEY="$(openssl rand -hex 32)"
KUNCI = os.environ["TOKEN_KEY"].encode()


def token(v: str) -> str:
    return "tok_" + hmac.new(KUNCI, v.encode(), hashlib.sha256).hexdigest()[:20]


def bersihkan(t: str) -> str:
    hs = an.analyze(t, language="en", entities=["NIK", "NO_HP"])
    for r in sorted(hs, key=lambda r: -r.start):
        t = t[:r.start] + f"<{r.entity_type}>" + t[r.end:]
    return t


def ukur(contoh):
    """contoh: list (teks, jumlah_pii_sebenarnya). Kembalikan jumlah temuan."""
    return sum(len(an.analyze(t, language="en", entities=["NIK", "NO_HP"]))
               for t, _ in contoh)


if __name__ == "__main__":
    print(token("3201011234560001"))
    print(token("3201011234560001"))   # konsisten: sama
    print(bersihkan("bayar kontrakan Bu Siti 081234567890"))
    print(bersihkan("transfer ke +6281234567890 untuk cicilan"))
    print(bersihkan("titipan NIK 3201011234560001 untuk akad"))
