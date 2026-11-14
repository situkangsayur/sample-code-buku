"""Algoritma 4.6 KelipatanTujuhPertama: break dan continue."""


def kelipatan_tujuh_pertama(a: list[int]) -> int:
    hasil = 0
    for x in a:
        if x <= 0:
            continue        # lewati bilangan nol dan negatif
        if x % 7 == 0:
            hasil = x
            break           # sudah ketemu
    return hasil


if __name__ == "__main__":
    assert kelipatan_tujuh_pertama([5, -14, 0, 21, 35]) == 21
    assert kelipatan_tujuh_pertama([-7, 3, 14, 0, 28]) == 14
    assert kelipatan_tujuh_pertama([1, 2, 3]) == 0
    assert kelipatan_tujuh_pertama([]) == 0
    print("break_continue.py: semua uji lolos")
