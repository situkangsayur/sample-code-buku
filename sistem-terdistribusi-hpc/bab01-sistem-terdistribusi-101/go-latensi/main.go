// Kode 1.2: mengukur latency banyak URL secara concurrent
// dengan goroutine dan channel.
// Jalankan: go run .
package main

import (
	"fmt"
	"net/http"
	"time"
)

func ukur(url string) string {
	mulai := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Sprintf("%-28s gagal: %v", url, err)
	}
	resp.Body.Close()
	return fmt.Sprintf("%-28s %v", url, time.Since(mulai))
}

func main() {
	daftar := []string{"https://www.tazkia.ac.id",
		"https://www.google.com", "https://www.wikipedia.org"}
	hasil := make(chan string)
	mulai := time.Now()
	for _, u := range daftar {
		go func() { hasil <- ukur(u) }() // satu goroutine per URL (Go 1.22+)
	}
	for range daftar { // terima sebanyak URL yang dikirim
		fmt.Println(<-hasil)
	}
	fmt.Println("total (paralel):", time.Since(mulai))
}
