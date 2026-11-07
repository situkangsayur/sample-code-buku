// Layanan katalog REST dengan pustaka standar Go (Go 1.22+).
//
// Endpoint:
//
//	GET /v1/produk/{id}         ambil satu produk (ETag + If-None-Match)
//	PUT /v1/produk/{id}         ubah produk (wajib If-Match: optimistic concurrency)
//	GET /v1/produk?limit=&after= daftar produk dengan cursor pagination
//
// Semua error memakai format Problem Details (RFC 9457). Dengan RATE_LIMIT=1,
// setiap klien dibatasi token bucket (r = 10/detik, b = 20) dan dijawab
// 429 + Retry-After bila melebihi batas.
//
// Jalankan: go run ./rest   (opsional JEDA=400ms untuk jeda buatan)
package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"net"
	"net/http"
	"os"
	"slices"
	"strconv"
	"sync"
	"time"
)

type Produk struct {
	ID    int64  `json:"id"`
	Nama  string `json:"nama"`
	Harga int64  `json:"harga"`
}

// gudang dan versi dilindungi mu karena PUT dapat mengubahnya bersamaan dengan GET.
var (
	mu     sync.RWMutex
	gudang = map[int64]Produk{
		42: {42, "Kopi", 25000},
		43: {43, "Teh", 15000},
		44: {44, "Gula Aren", 30000},
		45: {45, "Susu", 18000},
		46: {46, "Coklat", 27000},
	}
	versi = map[int64]int{42: 1, 43: 1, 44: 1, 45: 1, 46: 1} // dasar ETag
)

// jeda buatan untuk percobaan timeout/deadline (mis. JEDA=400ms)
var jeda, _ = time.ParseDuration(os.Getenv("JEDA"))

// tulisMasalah menulis error dengan format Problem Details (RFC 9457).
func tulisMasalah(w http.ResponseWriter, status int, judul, instance string) {
	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(map[string]any{
		"type":     "https://contoh.id/err/" + strconv.Itoa(status),
		"title":    judul,
		"status":   status,
		"instance": instance,
	})
}

func etag(id int64) string { return fmt.Sprintf(`"v%d"`, versi[id]) }

func ambil(w http.ResponseWriter, r *http.Request) {
	time.Sleep(jeda)
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	mu.RLock()
	p, ok := gudang[id]
	tag := etag(id)
	mu.RUnlock()
	if err != nil || !ok {
		tulisMasalah(w, 404, "Produk tidak ditemukan", r.URL.Path) // RFC 9457
		return
	}
	w.Header().Set("ETag", tag)
	w.Header().Set("Cache-Control", "max-age=10")
	if r.Header.Get("If-None-Match") == tag { // klien sudah punya versi ini
		w.WriteHeader(http.StatusNotModified)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(p)
}

// ubah menerapkan optimistic concurrency: PUT hanya berhasil bila If-Match
// sama dengan versi saat ini; bila tidak, 412 Precondition Failed.
func ubah(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		tulisMasalah(w, 400, "ID tidak sah", r.URL.Path)
		return
	}
	var baru Produk
	if err := json.NewDecoder(r.Body).Decode(&baru); err != nil || baru.Nama == "" || baru.Harga < 0 {
		tulisMasalah(w, 400, "Isi produk tidak sah", r.URL.Path)
		return
	}
	ifMatch := r.Header.Get("If-Match")
	if ifMatch == "" {
		tulisMasalah(w, 428, "Header If-Match wajib", r.URL.Path)
		return
	}
	mu.Lock()
	defer mu.Unlock()
	if _, ok := gudang[id]; !ok {
		tulisMasalah(w, 404, "Produk tidak ditemukan", r.URL.Path)
		return
	}
	if ifMatch != etag(id) {
		tulisMasalah(w, 412, "Versi sudah berubah, baca ulang lalu coba lagi", r.URL.Path)
		return
	}
	baru.ID = id
	gudang[id] = baru
	versi[id]++
	w.Header().Set("ETag", etag(id))
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(baru)
}

// daftar memakai cursor pagination: cursor adalah base64 dari ID terakhir
// yang sudah dibaca, sehingga halaman berikutnya mulai dari ID > cursor.
func daftar(w http.ResponseWriter, r *http.Request) {
	limit, err := strconv.Atoi(r.URL.Query().Get("limit"))
	if err != nil || limit <= 0 || limit > 100 {
		limit = 2
	}
	var setelah int64
	if c := r.URL.Query().Get("after"); c != "" {
		b, err := base64.RawURLEncoding.DecodeString(c)
		if err == nil {
			setelah, err = strconv.ParseInt(string(b), 10, 64)
		}
		if err != nil {
			tulisMasalah(w, 400, "Cursor tidak sah", r.URL.Path)
			return
		}
	}
	mu.RLock()
	ids := make([]int64, 0, len(gudang))
	for id := range gudang {
		if id > setelah {
			ids = append(ids, id)
		}
	}
	slices.Sort(ids)
	hasil := []Produk{}
	for _, id := range ids {
		if len(hasil) == limit {
			break
		}
		hasil = append(hasil, gudang[id])
	}
	mu.RUnlock()
	jawab := map[string]any{"data": hasil}
	if len(hasil) == limit && len(ids) > limit {
		akhir := strconv.FormatInt(hasil[len(hasil)-1].ID, 10)
		jawab["next"] = base64.RawURLEncoding.EncodeToString([]byte(akhir))
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(jawab)
}

// ember adalah token bucket per klien (Algoritma "Token bucket" di buku).
type ember struct {
	token float64
	akhir time.Time
}

type pembatas struct {
	mu    sync.Mutex
	r, b  float64 // laju isi ulang (token/detik) dan kapasitas
	ember map[string]*ember
}

func (p *pembatas) izinkan(klien string, t time.Time) (bool, time.Duration) {
	p.mu.Lock()
	defer p.mu.Unlock()
	e, ok := p.ember[klien]
	if !ok {
		e = &ember{token: p.b, akhir: t} // klien baru: ember penuh
		p.ember[klien] = e
	}
	e.token = math.Min(p.b, e.token+p.r*t.Sub(e.akhir).Seconds()) // isi ulang
	e.akhir = t
	if e.token >= 1 {
		e.token--
		return true, 0
	}
	tunggu := time.Duration((1 - e.token) / p.r * float64(time.Second))
	return false, tunggu
}

func (p *pembatas) bungkus(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		klien, _, _ := net.SplitHostPort(r.RemoteAddr)
		if ok, tunggu := p.izinkan(klien, time.Now()); !ok {
			detik := int(math.Ceil(tunggu.Seconds()))
			w.Header().Set("Retry-After", strconv.Itoa(max(1, detik)))
			tulisMasalah(w, 429, "Terlalu banyak permintaan", r.URL.Path)
			return
		}
		h.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /v1/produk/{id}", ambil) // pola metode + path (Go 1.22+)
	mux.HandleFunc("PUT /v1/produk/{id}", ubah)
	mux.HandleFunc("GET /v1/produk", daftar)

	var h http.Handler = mux
	// RATE_LIMIT=1 menyalakan pembatas laju. Bawaannya mati agar uji beban
	// dengan k6 (banyak VU dari satu alamat) tidak dijawab 429.
	if os.Getenv("RATE_LIMIT") == "1" {
		h = (&pembatas{r: 10, b: 20, ember: map[string]*ember{}}).bungkus(mux)
	}
	alamat := ":8080"
	if p := os.Getenv("PORT"); p != "" { // bila 8080 sudah dipakai program lain
		alamat = ":" + p
	}
	log.Println("REST katalog di", alamat)
	log.Fatal(http.ListenAndServe(alamat, h))
}
