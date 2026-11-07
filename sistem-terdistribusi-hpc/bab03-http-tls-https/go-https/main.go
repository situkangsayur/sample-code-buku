// Kode 3.7: server HTTPS minimal di Go.
// Siapkan sertifikat: mkcert -install && mkcert localhost 127.0.0.1
// Jalankan: go run .   Uji: curl --http1.1 https://localhost:8443/ ; curl --http2 ...
package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// r.TLS.Version 0x0304 = TLS 1.3
		fmt.Fprintf(w, "halo, protokol: %s, TLS: %x\n", r.Proto, r.TLS.Version)
	})
	log.Println("HTTPS di https://localhost:8443/")
	// dengan TLS, Go otomatis menawarkan HTTP/2 (ALPN "h2")
	log.Fatal(http.ListenAndServeTLS(":8443",
		"localhost+1.pem", "localhost+1-key.pem", nil))
}
