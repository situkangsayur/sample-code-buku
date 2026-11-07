"""Kode 5.8: retry dengan exponential backoff dan full jitter.

Demo: layanan palsu gagal dua kali lalu berhasil. Juga mencetak rentang jeda
untuk tiap percobaan agar dapat dibandingkan dengan soal latihan.

Pemakaian: python retry_backoff.py
"""
import random, time


class GalatSementara(Exception):
    ...


def dengan_retry(fungsi, maks=4, dasar=0.1, batas=2.0):
    for k in range(maks):
        try:
            return fungsi()            # fungsi wajib idempotent
        except GalatSementara:
            if k == maks - 1:
                raise                  # menyerah, biarkan pemanggil memutuskan
            jeda = random.uniform(0, min(batas, dasar * 2 ** k))
            print(f"  percobaan {k} gagal, tidur {jeda*1000:.0f} ms")
            time.sleep(jeda)


def layanan_palsu(gagal_sebanyak=2):
    hitung = {"n": 0}
    def panggil():
        hitung["n"] += 1
        if hitung["n"] <= gagal_sebanyak:
            raise GalatSementara()
        return f"berhasil pada panggilan ke-{hitung['n']}"
    return panggil


if __name__ == "__main__":
    print(dengan_retry(layanan_palsu()))
    print("rentang full jitter (dasar 100 ms, batas 2 s):")
    for k in range(6):
        print(f"  k={k}: 0 .. {min(2.0, 0.1 * 2 ** k)*1000:.0f} ms")
