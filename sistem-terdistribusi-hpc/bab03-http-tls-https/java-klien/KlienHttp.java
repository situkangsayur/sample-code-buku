// Kode 3.4: klien HTTP/2 dengan java.net.http.HttpClient (Java 11+).
// Jalankan (Java 21): java KlienHttp.java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class KlienHttp {
    public static void main(String[] args) throws Exception {
        String url = args.length > 0 ? args[0] : "https://www.cloudflare.com/";
        HttpClient klien = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)         // coba h2 lewat ALPN
            .connectTimeout(Duration.ofSeconds(2))
            .build();
        HttpRequest req = HttpRequest.newBuilder(URI.create(url))
            .timeout(Duration.ofSeconds(5))             // batas seluruh request
            .GET().build();
        HttpResponse<String> res = klien.send(req, HttpResponse.BodyHandlers.ofString());
        System.out.println(res.version() + " " + res.statusCode()
            + " " + res.body().length() + " karakter");
    }
}
