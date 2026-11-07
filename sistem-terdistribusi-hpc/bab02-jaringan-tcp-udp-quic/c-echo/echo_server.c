/* Kode 2.2: echo server TCP dalam C dengan socket API (iteratif).
 * Bangun: make   Jalankan: ./echo_server   Uji: nc localhost 9000 */
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    int ln = socket(AF_INET, SOCK_STREAM, 0);          /* socket() */
    if (ln < 0) { perror("socket"); return 1; }
    int ya = 1;
    setsockopt(ln, SOL_SOCKET, SO_REUSEADDR, &ya, sizeof ya);
    struct sockaddr_in a;
    memset(&a, 0, sizeof a);
    a.sin_family = AF_INET;
    a.sin_addr.s_addr = htonl(INADDR_ANY);
    a.sin_port = htons(9000);                           /* urutan byte jaringan */
    if (bind(ln, (struct sockaddr *)&a, sizeof a) < 0) { perror("bind"); return 1; }
    if (listen(ln, 128) < 0) { perror("listen"); return 1; }
    printf("echo TCP mendengar di :9000\n");
    for (;;) {
        struct sockaddr_in klien;
        socklen_t len = sizeof klien;
        int c = accept(ln, (struct sockaddr *)&klien, &len); /* socket baru per klien */
        if (c < 0) { perror("accept"); continue; }
        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &klien.sin_addr, ip, sizeof ip);
        printf("klien %s:%d terhubung\n", ip, ntohs(klien.sin_port));
        char buf[4096];
        ssize_t n;
        while ((n = recv(c, buf, sizeof buf, 0)) > 0)   /* 0 = klien menutup */
            send(c, buf, (size_t)n, 0);
        close(c);
    }
}
