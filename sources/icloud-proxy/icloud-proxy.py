import csv
import ipaddress
import os
import urllib.request
from datetime import date


url_icloudegress = os.environ.get("url_icloudegress", "https://mask-api.icloud.com/egress-ip-ranges.csv")
output_icloudegress = os.environ.get("output_icloudegress", "data/icloud-proxy")
COLUMNS = ["cidr", "country", "region", "city", "blank"]


def fetch():
    with urllib.request.urlopen(url_icloudegress) as response:
        return response.read().decode("utf-8")


def parse(raw: str) -> list[dict]:
    rows = []
    reader = csv.reader(raw.splitlines())
    for row in reader:
        padded = row + [""] * (len(COLUMNS) - len(row))
        rows.append(dict(zip(COLUMNS, padded)))
    return rows


def write_csv(path: str, fieldnames: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {path}")


def is_ipv4(cidr: str) -> bool:
    return ":" not in cidr


def collapse_cidrs(rows: list[dict], version: int) -> list[dict]:
    net_type = ipaddress.IPv4Network if version == 4 else ipaddress.IPv6Network
    networks = [net_type(r["cidr"], strict=False) for r in rows]
    collapsed = ipaddress.collapse_addresses(networks)
    return [{"cidr": str(net)} for net in collapsed]


if __name__ == "__main__":
    today = date.today().strftime("%Y%m%d")

    raw = fetch()
    rows = parse(raw)

    out = output_icloudegress.rstrip("/\\")
    os.makedirs(out, exist_ok=True)

    write_csv(f"{out}/egress-ip-ranges-current.csv", COLUMNS, rows)

    ipv4_rows = [r for r in rows if is_ipv4(r["cidr"])]
    ipv6_rows = [r for r in rows if not is_ipv4(r["cidr"])]

    write_csv(f"{out}/icloud-egress-ipv4.csv", COLUMNS, ipv4_rows)
    write_csv(f"{out}/icloud-egress-ipv6.csv", COLUMNS, ipv6_rows)

    write_csv(f"{out}/icloud-egress-compresscidr-ipv4.csv", ["cidr"], collapse_cidrs(ipv4_rows, 4))
    write_csv(f"{out}/icloud-egress-compresscidr-ipv6.csv", ["cidr"], collapse_cidrs(ipv6_rows, 6))
