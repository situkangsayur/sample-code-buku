#!/usr/bin/env bash
# Bab 37: melihat delta di packfile Git.
# Membuat repo sementara dengan tiga versi satu file, menjalankan git gc,
# lalu menampilkan isi pack dengan git verify-pack -v.
set -euo pipefail
REPO=$(mktemp -d)
trap 'rm -rf "$REPO"' EXIT
cd "$REPO"
git init -q
git config user.name Contoh
git config user.email contoh@example.com
python3 -c "
import sys
sys.stdout.write(''.join('baris %04d isi file yang panjang\n' % i for i in range(500)))" > data.txt
git add data.txt && git commit -qm v1
sed -i 's/baris 0250/BARIS 0250/' data.txt && git commit -qam v2
echo "baris tambahan" >> data.txt && git commit -qam v3
echo "object loose sebelum gc: $(find .git/objects -type f | wc -l)"
git gc -q
# kolom: id, tipe, ukuran asli, ukuran di pack, offset, [kedalaman delta, base]
git verify-pack -v .git/objects/pack/*.idx | grep -E "blob|chain"
# uji: dua blob lama harus tersimpan sebagai delta
test "$(git verify-pack -v .git/objects/pack/*.idx | grep -c 'blob .* 1 [0-9a-f]\{40\}$')" -eq 2
echo "packfile_demo: uji lolos"
