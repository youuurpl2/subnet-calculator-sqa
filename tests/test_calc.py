import pytest

from subnet_calculator_sqa.calc import hitung_subnet


def test_umum_26():
    r = hitung_subnet("192.168.10.37", 26)
    assert r["network"] == "192.168.10.0"
    assert r["broadcast"] == "192.168.10.63"
    assert r["host_pertama"] == "192.168.10.1"
    assert r["host_terakhir"] == "192.168.10.62"
    assert r["jumlah_host"] == 62


def test_prefix_30():
    assert hitung_subnet("10.0.0.5", 30)["jumlah_host"] == 2


def test_prefix_31_tanpa_broadcast():
    r = hitung_subnet("10.0.0.1", 31)
    assert r["jumlah_host"] == 2
    assert r["broadcast"] is None


def test_prefix_32_satu_host():
    r = hitung_subnet("10.0.0.1", 32)
    assert r["jumlah_host"] == 1
    assert r["host_pertama"] == r["host_terakhir"] == "10.0.0.1"


def test_prefix_0():
    assert hitung_subnet("1.2.3.4", 0)["jumlah_host"] == 2**32 - 2


@pytest.mark.parametrize("ip", ["", "300.1.1.1", "192.168.1", "a.b.c.d"])
def test_ip_tidak_valid(ip):
    with pytest.raises(ValueError):
        hitung_subnet(ip, 24)


@pytest.mark.parametrize("prefix", [-1, 33])
def test_prefix_di_luar_batas(prefix):
    with pytest.raises(ValueError):
        hitung_subnet("10.0.0.1", prefix)