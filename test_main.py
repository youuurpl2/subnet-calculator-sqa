import pytest
from fastapi.testclient import TestClient

from main import alokasi_vlsm, app, hitung_subnet


client = TestClient(app)


@pytest.mark.parametrize(
    ("ip", "prefix", "expected"),
    [
        ("172.16.5.130", 25, {
            "mask": "255.255.255.128",
            "network": "172.16.5.128",
            "broadcast": "172.16.5.255",
            "first_host": "172.16.5.129",
            "last_host": "172.16.5.254",
            "usable_hosts": 126,
        }),
        ("10.0.0.0", 30, {
            "mask": "255.255.255.252",
            "network": "10.0.0.0",
            "broadcast": "10.0.0.3",
            "first_host": "10.0.0.1",
            "last_host": "10.0.0.2",
            "usable_hosts": 2,
        }),
        ("192.168.1.0", 31, {
            "mask": "255.255.255.254",
            "network": "192.168.1.0",
            "broadcast": None,
            "first_host": "192.168.1.0",
            "last_host": "192.168.1.1",
            "usable_hosts": 2,
        }),
        ("192.168.1.5", 32, {
            "mask": "255.255.255.255",
            "network": "192.168.1.5",
            "broadcast": None,
            "first_host": "192.168.1.5",
            "last_host": "192.168.1.5",
            "usable_hosts": 1,
        }),
    ],
)
def test_hitung_subnet(ip, prefix, expected):
    assert hitung_subnet(ip, prefix) == expected


@pytest.mark.parametrize(
    ("ip", "prefix"),
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
        ("192.168.1.1 ", 24),
    ],
)
def test_hitung_subnet_rejects_invalid_input(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


def test_subnet_api_success():
    response = client.get("/api/subnet", params={"ip": "172.16.5.130", "prefix": 25})
    assert response.status_code == 200
    assert response.json()["network"] == "172.16.5.128"
    assert response.json()["broadcast"] == "172.16.5.255"


@pytest.mark.parametrize(
    ("ip", "prefix"),
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
    ],
)
def test_subnet_api_rejects_invalid_input(ip, prefix):
    response = client.get("/api/subnet", params={"ip": ip, "prefix": prefix})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()


def test_vlsm_allocation():
    hasil = alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2])
    assert [item["network_cidr"] for item in hasil] == [
        "192.168.1.0/25",
        "192.168.1.128/26",
        "192.168.1.192/27",
        "192.168.1.224/30",
    ]


@pytest.mark.parametrize(
    ("network", "needs"),
    [
        ("192.168.1.1/24", [10]),
        ("192.168.1.0/24", []),
        ("192.168.1.0/24", [0]),
        ("192.168.1.0/24", [200, 100]),
    ],
)
def test_vlsm_rejects_invalid_input(network, needs):
    with pytest.raises(ValueError):
        alokasi_vlsm(network, needs)


def test_vlsm_api_success():
    response = client.post(
        "/api/vlsm",
        json={"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]},
    )
    assert response.status_code == 200


def test_vlsm_api_rejects_invalid_input():
    response = client.post(
        "/api/vlsm",
        json={"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]},
    )
    assert response.status_code == 400
    assert "detail" in response.json()
