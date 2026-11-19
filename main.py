from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI()


def _ip_ke_int(ip: str) -> int:
    if not isinstance(ip, str) or not ip or ip != ip.strip():
        raise ValueError("IP tidak valid")
    oktet = ip.split(".")
    if len(oktet) != 4:
        raise ValueError("IP harus terdiri dari tepat 4 oktet")
    nilai = []
    for bagian in oktet:
        if not bagian or not bagian.isdigit():
            raise ValueError("IP tidak valid")
        if len(bagian) > 1 and bagian.startswith("0"):
            raise ValueError("Oktet tidak boleh diawali angka nol")
        angka = int(bagian)
        if angka < 0 or angka > 255:
            raise ValueError("Nilai oktet harus antara 0 dan 255")
        nilai.append(angka)
    hasil = 0
    for angka in nilai:
        hasil = (hasil << 8) | angka
    return hasil


def _int_ke_ip(nilai: int) -> str:
    return ".".join(str((nilai >> shift) & 255) for shift in (24, 16, 8, 0))


def _validasi_prefix(prefix: int) -> int:
    if isinstance(prefix, bool) or not isinstance(prefix, int) or prefix < 0 or prefix > 32:
        raise ValueError("Prefix harus bilangan bulat antara 0 dan 32")
    return prefix


def hitung_subnet(ip: str, prefix: int) -> dict:
    ip_int = _ip_ke_int(ip)
    prefix = _validasi_prefix(prefix)
    host_bits = 32 - prefix
    mask_int = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF if prefix else 0
    network_int = ip_int & mask_int
    broadcast_int = network_int | ((1 << host_bits) - 1)

    if prefix == 31:
        broadcast = None
        first_host = _int_ke_ip(network_int)
        last_host = _int_ke_ip(broadcast_int)
        usable_hosts = 2
    elif prefix == 32:
        broadcast = None
        first_host = ip
        last_host = ip
        usable_hosts = 1
    else:
        broadcast = _int_ke_ip(broadcast_int)
        first_host = _int_ke_ip(network_int + 1)
        last_host = _int_ke_ip(broadcast_int - 1)
        usable_hosts = (1 << host_bits) - 2

    return {
        "mask": _int_ke_ip(mask_int),
        "network": _int_ke_ip(network_int),
        "broadcast": broadcast,
        "first_host": first_host,
        "last_host": last_host,
        "usable_hosts": usable_hosts,
    }


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(network_cidr, str) or "/" not in network_cidr:
        raise ValueError("CIDR jaringan tidak valid")
    ip, prefix_text = network_cidr.rsplit("/", 1)
    if not prefix_text.isdigit():
        raise ValueError("CIDR jaringan tidak valid")
    prefix = int(prefix_text)
    _ip_ke_int(ip)
    _validasi_prefix(prefix)
    subnet = hitung_subnet(ip, prefix)
    if subnet["network"] != ip:
        raise ValueError("Network CIDR harus berupa alamat jaringan")
    if not kebutuhan_host:
        raise ValueError("Daftar kebutuhan tidak boleh kosong")
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 1 for n in kebutuhan_host):
        raise ValueError("Nilai kebutuhan harus bilangan bulat minimal 1")

    network_int = _ip_ke_int(ip)
    batas = network_int + (1 << (32 - prefix))
    current = network_int
    hasil = []
    for kebutuhan in sorted(kebutuhan_host, reverse=True):
        host_plus_network_broadcast = kebutuhan + 2
        block_size = 1
        while block_size < host_plus_network_broadcast:
            block_size <<= 1
        block_prefix = 32 - (block_size.bit_length() - 1)
        if block_prefix < prefix:
            raise ValueError("Blok tidak cukup menampung seluruh kebutuhan")
        if current + block_size > batas:
            raise ValueError("Blok tidak cukup menampung seluruh kebutuhan")
        cidr = f"{_int_ke_ip(current)}/{block_prefix}"
        detail = hitung_subnet(_int_ke_ip(current), block_prefix)
        hasil.append({"kebutuhan": kebutuhan, "network_cidr": cidr, **detail})
        current += block_size
    return hasil


@app.get("/api/subnet")
def api_subnet(ip: str | None = None, prefix: str | None = None):
    try:
        if ip is None or prefix is None or not prefix.isdigit():
            raise ValueError("Prefix harus bilangan bulat antara 0 dan 32")
        return hitung_subnet(ip, int(prefix))
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/vlsm")
def api_vlsm(body: dict):
    try:
        network = body.get("network")
        kebutuhan_host = body.get("kebutuhan_host")
        if not isinstance(kebutuhan_host, list):
            raise ValueError("Daftar kebutuhan tidak valid")
        return alokasi_vlsm(network, kebutuhan_host)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/")
def homepage():
    return FileResponse("index.html")
