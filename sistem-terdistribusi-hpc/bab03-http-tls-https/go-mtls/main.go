// Kode 3.8: server Go yang mewajibkan mTLS, plus klien uji.
// 1) ./buat_sertifikat.sh   2) go run . server   3) go run . klien
package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

func poolCA() *x509.CertPool {
	caPEM, err := os.ReadFile("ca.pem") // CA internal
	if err != nil {
		log.Fatal(err)
	}
	pool := x509.NewCertPool()
	pool.AppendCertsFromPEM(caPEM)
	return pool
}

func server() {
	srv := &http.Server{
		Addr: ":9443",
		TLSConfig: &tls.Config{
			MinVersion: tls.VersionTLS13,
			ClientAuth: tls.RequireAndVerifyClientCert, // klien wajib bersertifikat
			ClientCAs:  poolCA(),                       // yang diterbitkan CA ini
		},
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			nama := r.TLS.PeerCertificates[0].Subject.CommonName
			fmt.Fprintf(w, "halo %s\n", nama) // identitas pemanggil
		}),
	}
	log.Println("server mTLS di :9443")
	log.Fatal(srv.ListenAndServeTLS("server.pem", "server-key.pem"))
}

func klien(denganSertifikat bool) {
	cfg := &tls.Config{RootCAs: poolCA(), MinVersion: tls.VersionTLS13}
	if denganSertifikat {
		cert, err := tls.LoadX509KeyPair("klien.pem", "klien-key.pem")
		if err != nil {
			log.Fatal(err)
		}
		cfg.Certificates = []tls.Certificate{cert}
	}
	c := &http.Client{Timeout: 3 * time.Second, Transport: &http.Transport{TLSClientConfig: cfg}}
	resp, err := c.Get("https://localhost:9443/")
	if err != nil {
		fmt.Println("gagal (diharapkan bila tanpa sertifikat):", err)
		return
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	fmt.Print("berhasil: ", string(b))
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("pakai: go run . server | klien | klien-tanpa-sertifikat")
		return
	}
	switch os.Args[1] {
	case "server":
		server()
	case "klien":
		klien(true)
	default:
		klien(false)
	}
}
