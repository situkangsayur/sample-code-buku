"""Kode 14.3 - Membangkitkan teks dengan GPT-2 dan berbagai strategi decoding (CPU cukup)."""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
masukan = tok("Machine learning is", return_tensors="pt")

torch.manual_seed(0)
for nama, opsi in [("greedy", dict(do_sample=False)),
                   ("T=0.7, top-p=0.9", dict(do_sample=True, temperature=0.7, top_p=0.9)),
                   ("T=1.5", dict(do_sample=True, temperature=1.5, top_k=0))]:
    keluaran = model.generate(**masukan, max_new_tokens=30,
                              pad_token_id=tok.eos_token_id, **opsi)
    print(f"[{nama}]", tok.decode(keluaran[0], skip_special_tokens=True), "\n")

with torch.no_grad():
    logit = model(**masukan).logits[0, -1]
p = logit.softmax(-1)
print("Lima token berikutnya teratas:")
for i in p.topk(5).indices:
    print(f"  {tok.decode(i)!r:12s} {p[i].item():.3f}")

# perplexity sebuah kalimat: exp(rata-rata cross-entropy per token)
kalimat = tok("Machine learning is a field of artificial intelligence.", return_tensors="pt")
with torch.no_grad():
    loss = model(**kalimat, labels=kalimat["input_ids"]).loss
print(f"cross-entropy {loss.item():.3f}, perplexity {torch.exp(loss).item():.1f}")
