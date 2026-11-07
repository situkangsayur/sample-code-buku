// ServerKatalog.java -- implementasi, diekspor sebagai objek jarak jauh
// Contoh ini dibahas sebagai sejarah. Jangan memakai Java RMI untuk sistem baru.
public class ServerKatalog implements Katalog {
    public String ambilNama(long id) { return id == 42 ? "Kopi" : "tidak ada"; }

    public static void main(String[] a) throws Exception {
        int port = a.length > 0 ? Integer.parseInt(a[0]) : 1099;
        // exportObject membuat stub dan membuka port dinamis untuk objek ini
        Katalog stub = (Katalog) java.rmi.server.UnicastRemoteObject.exportObject(new ServerKatalog(), 0);
        // registry: "buku telepon" tempat klien mencari stub berdasarkan nama
        java.rmi.registry.LocateRegistry.createRegistry(port).rebind("katalog", stub);
        System.out.println("server RMI siap di port " + port);
        // proses tetap hidup selama objek masih diekspor
    }
}
