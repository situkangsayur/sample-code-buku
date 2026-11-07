// Klien gRPC layanan katalog: deadline 300 ms, metadata authorization,
// service config (timeout + retry policy), dan contoh tiga mode streaming.
// Catatan: timeout 0.3s di service_config.json berlaku untuk semua method
// layanan; entri kedua (per method) menimpanya untuk method streaming yang
// memang berumur panjang, sehingga deadline-nya diatur dari kode.
//
// Contoh:
//
//	go run ./grpcklien                     # unary AmbilProduk id 42
//	go run ./grpcklien -id 99              # NOT_FOUND
//	go run ./grpcklien -mode pantau -n 3   # server streaming, 3 pesan
//	go run ./grpcklien -mode impor         # client streaming
//	go run ./grpcklien -mode tawar         # bidirectional streaming
package main

import (
	"context"
	_ "embed"
	"errors"
	"flag"
	"fmt"
	"io"
	"log"
	"time"

	pb "contoh/katalog/gen/katalogv1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

//go:embed service_config.json
var konfigJSON string

func main() {
	alamat := flag.String("alamat", "localhost:50051", "alamat server gRPC")
	mode := flag.String("mode", "unary", "unary | pantau | impor | tawar")
	id := flag.Int64("id", 42, "ID produk")
	n := flag.Int("n", 3, "jumlah pesan yang ditunggu pada mode pantau")
	flag.Parse()

	conn, err := grpc.NewClient(*alamat,
		grpc.WithTransportCredentials(insecure.NewCredentials()), // produksi: TLS/mTLS
		grpc.WithDefaultServiceConfig(konfigJSON))                // timeout + retry policy
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	c := pb.NewKatalogClient(conn)

	switch *mode {
	case "unary":
		unary(c, *id)
	case "pantau":
		pantau(c, *id, *n)
	case "impor":
		impor(c)
	case "tawar":
		tawar(c, *id)
	default:
		log.Fatalf("mode tidak dikenal: %s", *mode)
	}
}

// unary: persis seperti Kode di buku, selalu dengan deadline.
func unary(c pb.KatalogClient, id int64) {
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer rahasia")

	p, err := c.AmbilProduk(ctx, &pb.AmbilProdukRequest{Id: id})
	switch status.Code(err) {
	case codes.OK:
		fmt.Println(p.GetNama(), p.GetHarga())
	case codes.DeadlineExceeded:
		log.Println("terlalu lambat, pakai data cadangan")
	default:
		log.Println("gagal:", err)
	}
}

// pantau: server streaming. Deadline dihitung dari jumlah pesan yang ditunggu;
// cancel() di akhir memberi tahu server untuk berhenti mengirim.
func pantau(c pb.KatalogClient, id int64, n int) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(n+2)*time.Second)
	defer cancel()
	ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer rahasia")
	stream, err := c.PantauHarga(ctx, &pb.AmbilProdukRequest{Id: id})
	if err != nil {
		log.Fatal(err)
	}
	for i := 0; i < n; i++ {
		p, err := stream.Recv()
		if err != nil {
			log.Fatal("stream putus: ", err)
		}
		fmt.Printf("%s harga %s: %d\n", time.Now().Format("15:04:05"), p.GetNama(), p.GetHarga())
	}
}

// impor: client streaming. Kirim beberapa produk, tutup, terima ringkasan.
func impor(c pb.KatalogClient) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer rahasia")
	stream, err := c.ImporProduk(ctx)
	if err != nil {
		log.Fatal(err)
	}
	for i, nama := range []string{"Kopi Gayo", "Kopi Toraja", "Kopi Kintamani"} {
		if err := stream.Send(&pb.Produk{Id: int64(100 + i), Nama: nama, Harga: 30000}); err != nil {
			log.Fatal(err)
		}
	}
	r, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("produk diimpor:", r.GetJumlah())
}

// tawar: bidirectional streaming. Pengiriman dan penerimaan berjalan di dua
// goroutine; klien menaikkan tawaran sampai server menyetujui.
func tawar(c pb.KatalogClient, id int64) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	ctx = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer rahasia")
	stream, err := c.Tawar(ctx)
	if err != nil {
		log.Fatal(err)
	}
	selesai := make(chan struct{})
	go func() { // penerima
		defer close(selesai)
		for {
			t, err := stream.Recv()
			if errors.Is(err, io.EOF) {
				return
			}
			if err != nil {
				log.Println("gagal menerima:", err)
				return
			}
			fmt.Println("server membalas:", t.GetHarga())
		}
	}()
	for _, h := range []int64{15000, 20000, 23000} { // pengirim
		fmt.Println("klien menawar :", h)
		if err := stream.Send(&pb.Tawaran{Id: id, Harga: h}); err != nil {
			log.Fatal(err)
		}
		time.Sleep(100 * time.Millisecond)
	}
	stream.CloseSend()
	<-selesai
}
