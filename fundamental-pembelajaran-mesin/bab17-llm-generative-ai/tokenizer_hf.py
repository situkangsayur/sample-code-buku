"""Kode 14.2 - Memakai tokenizer model terlatih (Hugging Face) dan membandingkan jumlah token."""
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
teks = "Nasabah itu menutup rekeningnya."
ids = tok.encode(teks)
print(ids)
print(tok.convert_ids_to_tokens(ids))
print(len(teks.split()), "kata ->", len(ids), "token")
print("dapat dikembalikan utuh:", tok.decode(ids) == teks)

# Bandingkan kalimat bermakna sama dalam dua bahasa: ukur, jangan menebak.
pasangan = [
    ("The customer closed the account because of poor service.",
     "Nasabah menutup rekening karena layanannya buruk."),
    ("Students may take the thesis after passing the required credits.",
     "Mahasiswa boleh mengambil skripsi setelah lulus SKS yang disyaratkan."),
]
for en, idn in pasangan:
    print(f"EN {len(tok.encode(en)):3d} token | ID {len(tok.encode(idn)):3d} token")
