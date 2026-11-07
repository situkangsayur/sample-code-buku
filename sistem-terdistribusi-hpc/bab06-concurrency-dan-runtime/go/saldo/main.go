// Kode 6.18: soal saldo bersama, satu goroutine pemilik saldo.
// Jalankan: go run -race ./saldo   lalu   time go run ./saldo
// Tambahkan argumen "mutex" untuk membandingkan dengan sync.Mutex.
package main

import (
	"fmt"
	"os"
	"sync"
	"time"
)

func denganChannel() int {
	tambah := make(chan int, 1024)
	selesai := make(chan int)
	go func() { // pemilik tunggal saldo
		saldo := 0
		for d := range tambah {
			saldo += d
		}
		selesai <- saldo
	}()
	var wg sync.WaitGroup
	for t := 0; t < 1000; t++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < 1000; i++ {
				tambah <- 1
			}
		}()
	}
	wg.Wait()
	close(tambah)
	return <-selesai
}

func denganMutex() int {
	var mu sync.Mutex
	saldo := 0
	var wg sync.WaitGroup
	for t := 0; t < 1000; t++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < 1000; i++ {
				mu.Lock()
				saldo++
				mu.Unlock()
			}
		}()
	}
	wg.Wait()
	return saldo
}

func main() {
	f, nama := denganChannel, "channel"
	if len(os.Args) > 1 && os.Args[1] == "mutex" {
		f, nama = denganMutex, "mutex"
	}
	for i := 0; i < 5; i++ {
		t0 := time.Now()
		s := f()
		fmt.Printf("%s: saldo=%d waktu=%v\n", nama, s, time.Since(t0).Round(time.Millisecond))
	}
}
