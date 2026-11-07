// Server SSE (Server-Sent Events) dengan Go: harga produk dikirim ke peramban
// tanpa diminta. Satu "hub" menyiarkan setiap perubahan harga ke semua klien
// yang sedang terhubung; tiap klien punya kanal perubahanHarga sendiri.
//
// Jalankan: go run .   lalu buka http://localhost:8081/ di peramban,
// atau: curl -N http://localhost:8081/v1/harga/42
package main

import (
	"fmt"
	"log"
	"math/rand/v2"
	"net/http"
	"os"
	"sync"
	"time"
)

// hub menyimpan kanal setiap klien yang berlangganan.
type hub struct {
	mu    sync.Mutex
	klien map[chan int64]struct{}
}

func (h *hub) langganan() chan int64 {
	c := make(chan int64, 8) // penyangga kecil
	h.mu.Lock()
	h.klien[c] = struct{}{}
	h.mu.Unlock()
	return c
}

func (h *hub) berhenti(c chan int64) {
	h.mu.Lock()
	delete(h.klien, c)
	h.mu.Unlock()
}

// siarkan mengirim harga ke semua klien. Klien lambat yang penyangganya penuh
// dilewati (pesan dibuang) agar tidak menahan klien lain: bentuk sederhana
// penanganan backpressure.
func (h *hub) siarkan(harga int64) {
	h.mu.Lock()
	defer h.mu.Unlock()
	for c := range h.klien {
		select {
		case c <- harga:
		default:
		}
	}
}

var pusat = &hub{klien: map[chan int64]struct{}{}}

func harga(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	f := w.(http.Flusher)
	perubahanHarga := pusat.langganan()
	defer pusat.berhenti(perubahanHarga)
	detak := time.NewTicker(15 * time.Second) // heartbeat agar proxy tidak memutus
	defer detak.Stop()
	f.Flush() // kirim header segera
	for {
		select {
		case <-r.Context().Done(): // klien pergi: berhenti
			return
		case h := <-perubahanHarga:
			fmt.Fprintf(w, "data: %d\n\n", h) // satu event diakhiri baris kosong
			f.Flush()
		case <-detak.C:
			fmt.Fprint(w, ": ping\n\n") // baris komentar SSE, diabaikan peramban
			f.Flush()
		}
	}
}

const halaman = `<!doctype html>
<meta charset="utf-8"><title>Harga kopi</title>
<h1>Harga kopi: <span id="h">menunggu...</span></h1>
<script>
const es = new EventSource('/v1/harga/42');
es.onmessage = (e) => { document.getElementById('h').textContent = e.data; };
</script>`

func main() {
	// simulasi layanan harga: harga berubah setiap detik
	go func() {
		h := int64(25000)
		for range time.Tick(time.Second) {
			h += (rand.Int64N(5) - 2) * 100
			pusat.siarkan(h)
		}
	}()
	http.HandleFunc("GET /v1/harga/{id}", harga) // contoh ini hanya punya satu produk
	http.HandleFunc("GET /{$}", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, halaman)
	})
	alamat := ":8081"
	if p := os.Getenv("PORT"); p != "" {
		alamat = ":" + p
	}
	log.Println("SSE di", alamat)
	log.Fatal(http.ListenAndServe(alamat, nil))
}
