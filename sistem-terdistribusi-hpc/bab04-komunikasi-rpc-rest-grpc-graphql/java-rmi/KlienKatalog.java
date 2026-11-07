// KlienKatalog.java -- cari stub di registry, lalu panggil seperti objek lokal
public class KlienKatalog {
    public static void main(String[] a) throws Exception {
        String host = a.length > 0 ? a[0] : "localhost";
        long id = a.length > 1 ? Long.parseLong(a[1]) : 42;
        var reg = java.rmi.registry.LocateRegistry.getRegistry(host, 1099);
        Katalog k = (Katalog) reg.lookup("katalog");
        try {
            System.out.println(k.ambilNama(id));              // terlihat lokal, padahal jaringan
        } catch (java.rmi.RemoteException e) {
            // kegagalan jaringan tetap muncul: ilusi lokal tidak pernah total
            System.err.println("panggilan jarak jauh gagal: " + e.getMessage());
        }
    }
}
