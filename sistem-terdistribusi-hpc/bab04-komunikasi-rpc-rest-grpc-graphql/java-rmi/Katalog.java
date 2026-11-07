// Katalog.java -- kontrak: antarmuka yang mewarisi Remote
// Setiap method jarak jauh wajib menyatakan RemoteException, karena panggilan
// ini melewati jaringan dan bisa gagal walaupun terlihat seperti panggilan lokal.
public interface Katalog extends java.rmi.Remote {
    String ambilNama(long id) throws java.rmi.RemoteException;  // wajib dideklarasikan
}
