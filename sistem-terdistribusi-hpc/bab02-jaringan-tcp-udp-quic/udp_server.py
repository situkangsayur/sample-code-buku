"""Kode 2.7 (atas): echo server UDP di port 9001."""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 9001))
print("echo UDP mendengar di :9001")
while True:
    data, alamat = s.recvfrom(2048)  # satu datagram utuh
    s.sendto(data, alamat)
