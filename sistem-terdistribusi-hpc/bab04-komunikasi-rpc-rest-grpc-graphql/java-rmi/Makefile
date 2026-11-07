# Java RMI (sejarah). Butuh JDK 11 atau lebih baru (contoh memakai 'var').
OUT = kelas

all: kompilasi

kompilasi:
	mkdir -p $(OUT)
	javac -d $(OUT) Katalog.java ServerKatalog.java KlienKatalog.java

server: kompilasi
	java -cp $(OUT) ServerKatalog

klien: kompilasi
	java -cp $(OUT) KlienKatalog localhost 42

bersih:
	rm -rf $(OUT)

.PHONY: all kompilasi server klien bersih
