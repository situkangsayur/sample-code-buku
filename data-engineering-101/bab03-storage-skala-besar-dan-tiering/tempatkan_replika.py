"""Simulasi kebijakan penempatan replika default HDFS (Kode 3.x).

Replika 1 di mesin penulis (atau acak), replika 2 di rak lain,
replika 3 di rak yang sama dengan replika 2 tetapi mesin berbeda.
"""
import random

KLASTER = {f"rak{r}": [f"r{r}n{n}" for n in range(1, 5)] for r in range(1, 4)}
RAK_DARI = {m: r for r, ms in KLASTER.items() for m in ms}


def tempatkan(penulis: str | None, rng: random.Random) -> list[str]:
    semua = list(RAK_DARI)
    r1 = penulis if penulis in RAK_DARI else rng.choice(semua)
    rak_lain = [m for m in semua if RAK_DARI[m] != RAK_DARI[r1]]
    r2 = rng.choice(rak_lain)
    serak_r2 = [m for m in KLASTER[RAK_DARI[r2]] if m != r2]
    r3 = rng.choice(serak_r2)
    return [r1, r2, r3]


if __name__ == "__main__":
    rng = random.Random(7)
    for blok in range(5):
        rep = tempatkan("r1n2", rng)
        print(f"blok b{blok}: {rep}  rak: {sorted({RAK_DARI[m] for m in rep})}")
    # Uji: bila satu rak padam, apakah setiap blok masih punya replika?
    blok = [tempatkan(None, rng) for _ in range(10_000)]
    for rak in KLASTER:
        hilang = sum(all(RAK_DARI[m] == rak for m in b) for b in blok)
        print(f"{rak} padam -> blok hilang: {hilang}")
