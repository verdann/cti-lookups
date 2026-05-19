import csv
import json
import os
import urllib.request

url_binaryedge = os.environ.get("url_binaryedge", "https://api.binaryedge.io/v1/minions")
output_binaryedge = os.environ.get("output_binaryedge", "data/binaryedge")


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def is_ipv4(ip: str) -> bool:
    return ":" not in ip


def write_csv(path: str, header: str, rows: list[str]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([header])
        for value in rows:
            writer.writerow([value])
    print(f"Saved {len(rows)} rows to {path}")


if __name__ == "__main__":
    out = output_binaryedge.rstrip("/\\")
    os.makedirs(out, exist_ok=True)

    print(f"Fetching BinaryEdge minions: {url_binaryedge}")
    data = fetch_json(url_binaryedge)

    ipv4 = sorted(ip for ip in data.get("scanners", []) if is_ipv4(ip))

    write_csv(f"{out}/binaryedge-ipv4-ip.csv", "ip", ipv4)
    write_csv(f"{out}/binaryedge-ipv4-cidr.csv", "cidr", [f"{ip}/32" for ip in ipv4])
