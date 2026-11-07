// Server gRPC layanan katalog: keempat mode panggilan, interceptor autentikasi
// dan log, health check baku (grpc.health.v1), dan server reflection.
//
// Jalankan: go run ./grpcserver   (opsional JEDA=400ms untuk jeda buatan
// pada AmbilProduk, guna membuktikan DEADLINE_EXCEEDED di klien)
package main

import (
	"context"
	"errors"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"time"

	pb "contoh/katalog/gen/katalogv1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/health"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
)

// Data dan logika sama dengan versi REST (rest/main.go) agar perbandingan adil.
// gudang hanya dibaca setelah program mulai, jadi aman dibaca banyak goroutine.
var gudang = map[int64]*pb.Produk{
	42: {Id: 42, Nama: "Kopi", Harga: 25000},
	43: {Id: 43, Nama: "Teh", Harga: 15000},
	44: {Id: 44, Nama: "Gula Aren", Harga: 30000},
	45: {Id: 45, Nama: "Susu", Harga: 18000},
	46: {Id: 46, Nama: "Coklat", Harga: 27000},
}

var jeda, _ = time.ParseDuration(os.Getenv("JEDA"))

type server struct {
	pb.UnimplementedKatalogServer // aman bila kontrak bertambah method
}

// AmbilProduk: unary.
func (s *server) AmbilProduk(ctx context.Context, req *pb.AmbilProdukRequest) (*pb.Produk, error) {
	if jeda > 0 {
		select {
		case <-time.After(jeda): // jeda buatan
		case <-ctx.Done(): // deadline klien habis: jangan teruskan pekerjaan
			return nil, status.FromContextError(ctx.Err()).Err()
		}
	}
	p, ok := gudang[req.GetId()]
	if !ok {
		return nil, status.Errorf(codes.NotFound, "produk %d tidak ada", req.GetId())
	}
	return p, nil
}

// PantauHarga: server streaming, satu pesan per detik sampai klien pergi.
func (s *server) PantauHarga(req *pb.AmbilProdukRequest, stream pb.Katalog_PantauHargaServer) error {
	if _, ok := gudang[req.GetId()]; !ok {
		return status.Errorf(codes.NotFound, "produk %d tidak ada", req.GetId())
	}
	t := time.NewTicker(time.Second)
	defer t.Stop()
	for {
		select {
		case <-stream.Context().Done(): // klien batal atau deadline habis
			return stream.Context().Err()
		case <-t.C:
			if err := stream.Send(gudang[req.GetId()]); err != nil {
				return err
			}
		}
	}
}

// ImporProduk: client streaming. Server menghitung produk yang diterima,
// lalu menjawab satu ringkasan setelah klien menutup aliran.
func (s *server) ImporProduk(stream pb.Katalog_ImporProdukServer) error {
	var jumlah int32
	for {
		p, err := stream.Recv()
		if errors.Is(err, io.EOF) { // klien selesai mengirim
			return stream.SendAndClose(&pb.RingkasanImpor{Jumlah: jumlah})
		}
		if err != nil {
			return err
		}
		if p.GetNama() == "" {
			return status.Error(codes.InvalidArgument, "nama produk kosong")
		}
		jumlah++ // contoh ini tidak menyimpan; cukup menghitung
	}
}

// Tawar: bidirectional streaming. Setiap tawaran dijawab tawaran balik:
// bila tawaran di bawah 90% harga, server menawar di tengah-tengah;
// bila sudah cukup, server menyetujui harga tawaran itu.
func (s *server) Tawar(stream pb.Katalog_TawarServer) error {
	for {
		t, err := stream.Recv()
		if errors.Is(err, io.EOF) {
			return nil
		}
		if err != nil {
			return err
		}
		p, ok := gudang[t.GetId()]
		if !ok {
			return status.Errorf(codes.NotFound, "produk %d tidak ada", t.GetId())
		}
		balas := t.GetHarga()
		if t.GetHarga()*10 < p.GetHarga()*9 {
			balas = (t.GetHarga() + p.GetHarga()) / 2
		}
		if err := stream.Send(&pb.Tawaran{Id: t.GetId(), Harga: balas}); err != nil {
			return err
		}
	}
}

// authLog: interceptor unary untuk autentikasi dan log.
func authLog(ctx context.Context, req any, info *grpc.UnaryServerInfo,
	h grpc.UnaryHandler) (any, error) {
	if lewatiAuth(info.FullMethod) {
		return h(ctx, req)
	}
	md, _ := metadata.FromIncomingContext(ctx)
	if len(md.Get("authorization")) == 0 {
		return nil, status.Error(codes.Unauthenticated, "token kosong")
	}
	mulai := time.Now()
	resp, err := h(ctx, req) // panggil handler asli
	log.Printf("%s %v %s", info.FullMethod, status.Code(err), time.Since(mulai))
	return resp, err
}

// authLogStream: versi streaming dari authLog.
func authLogStream(srv any, ss grpc.ServerStream, info *grpc.StreamServerInfo,
	h grpc.StreamHandler) error {
	if lewatiAuth(info.FullMethod) {
		return h(srv, ss)
	}
	md, _ := metadata.FromIncomingContext(ss.Context())
	if len(md.Get("authorization")) == 0 {
		return status.Error(codes.Unauthenticated, "token kosong")
	}
	mulai := time.Now()
	err := h(srv, ss)
	log.Printf("%s %v %s (stream)", info.FullMethod, status.Code(err), time.Since(mulai))
	return err
}

// Health check dan reflection tidak memerlukan token, supaya probe Kubernetes
// dan grpcurl list tetap bekerja. Di layanan publik, pertimbangkan mematikan
// reflection.
func lewatiAuth(method string) bool {
	return strings.HasPrefix(method, "/grpc.health.v1.") ||
		strings.HasPrefix(method, "/grpc.reflection.")
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatal(err)
	}
	s := grpc.NewServer(
		grpc.ChainUnaryInterceptor(authLog), // interceptor authLog di atas
		grpc.ChainStreamInterceptor(authLogStream),
	)
	pb.RegisterKatalogServer(s, &server{})

	// health check baku: SERVING untuk seluruh server dan untuk layanan katalog
	hs := health.NewServer()
	hs.SetServingStatus("", healthpb.HealthCheckResponse_SERVING)
	hs.SetServingStatus("katalog.v1.Katalog", healthpb.HealthCheckResponse_SERVING)
	healthpb.RegisterHealthServer(s, hs)

	reflection.Register(s) // agar grpcurl dapat memanggil tanpa berkas .proto

	log.Println("gRPC katalog di :50051")
	log.Fatal(s.Serve(lis))
}
