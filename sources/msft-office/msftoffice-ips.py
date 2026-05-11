import csv
import ipaddress
import json
import os
import urllib.request

url_msftoffice = os.environ.get("url_msftoffice", "https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7")
output_msftoffice = os.environ.get("output_msftoffice", "data/msft-office")


def fetch_json(url: str) -> list:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def save_json(path: str, data: list):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {path}")


def write_csv(path: str, rows: list[dict], fieldnames: list[str]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {path}")


def is_ipv4(cidr: str) -> bool:
    return ":" not in cidr


def collapse_cidrs(cidrs: list[str], version: int) -> list[dict]:
    net_type = ipaddress.IPv4Network if version == 4 else ipaddress.IPv6Network
    networks = [net_type(c, strict=False) for c in cidrs]
    return [{"cidr": str(n)} for n in ipaddress.collapse_addresses(networks)]


def collapse_by_service(rows: list[dict], version: int) -> list[dict]:
    grouped: dict[str, list[str]] = {}
    for r in rows:
        grouped.setdefault(r["serviceArea"], []).append(r["cidr"])
    result = []
    for svc in sorted(grouped):
        for entry in collapse_cidrs(grouped[svc], version):
            result.append({"serviceArea": svc, "cidr": entry["cidr"]})
    return result


def parse_entries(data: list) -> list[dict]:
    rows = []
    for entry in data:
        service_area = entry.get("serviceArea", "unknown")
        for cidr in entry.get("ips", []):
            rows.append({"serviceArea": service_area, "cidr": cidr})
    return rows


if __name__ == "__main__":
    out = output_msftoffice.rstrip("/\\")
    os.makedirs(out, exist_ok=True)

    print(f"Fetching Office 365 endpoints: {url_msftoffice}")
    data = fetch_json(url_msftoffice)
    save_json(f"{out}/msft-office-current.json", data)

    all_rows = parse_entries(data)

    ipv4_rows = [r for r in all_rows if is_ipv4(r["cidr"])]
    ipv6_rows = [r for r in all_rows if not is_ipv4(r["cidr"])]

    write_csv(f"{out}/msftoffice-services-ipv4.csv", collapse_by_service(ipv4_rows, 4), ["serviceArea", "cidr"])
    write_csv(f"{out}/msftoffice-services-ipv6.csv", collapse_by_service(ipv6_rows, 6), ["serviceArea", "cidr"])
