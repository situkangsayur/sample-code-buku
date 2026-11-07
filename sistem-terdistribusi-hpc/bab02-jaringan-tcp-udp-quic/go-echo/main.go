// Kode 2.3: echo server TCP dalam Go, satu goroutine per klien.
// Jalankan: go run .    Uji: nc localhost 9000
package main

import (
	"bufio"
	"log"
	"net"
)

func main() {
	ln, err := net.Listen("tcp", ":9000") // socket + bind + listen
	if err != nil {
		log.Fatal(err)
	}
	log.Println("echo TCP mendengar di :9000")
	for {
		conn, err := ln.Accept() // menunggu handshake selesai
		if err != nil {
			continue
		}
		go layani(conn) // satu goroutine per klien
	}
}

func layani(c net.Conn) {
	defer c.Close()
	log.Println("klien", c.RemoteAddr())
	s := bufio.NewScanner(c) // framing: baca per baris
	for s.Scan() {
		if _, err := c.Write(append(s.Bytes(), '\n')); err != nil {
			return
		}
	}
}
