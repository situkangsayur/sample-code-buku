# Bab 7 - Replikasi, Konsistensi, Konsensus, dan Kubernetes

Contoh kode untuk Bab 7 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `python/jam_logis.py` | Lamport clock dan vector clock, contoh tiga proses dan deteksi konflik | Kode 7.1, Algoritma 7.1, Gambar 7.1 |
| `python/quorum_sim.py` | Simulasi quorum: seberapa sering pembaca melihat versi usang untuk berbagai N, W, R | Subbab 7.2.3, Gambar 7.3 |
| `python/raft_pemilihan.py` | Simulasi pemilihan leader Raft dengan election timeout acak | Algoritma 7.2 |
| `go/etcdlock/` | Distributed lock dan pemilihan leader dengan etcd (Go) | Kode 7.2 |
| `python/consistent_hash.py` | Consistent hashing dengan virtual node, dibandingkan hash mod N | Kode 7.3, Gambar 7.9 |
| `katalog/` | Layanan katalog Go (`/item/{id}`, `/healthz`, `/readyz`, berhenti rapi saat SIGTERM) dan Dockerfile multi-stage | Kode 7.4 |
| `k8s/deployment.yaml` | Deployment tiga replika dengan probe, resources, dan topologySpreadConstraints | Kode 7.5 |
| `k8s/service.yaml` | Service `katalog` | Kode 7.6 |
| `k8s/hpa.yaml` | HorizontalPodAutoscaler berbasis CPU (target 70%) | Kode 7.7 |
| `kind-sister.yaml` | Klaster kind tiga node (satu control plane, dua worker) | Subbab 7.7 |
| `praktikum.sh` | Praktikum self-healing: deploy, beban dari dalam klaster, matikan pod, hitung kegagalan | Kode 7.8 |

## Menjalankan contoh Python dan Go

```bash
python python/jam_logis.py
python python/quorum_sim.py
python python/raft_pemilihan.py 5 3
python python/consistent_hash.py

# etcd lokal, lalu dua replika yang berebut menjadi leader
docker run -d --name etcd -p 2379:2379 quay.io/coreos/etcd:v3.5.17 \
  etcd --advertise-client-urls http://0.0.0.0:2379 --listen-client-urls http://0.0.0.0:2379
(cd go/etcdlock && go run . replika-1)   # terminal 1
(cd go/etcdlock && go run . replika-2)   # terminal 2
```

Contoh Python hanya memakai pustaka standar.

## Layanan katalog tanpa Kubernetes

```bash
cd katalog
PORT=8080 go run .
curl localhost:8080/readyz       # 503 selama pemanasan (2 detik), lalu 200
curl localhost:8080/item/1       # {"id":1,"nama":"Kopi","harga":10000,"pod":"..."}
docker build -t katalog:v1 .     # image akhir sekitar 10 MB (distroless, nonroot)
```

## Praktikum Kubernetes (Subbab 7.7)

Butuh docker, [kind](https://kind.sigs.k8s.io/), dan kubectl.

```bash
./praktikum.sh siapkan     # klaster kind "sister", build + load image, kubectl apply -f k8s/
./praktikum.sh beban       # terminal A: 5 request/detik dari pod curl di dalam klaster
./praktikum.sh bunuh       # terminal B: hapus satu pod, amati pengganti (Ctrl+C)
./praktikum.sh hitung      # jumlah request gagal di beban.log
./praktikum.sh peristiwa   # urutan event untuk menghitung waktu pulih
./praktikum.sh hpa         # pasang metrics-server, BEBAN_CPU=5ms, amati HPA
./praktikum.sh bersih      # hapus klaster
```

Variasi yang dianjurkan di buku:

1. Ubah `replicas` menjadi 1 lalu 3 (`kubectl scale deployment/katalog --replicas=1`), ulangi
   langkah bunuh, dan bandingkan jumlah request gagal.
2. Hapus `readinessProbe` dari `k8s/deployment.yaml`, `kubectl apply -f k8s/`, lalu ulangi.
   Pod pengganti langsung menerima lalu lintas selama pemanasan, padahal `/item` masih
   menjawab 503, sehingga jumlah request gagal naik.
3. Catat waktu dari pod dihapus sampai penggantinya Ready dengan `./praktikum.sh peristiwa`.
4. Beri beban tinggi lalu amati `kubectl get hpa -w`.

Mengapa beban dari dalam klaster: `kubectl port-forward svc/katalog` hanya tersambung ke satu
pod. Bila pod itu yang dimatikan, alat ukurnya yang putus, bukan layanannya.
