// Kode 6.7: timeout dengan select dan dengan context.
// Jalankan: go run ./selecttimeout
package main

import (
	"context"
	"fmt"
	"math/rand"
	"time"
)

func panggilLayanan() string {
	time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond) // 0-1 detik
	return "OK"
}

// statusDenganContext mensimulasikan klien gRPC yang menghormati deadline.
func statusDenganContext(ctx context.Context) (string, error) {
	select {
	case <-time.After(time.Duration(rand.Intn(1000)) * time.Millisecond):
		return "LUNAS", nil
	case <-ctx.Done():
		return "", ctx.Err() // pembatalan menjalar
	}
}

func main() {
	for i := 0; i < 3; i++ {
		hasil := make(chan string, 1) // buffer 1: cegah goroutine leak
		go func() { hasil <- panggilLayanan() }()
		select {
		case r := <-hasil:
			fmt.Println("jawaban:", r)
		case <-time.After(500 * time.Millisecond):
			fmt.Println("timeout, pakai cadangan")
		}
	}
	ctx, batal := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer batal()
	s, err := statusDenganContext(ctx)
	fmt.Println("dengan context:", s, err)
}
