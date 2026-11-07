// Retry dengan exponential backoff dan full jitter, menghormati deadline.
// Program ini menjalankan server HTTP palsu yang gagal (503) beberapa kali
// sebelum berhasil, lalu memanggilnya lewat denganRetry.
//
// Jalankan: go run .        (opsional: go run . -gagal 6 -deadline 1s)
package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log"
	"math/rand/v2"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"time"
)

// errSementara menandai error yang aman diulang (503, 429, UNAVAILABLE).
var errSementara = errors.New("error sementara")

func bisaDiulang(err error) bool { return errors.Is(err, errSementara) }

func denganRetry(ctx context.Context, f func(context.Context) error) error {
	base, maks := 100*time.Millisecond, 2*time.Second
	var err error
	for coba := 0; coba < 5; coba++ {
		if err = f(ctx); err == nil || !bisaDiulang(err) {
			return err
		}
		batas := min(maks, base<<coba)                    // 100, 200, 400, ...
		tunda := time.Duration(rand.Int64N(int64(batas))) // full jitter
		log.Printf("percobaan %d gagal (%v), tunggu %v (batas %v)", coba+1, err, tunda.Round(time.Millisecond), batas)
		select {
		case <-time.After(tunda):
		case <-ctx.Done(): // hormati deadline
			return ctx.Err()
		}
	}
	return err
}

func main() {
	nGagal := flag.Int64("gagal", 3, "jumlah 503 sebelum server berhasil")
	deadline := flag.Duration("deadline", 3*time.Second, "deadline seluruh operasi")
	flag.Parse()

	// server palsu: n permintaan pertama dijawab 503, sisanya 200
	var hitung atomic.Int64
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if hitung.Add(1) <= *nGagal {
			http.Error(w, "sibuk", http.StatusServiceUnavailable)
			return
		}
		fmt.Fprintln(w, "ok")
	}))
	defer srv.Close()

	// operasi GET bersifat idempotent, jadi aman diulang
	panggil := func(ctx context.Context) error {
		req, _ := http.NewRequestWithContext(ctx, http.MethodGet, srv.URL, nil)
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			return err
		}
		defer resp.Body.Close()
		switch {
		case resp.StatusCode == 503 || resp.StatusCode == 429:
			return fmt.Errorf("%w: status %d", errSementara, resp.StatusCode)
		case resp.StatusCode >= 400:
			return fmt.Errorf("status %d", resp.StatusCode) // jangan diulang
		}
		return nil
	}

	ctx, cancel := context.WithTimeout(context.Background(), *deadline)
	defer cancel()
	mulai := time.Now()
	err := denganRetry(ctx, panggil)
	log.Printf("hasil: err=%v, total permintaan=%d, waktu=%v", err, hitung.Load(), time.Since(mulai).Round(time.Millisecond))
}
