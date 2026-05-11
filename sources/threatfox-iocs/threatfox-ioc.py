import csv
import io
import os
import urllib.request

url_threatfox = os.environ.get("url_threatfox", "https://threatfox.abuse.ch/export/csv/recent/")
output_threatfox = os.environ.get("output_threatfox", "data/threatfox-iocs")

OUTPUT_FIELDS = ["first_seen_utc", "ioc_id", "ioc_value", "threat_type", "malware_printable", "tags"]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8")


def save_raw(path: str, content: str):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"Saved raw data to {path}")


def write_csv(path: str, rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {path}")


def parse(raw: str) -> tuple[list[dict], list[dict]]:
    # Strip comment lines (start with #)
    data_lines = [l for l in raw.splitlines() if not l.startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(data_lines)))

    domains = []
    ips = []
    for row in reader:
        ioc_type = row.get("ioc_type", "").strip()
        if ioc_type == "domain":
            domains.append(row)
        elif ioc_type == "ip:port":
            row["ioc_value"] = row.get("ioc_value", "").rsplit(":", 1)[0]
            ips.append(row)

    return domains, ips


if __name__ == "__main__":
    out = output_threatfox.rstrip("/\\")
    os.makedirs(out, exist_ok=True)

    print(f"Fetching ThreatFox IOCs: {url_threatfox}")
    raw = fetch(url_threatfox)

    save_raw(f"{out}/threatfox-iocs-current.csv", raw)

    domains, ips = parse(raw)

    write_csv(f"{out}/threatfox-domains.csv", domains)
    write_csv(f"{out}/threatfox-ips.csv", ips)
