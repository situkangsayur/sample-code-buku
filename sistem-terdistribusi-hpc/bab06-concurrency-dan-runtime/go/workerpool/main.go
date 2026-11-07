// Kode 6.8: worker pool dengan empat pekerja.
// Jalankan: go run ./workerpool   (keluaran 2870 = 1^2 + ... + 20^2)
package main

import (
	"fmt"
	"sync"
)

func pekerja(jobs <-chan int, out chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs { // hanya menerima dari jobs
		out <- j * j
	}
}

func main() {
	jobs, out := make(chan int, 100), make(chan int, 100)
	var wg sync.WaitGroup
	for w := 0; w < 4; w++ { // 4 pekerja tetap
		wg.Add(1)
		go pekerja(jobs, out, &wg)
	}
	for j := 1; j <= 20; j++ {
		jobs <- j
	}
	close(jobs)
	go func() { wg.Wait(); close(out) }()
	total := 0
	for r := range out { // total hanya disentuh satu goroutine
		total += r
	}
	fmt.Println(total)
}
