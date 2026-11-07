"""immudb: verified write/read dan riwayat versi satu key.
Jalankan server dulu: docker run -d -p 3322:3322 codenotary/immudb
Kredensial bawaan immudb hanya untuk lab; ganti di lingkungan lain."""
from immudb import ImmudbClient

c = ImmudbClient("localhost:3322")
c.login("immudb", "immudb")
c.verifiedSet(b"akad:1", b"120000000")      # klien memverifikasi bukti saat menulis
c.verifiedSet(b"akad:1", b"130000000")      # versi baru, versi lama tidak hilang
print(c.verifiedGet(b"akad:1"))             # nilai terbaru + verifikasi bukti
for e in c.history(b"akad:1", 0, 10, False):
    print(e.tx, e.value)
c.logout()
