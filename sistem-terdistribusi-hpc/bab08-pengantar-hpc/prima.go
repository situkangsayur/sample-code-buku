// Kode 8.1: menghitung bilangan prima secara paralel dengan goroutine.
// Pemakaian: go run prima.go <jumlah_worker> [N] [blok]
// Keluaran: p,detik,jumlah_prima
package main

import (
	"fmt"
	"os"
	"runtime"
	"strconv"
	"sync"
	"time"
)

func prima(n int) bool {
	if n < 2 {
		return false
	}
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "pemakaian: prima <p> [N] [blok]")
		os.Exit(1)
	}
	p, _ := strconv.Atoi(os.Args[1]) // jumlah worker
	N := 20_000_000
	if len(os.Args) > 2 {
		N, _ = strconv.Atoi(os.Args[2])
	}
	blok := len(os.Args) > 3 && os.Args[3] == "blok"
	runtime.GOMAXPROCS(p) // batasi jumlah core
	hasil := make([]int, p)
	var wg sync.WaitGroup
	mulai := time.Now()
	for w := 0; w < p; w++ {
		wg.Add(1)
		go func(w int) {
			defer wg.Done()
			c := 0 // penghitung lokal (hindari false sharing)
			if blok {
				for i := w * N / p; i < (w+1)*N/p; i++ { // pembagian blok
					if prima(i) {
						c++
					}
				}
			} else {
				for i := w; i < N; i += p { // pembagian cyclic
					if prima(i) {
						c++
					}
				}
			}
			hasil[w] = c // tulis sekali di akhir
		}(w)
	}
	wg.Wait()
	total := 0
	for _, c := range hasil {
		total += c
	}
	fmt.Printf("%d,%.4f,%d\n", p, time.Since(mulai).Seconds(), total)
}
