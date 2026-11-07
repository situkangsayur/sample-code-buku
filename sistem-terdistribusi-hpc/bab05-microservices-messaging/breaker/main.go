// Kode 5.9: circuit breaker di depan panggilan ke layanan pembayaran.
//
// Layanan pembayaran disimulasikan oleh fungsi yang gagal selama 3 detik pertama
// lalu pulih. Program memanggilnya tiap 100 ms dan mencetak keadaan breaker.
// Jalankan: go run .
package main

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/sony/gobreaker"
)

var mulai = time.Now()

// statusPembayaran mensimulasikan panggilan gRPC ke layanan pembayaran.
func statusPembayaran(ctx context.Context, id string) (string, error) {
	select {
	case <-ctx.Done():
		return "", ctx.Err()
	case <-time.After(20 * time.Millisecond):
	}
	if time.Since(mulai) < 3*time.Second {
		return "", errors.New("pembayaran: unavailable")
	}
	return "LUNAS", nil
}

var cb = gobreaker.NewCircuitBreaker(gobreaker.Settings{
	Name:        "pembayaran",
	MaxRequests: 3,               // panggilan uji saat half-open
	Timeout:     2 * time.Second, // lama keadaan open (di buku 10 detik)
	ReadyToTrip: func(c gobreaker.Counts) bool {
		rasio := float64(c.TotalFailures) / float64(c.Requests)
		return c.Requests >= 10 && rasio >= 0.5
	},
	OnStateChange: func(nama string, dari, ke gobreaker.State) {
		fmt.Printf("%6.2fs  breaker %s: %s -> %s\n", time.Since(mulai).Seconds(), nama, dari, ke)
	},
})

func cekStatus(ctx context.Context, id string) (string, error) {
	hasil, err := cb.Execute(func() (interface{}, error) {
		ctx, batal := context.WithTimeout(ctx, 300*time.Millisecond)
		defer batal()
		return statusPembayaran(ctx, id)
	})
	if errors.Is(err, gobreaker.ErrOpenState) || errors.Is(err, gobreaker.ErrTooManyRequests) {
		return "TIDAK_DIKETAHUI", nil // fallback: tolak cepat
	}
	if err != nil {
		return "", err
	}
	return hasil.(string), nil
}

func main() {
	ctx := context.Background()
	for i := 0; i < 70; i++ {
		s, err := cekStatus(ctx, "1001")
		if i%5 == 0 {
			fmt.Printf("%6.2fs  status=%-16s err=%v\n", time.Since(mulai).Seconds(), s, err)
		}
		time.Sleep(100 * time.Millisecond)
	}
}
