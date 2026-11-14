"""Bab 36: object Git yang dialamatkan dengan hash (format SHA-1).

    id(object) = SHA-1( "<tipe> <panjang>\\0" + isi )
Blob berisi isi file. Tree berisi entri "<mode> <nama>\\0<20 byte id>"
yang diurutkan menurut nama. Uji membandingkan hasil hitungan sendiri
dengan perintah git asli di repo sementara.
"""
import hashlib
import os
import shutil
import subprocess
import tempfile
import zlib


def object_id(tipe, isi):
    header = b"%s %d\x00" % (tipe.encode(), len(isi))
    return hashlib.sha1(header + isi).hexdigest()


def blob_id(isi):
    return object_id("blob", isi)


def tree_id(entri):
    """entri: list (mode, nama, id_hex) untuk file biasa (tanpa subdirektori)."""
    isi = b""
    for mode, nama, oid in sorted(entri, key=lambda e: e[1].encode()):
        isi += b"%s %s\x00" % (mode.encode(), nama.encode()) + bytes.fromhex(oid)
    return object_id("tree", isi)


def git(repo, *args, data=None):
    hasil = subprocess.run(["git", "-C", repo, *args], input=data,
                           capture_output=True, check=True)
    return hasil.stdout.decode().strip()


if __name__ == "__main__":
    assert blob_id(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
    assert blob_id(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"

    if shutil.which("git") is None:
        print("git tidak ditemukan; uji pembanding dilewati")
    else:
        repo = tempfile.mkdtemp()
        try:
            git(repo, "init", "-q")
            git(repo, "config", "user.name", "Contoh")
            git(repo, "config", "user.email", "contoh@example.com")
            file_ = {"README.md": b"# Algoritma 101\n",
                     "bab35.txt": b"Git menyimpan snapshot.\n",
                     "angka.txt": b"1\n2\n3\n"}
            for nama, isi in file_.items():
                with open(os.path.join(repo, nama), "wb") as f:
                    f.write(isi)
            git(repo, "add", ".")
            for nama, isi in file_.items():
                assert git(repo, "hash-object", nama) == blob_id(isi)
            entri = [("100644", n, blob_id(i)) for n, i in file_.items()]
            assert git(repo, "write-tree") == tree_id(entri)

            # object loose disimpan terkompresi zlib (DEFLATE) di .git/objects
            oid = blob_id(file_["angka.txt"])
            path = os.path.join(repo, ".git", "objects", oid[:2], oid[2:])
            with open(path, "rb") as f:
                mentah = zlib.decompress(f.read())
            assert mentah == b"blob 6\x00" + file_["angka.txt"]

            # ubah satu byte: id blob, tree, dan seluruh rantai ikut berubah
            t1 = tree_id(entri)
            entri[2] = ("100644", "angka.txt", blob_id(b"1\n2\n4\n"))
            assert tree_id(entri) != t1
            print("tree:", t1)
        finally:
            shutil.rmtree(repo)
    print("git_object: semua uji lolos")
