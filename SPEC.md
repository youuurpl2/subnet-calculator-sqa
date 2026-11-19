# Kalkulator Subnet & VLSM

## Tujuan

Aplikasi web berbasis FastAPI untuk membantu guru dan siswa SMK TKJ menghitung subnet IPv4 serta mengalokasikan jaringan dengan VLSM.

## Aturan Validasi

- IPv4 terdiri tepat atas empat oktet bernilai 0-255.
- Oktet tidak boleh diawali nol, misalnya `192.168.01.1`.
- IP tidak boleh mengandung spasi.
- Prefix harus bilangan bulat dari 0 sampai 32.
- Input tidak valid menghasilkan `ValueError` pada fungsi dan HTTP 400 pada API.
- CIDR VLSM harus berupa alamat jaringan yang valid.
- Daftar kebutuhan tidak boleh kosong dan setiap kebutuhan harus lebih besar atau sama dengan 1.

## Kontrak Fungsi

### `hitung_subnet(ip: str, prefix: int) -> dict`

Mengembalikan `mask`, `network`, `broadcast`, `first_host`, `last_host`, dan `usable_hosts`.

- Network dihitung dengan operasi bitwise AND antara IP dan mask.
- Untuk prefix 0-30, jumlah host adalah `2 ** (32-prefix) - 2`.
- Prefix /31 memakai aturan point-to-point RFC 3021: dua host, tanpa broadcast.
- Prefix /32 memakai satu host, dengan IP sebagai first dan last host serta tanpa broadcast.

### `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

- Urutkan kebutuhan dari terbesar ke terkecil.
- Gunakan blok pangkat dua terkecil yang memenuhi `kebutuhan + 2`, minimum /30.
- Alokasikan berurutan dari alamat network.
- Setiap hasil memuat `kebutuhan`, `network_cidr`, dan semua kunci `hitung_subnet`.

## Kontrak API

- `GET /api/subnet?ip=&prefix=` mengembalikan hasil subnet.
- `POST /api/vlsm` menerima JSON `{"network": ".../24", "kebutuhan_host": [...]}`.
- `GET /` menyajikan halaman `index.html`.
- Kesalahan input API mengembalikan HTTP 400 dengan field JSON `detail`.

## Halaman Web

Satu halaman responsif dengan tab Subnet dan VLSM, desain terang, kartu hasil, serta pesan error yang jelas di bawah input.

## Tabel Test Case

| Kasus | Input | Hasil yang diharapkan | Status |
|---|---|---|---|
| Subnet /25 | `172.16.5.130/25` | network `172.16.5.128`, broadcast `172.16.5.255`, 126 host | pasti |
| Subnet /30 | `10.0.0.0/30` | host `.1-.2`, broadcast `.3`, 2 host | pasti |
| Point-to-point /31 | `192.168.1.0/31` | 2 host, broadcast `null` | pasti |
| Host tunggal /32 | `192.168.1.5/32` | 1 host, first=last `192.168.1.5`, broadcast `null` | pasti |
| Oktet invalid | `256.1.1.1/24` | ditolak | pasti |
| Nol depan | `192.168.01.1/24` | ditolak | pasti |
| Oktet kurang | `192.168.1/24` | ditolak | pasti |
| Bukan IP | `abc/24` | ditolak | pasti |
| IP kosong | kosong | ditolak | pasti |
| Prefix tinggi | prefix 33 | ditolak | pasti |
| Prefix negatif | prefix -1 | ditolak | pasti |
| VLSM | `192.168.1.0/24`, kebutuhan `100,50,20,2` | `/25 .0`, `/26 .128`, `/27 .192`, `/30 .224` | pasti |
| VLSM tidak muat | `192.168.1.0/24`, kebutuhan `200,100` | ditolak | pasti |

## Di Luar Cakupan

- IPv6.
- FLSM yang menghasilkan konfigurasi perangkat.
- Penyimpanan riwayat kalkulasi atau akun pengguna.
