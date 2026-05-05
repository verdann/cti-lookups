import csv
import ipaddress
import json
import os
import urllib.error
import urllib.request
from datetime import date, timedelta

output_azure = os.environ.get("output_azure", "data/azure-cloud")
url_azurecloud_base = os.environ.get("url_azurecloud_base", "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63")
agentheader_azurecloud = {"User-Agent": os.environ.get("agentheader_azurecloud", "Mozilla/5.0")}


def find_json_url(lookback_days: int = 14) -> str:
#strict on bots going to their download page, so go check download.microsoft with known GUID and try dates
    today = date.today()
    for i in range(lookback_days):
        candidate = today - timedelta(days=i)
        url = f"{url_azurecloud_base}/ServiceTags_Public_{candidate.strftime('%Y%m%d')}.json"
        try:
            req = urllib.request.Request(url, headers=agentheader_azurecloud, method="HEAD")
            urllib.request.urlopen(req)
            return url
        except urllib.error.HTTPError:
            continue
    raise ValueError(f"No ServiceTags_Public JSON found in the last {lookback_days} days")


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=agentheader_azurecloud)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def save_json(path: str, data: dict):
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
        grouped.setdefault(r["systemService"], []).append(r["cidr"])
    result = []
    for svc in sorted(grouped):
        for entry in collapse_cidrs(grouped[svc], version):
            result.append({"systemService": svc, "cidr": entry["cidr"]})
    return result


def parse_by_service(data: dict) -> dict[str, list[str]]:
    services: dict[str, list[str]] = {}
    for entry in data.get("values", []):
        service = entry.get("properties", {}).get("systemService", "").strip()
        prefixes = entry.get("properties", {}).get("addressPrefixes", [])
        if not service:
            service = entry.get("name", "unknown")
        if service not in services:
            services[service] = []
        services[service].extend(prefixes)
    return services


if __name__ == "__main__":
    today = date.today().strftime("%Y%m%d")
    out = output_azure.rstrip("/\\")
    os.makedirs(out, exist_ok=True)

    print("Locating current ServiceTags_Public JSON...")
    json_url = find_json_url()
    print(f"Found: {json_url}")

    data = fetch_json(json_url)
    save_json(f"{out}/ServiceTags_Public_Current.json", data)

    services = parse_by_service(data)

    # One row per CIDR with systemService label
    all_rows = [
        {"systemService": svc, "cidr": cidr}
        for svc, cidrs in sorted(services.items())
        for cidr in cidrs
    ]
    write_csv(f"{out}/azure-cidrs-servicetag-current.csv", all_rows, ["systemService", "cidr"])

    ipv4_rows = [r for r in all_rows if is_ipv4(r["cidr"])]
    ipv6_rows = [r for r in all_rows if not is_ipv4(r["cidr"])]

    write_csv(f"{out}/azure-ipv4-servicetag.csv", collapse_by_service(ipv4_rows, 4), ["systemService", "cidr"])
    write_csv(f"{out}/azure-ipv6-servicetag.csv", collapse_by_service(ipv6_rows, 6), ["systemService", "cidr"])

    write_csv(f"{out}/azurecloud-ipv4.csv", collapse_cidrs([r["cidr"] for r in ipv4_rows], 4), ["cidr"])
    write_csv(f"{out}/azurecloud-ipv6.csv", collapse_cidrs([r["cidr"] for r in ipv6_rows], 6), ["cidr"])
