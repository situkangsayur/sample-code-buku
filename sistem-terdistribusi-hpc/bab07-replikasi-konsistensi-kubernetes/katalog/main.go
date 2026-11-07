// Layanan katalog minimal untuk praktikum Kubernetes (stateless, tanpa basis data).
//
// Endpoint:
//
//	GET /item/{id}  data item; jawaban memuat nama pod agar pembagian beban terlihat;
//	                503 selama pemanasan (cache belum dimuat)
//	GET /healthz    liveness: hanya memeriksa proses ini sendiri
//	GET /readyz     readiness: 503 selama pemanasan dan saat sedang berhenti
//
// Variabel lingkungan:
//
//	PORT         port HTTP (bawaan 8080)
//	PEMANASAN    lama pemanasan sebelum siap, mis. 3s (bawaan 2s)
//	BEBAN_CPU    kerja CPU buatan per request, mis. 5ms, untuk mencoba HPA
//
// Saat menerima SIGTERM (pod dihapus), layanan menandai dirinya tidak siap,
// menunggu sebentar agar Service berhenti mengirim lalu lintas, lalu menutup
// koneksi dengan rapi. Ini mengurangi request gagal saat pod diganti.
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"sync/atomic"
	"syscall"
	"time"
)

type Item struct {
	ID    int    `json:"id"`
	Nama  string `json:"nama"`
	Harga int    `json:"harga"`
	Pod   string `json:"pod"`
}

var nama = map[int]string{1: "Kopi", 2: "Teh", 3: "Gula Aren"}

func durasi(kunci string, bawaan time.Duration) time.Duration {
	if d, err := time.ParseDuration(os.Getenv(kunci)); err == nil {
		return d
	}
	return bawaan
}

func main() {
	pod, _ := os.Hostname() // di Kubernetes, hostname = nama pod
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	bebanCPU := durasi("BEBAN_CPU", 0)
	var hangat, berhenti atomic.Bool // pemanasan selesai; sedang berhenti

	mux := http.NewServeMux()
	mux.HandleFunc("GET /item/{id}", func(w http.ResponseWriter, r *http.Request) {
		if !hangat.Load() { // tanpa readinessProbe, request ini tetap sampai ke sini
			http.Error(w, "sedang pemanasan", http.StatusServiceUnavailable)
			return
		}
		id, err := strconv.Atoi(r.PathValue("id"))
		n, ok := nama[id]
		if err != nil || !ok {
			http.Error(w, "item tidak ada", http.StatusNotFound)
			return
		}
		for akhir := time.Now().Add(bebanCPU); time.Now().Before(akhir); {
			// putaran sibuk: meniru kerja CPU agar HPA punya alasan menambah replika
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(Item{ID: id, Nama: n, Harga: 10000 * id, Pod: pod})
	})
	mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok")) // jangan periksa dependensi eksternal di sini
	})
	mux.HandleFunc("GET /readyz", func(w http.ResponseWriter, r *http.Request) {
		if !hangat.Load() || berhenti.Load() {
			http.Error(w, "belum siap", http.StatusServiceUnavailable)
			return
		}
		w.Write([]byte("siap"))
	})

	srv := &http.Server{Addr: ":" + port, Handler: mux, ReadHeaderTimeout: 5 * time.Second}
	go func() {
		log.Printf("katalog %s mendengar di :%s", pod, port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal(err)
		}
	}()

	// pemanasan: misalnya memuat cache; selama ini readiness gagal
	time.Sleep(durasi("PEMANASAN", 2*time.Second))
	hangat.Store(true)
	log.Println("siap menerima lalu lintas")

	// berhenti dengan rapi saat SIGTERM
	sinyal := make(chan os.Signal, 1)
	signal.Notify(sinyal, syscall.SIGTERM, os.Interrupt)
	<-sinyal
	berhenti.Store(true) // readiness gagal, tetapi request yang masih datang tetap dilayani
	log.Println("SIGTERM: berhenti menerima lalu lintas baru")
	time.Sleep(3 * time.Second) // beri waktu endpoint Service diperbarui
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	srv.Shutdown(ctx) // selesaikan request yang sedang berjalan
	log.Println("selesai")
}
