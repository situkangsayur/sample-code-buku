# tahap 1: kompilasi
FROM golang:1.25 AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /katalog .

# tahap 2: image kecil untuk produksi (tanpa shell)
FROM gcr.io/distroless/static-debian12
COPY --from=build /katalog /katalog
EXPOSE 8080
USER nonroot
ENTRYPOINT ["/katalog"]
