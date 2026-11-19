# Deskripsi
Tambahkan kalkulator subnet IPv4 berbasis web dengan validasi input, API FastAPI, dan antarmuka responsif.

# Tugas
- Implementasikan `hitung_subnet(ip, prefix)`.
- Tambahkan `GET /api/subnet` dan `GET /`.
- Bangun halaman Subnet di `index.html`.
- Tulis dan jalankan test subnet.

# Kriteria Penerimaan
- Semua test di tabel `SPEC.md` untuk subnet lulus.
- Input invalid mengembalikan HTTP 400 dengan field `detail`.
- /31 dan /32 mengikuti keputusan yang tercantum dalam spesifikasi.
- Halaman menampilkan hasil serta pesan error yang jelas.

# Alur Kerja
Issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge
