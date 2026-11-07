// Kode 6.6: goroutine, channel, dan sync.WaitGroup.
// Jalankan: go run ./goroutine
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// ambil mensimulasikan panggilan jaringan yang butuh 50-150 ms.
func ambil(u string) string {
	time.Sleep(time.Duration(50+rand.Intn(100)) * time.Millisecond)
	return "isi " + u
}

func main() {
	t0 := time.Now()
	urls := []string{"a.id", "b.id", "c.id"}
	hasil := make(chan string, len(urls)) // channel ber-buffer
	var wg sync.WaitGroup
	for _, u := range urls {
		wg.Add(1)
		go func(u string) { // goroutine baru
			defer wg.Done()
			hasil <- ambil(u) // kirim ke channel
		}(u)
	}
	wg.Wait()              // tunggu semua goroutine
	close(hasil)           // tidak ada lagi yang mengirim
	for h := range hasil { // range berhenti setelah close
		fmt.Println(h)
	}
	fmt.Println("waktu total:", time.Since(t0).Round(time.Millisecond))
}
