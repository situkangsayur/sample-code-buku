#!/usr/bin/env bash
# Praktikum self-healing dengan kind: matikan pod, ukur waktu pulih.
# Butuh: docker, kind, kubectl.
#
# Pakai (dari folder ini):
#   ./praktikum.sh siapkan     # 1. klaster lokal, build image, deploy
#   ./praktikum.sh beban       # 2. beban terus-menerus DARI DALAM klaster (terminal A)
#   ./praktikum.sh bunuh       # 3. matikan satu pod dan amati penggantinya (terminal B)
#   ./praktikum.sh hitung      # 4. hitung permintaan yang gagal
#   ./praktikum.sh peristiwa   #    urutan event: kapan pod dihapus dan kapan pengganti Ready
#   ./praktikum.sh hpa         #    pasang metrics-server dan amati HPA
#   ./praktikum.sh bersih      #    hapus klaster
set -euo pipefail
cd "$(dirname "$0")"
KLASTER=sister

siapkan() {
  # 1. klaster lokal dan deploy (tiga node: lihat kind-sister.yaml)
  kind get clusters | grep -qx "$KLASTER" || kind create cluster --name "$KLASTER" --config kind-sister.yaml
  docker build -t katalog:v1 ./katalog
  kind load docker-image katalog:v1 --name "$KLASTER"
  kubectl apply -f k8s/
  kubectl rollout status deployment/katalog --timeout=120s
  kubectl get pods -l app=katalog -o wide
}

beban() {
  # 2. beban terus-menerus DARI DALAM klaster (5 permintaan per detik).
  # Baris yang tidak diawali jam (pesan kubectl) diabaikan saat menghitung.
  kubectl run beban --rm -it --restart=Never --image=curlimages/curl -- sh -c \
    'while true; do echo "$(date +%T) $(curl -s -o /dev/null -m 1 \
     -w %{http_code} http://katalog/item/1)"; sleep 0.2; done' | tee beban.log
}

bunuh() {
  # 3. matikan satu pod dan amati penggantinya (Ctrl+C untuk berhenti mengamati)
  kubectl delete $(kubectl get pod -l app=katalog -o name | head -1) --wait=false
  kubectl get pods -l app=katalog -w
}

hitung() {
  # 4. hitung permintaan yang gagal (status selain 200, termasuk 000 = timeout)
  local total gagal
  total=$(grep -cE '^[0-9]{2}:[0-9]{2}:[0-9]{2} ' beban.log || true)
  gagal=$(grep -E '^[0-9]{2}:[0-9]{2}:[0-9]{2} ' beban.log | grep -vc ' 200' || true)
  echo "total permintaan: $total, gagal: $gagal"
  grep -E '^[0-9]{2}:[0-9]{2}:[0-9]{2} ' beban.log | grep -v ' 200' || true
}

peristiwa() {
  kubectl get events --sort-by=.lastTimestamp | grep -E 'katalog|Killing|Scheduled|Started' | tail -20
}

hpa() {
  # metrics-server; --kubelet-insecure-tls hanya untuk klaster lokal kind
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  kubectl -n kube-system patch deployment metrics-server --type=json \
    -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
  kubectl -n kube-system rollout status deployment/metrics-server --timeout=120s
  # beri kerja CPU buatan per request agar pemakaian CPU naik saat dibebani
  kubectl set env deployment/katalog BEBAN_CPU=5ms
  echo "Beri beban tinggi, misalnya:"
  echo "  kubectl run hey --rm -it --restart=Never --image=williamyeh/hey -- -z 120s -c 50 http://katalog/item/1"
  kubectl get hpa katalog -w
}

bersih() {
  kind delete cluster --name "$KLASTER"
  rm -f beban.log
}

case "${1:-}" in
  siapkan|beban|bunuh|hitung|peristiwa|hpa|bersih) "$1" ;;
  *) sed -n '2,15p' "$0"; exit 1 ;;
esac
