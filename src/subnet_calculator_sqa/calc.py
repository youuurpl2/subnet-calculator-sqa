from ipaddress import IPv4Address, IPv4Network


def hitung_subnet(ip: str, prefix: int) -> dict:
    if isinstance(prefix, bool) or not isinstance(prefix, int) or not 0 <= prefix <= 32:
        raise ValueError("Prefix harus berupa angka 0 sampai 32")

    alamat = IPv4Address(ip)  # ValueError kalau IP tidak valid
    net = IPv4Network(f"{alamat}/{prefix}", strict=False)

    if prefix == 32:
        jumlah = 1
        pertama = terakhir = net.network_address
    elif prefix == 31:
        jumlah = 2
        pertama = net.network_address
        terakhir = net.broadcast_address
    else:
        jumlah = net.num_addresses - 2
        pertama = net.network_address + 1
        terakhir = net.broadcast_address - 1

    return {
        "ip": str(alamat),
        "prefix": prefix,
        "network": str(net.network_address),
        "broadcast": None if prefix >= 31 else str(net.broadcast_address),
        "host_pertama": str(pertama),
        "host_terakhir": str(terakhir),
        "jumlah_host": jumlah,
        "subnet_mask": str(net.netmask),
    }