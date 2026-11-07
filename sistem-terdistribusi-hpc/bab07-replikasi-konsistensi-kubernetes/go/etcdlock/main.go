// Kode 7.2: distributed lock dan pemilihan leader dengan etcd.
//
// Jalankan etcd lokal:
//   docker run -d --name etcd -p 2379:2379 quay.io/coreos/etcd:v3.5.17 \
//     etcd --advertise-client-urls http://0.0.0.0:2379 --listen-client-urls http://0.0.0.0:2379
// Lalu di dua terminal berbeda:
//   go run . replika-1
//   go run . replika-2
// Hanya satu yang menjadi leader; matikan (Ctrl+C) yang aktif, yang lain mengambil alih
// setelah lease habis (paling lama 10 detik).
package main

import (
	"context"
	"log"
	"os"
	"time"

	clientv3 "go.etcd.io/etcd/client/v3"
	"go.etcd.io/etcd/client/v3/concurrency"
)

func main() {
	namaReplika := "replika-1"
	if len(os.Args) > 1 {
		namaReplika = os.Args[1]
	}
	cli, err := clientv3.New(clientv3.Config{
		Endpoints: []string{"localhost:2379"}, DialTimeout: 5 * time.Second})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	// sesi dengan lease 10 detik: bila proses mati, lock dilepas otomatis
	s, err := concurrency.NewSession(cli, concurrency.WithTTL(10))
	if err != nil {
		log.Fatal(err)
	}
	defer s.Close()

	// 1. distributed lock untuk satu rekening
	m := concurrency.NewMutex(s, "/kunci/rekening-1001")
	ctx, batal := context.WithTimeout(context.Background(), 3*time.Second)
	defer batal()
	if err := m.Lock(ctx); err != nil {
		log.Fatal("gagal mendapat lock: ", err)
	}
	log.Println(namaReplika, "memegang lock rekening-1001; bekerja 1 detik")
	time.Sleep(time.Second) // ... critical section lintas mesin ...
	if err := m.Unlock(context.Background()); err != nil {
		log.Fatal(err)
	}

	// 2. pemilihan leader: hanya satu replika penjadwal yang aktif
	e := concurrency.NewElection(s, "/pemimpin/penjadwal")
	log.Println(namaReplika, "mencalonkan diri...")
	if err := e.Campaign(context.Background(), namaReplika); err != nil {
		log.Fatal(err)
	}
	log.Println(namaReplika, "sekarang leader; mulai menjadwalkan")
	for i := 0; ; i++ {
		log.Println(namaReplika, "menjalankan tugas terjadwal", i)
		time.Sleep(2 * time.Second)
	}
}
