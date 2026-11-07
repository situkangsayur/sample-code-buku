# Layanan katalog: REST (:8080) dan gRPC (:50051) dengan data dan logika yang sama.
# Kode hasil generate sudah disertakan di gen/; jalankan 'make gen' bila .proto berubah.
# Butuh: Go 1.22+, buf, protoc-gen-go, protoc-gen-go-grpc (untuk 'make gen').
#   go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
#   go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

all: build

gen:
	buf lint
	buf generate

build:
	go vet ./...
	go build -o bin/ ./...

rest:
	go run ./rest

server:
	go run ./grpcserver

klien:
	go run ./grpcklien

bersih:
	rm -rf bin

.PHONY: all gen build rest server klien bersih
