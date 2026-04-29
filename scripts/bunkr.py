import sys
import base64
import requests
from math import floor
from itertools import cycle

BUNKRR_API = "https://bunkr.cr/api/vs"
BUNKRR_DOMAINS = ("bunkr.si", "bunkr.fi", "bunkr.ru", "bunkr.cr", "bunkr.rip", "bunkrr.su")
BUNKRR_DOWNLOAD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Referer": "https://get.bunkrr.su/",
    "Connection": "keep-alive",
}
_offline_subs = set()


def is_bunkr_url(url: str) -> bool:
    return any(domain in url for domain in BUNKRR_DOMAINS)


def get_slug(url: str) -> str:
    match = __import__("re").search(r"/([a-zA-Z0-9_-]+)$", url)
    return match.group(1) if match else None


def fetch_bunkr_api(url: str) -> dict | None:
    slug = get_slug(url)
    if not slug:
        return None
    payload = {"slug": slug}
    for dom in (BUNKRR_API.split("/")[2], *_offline_subs):
        try:
            api_url = f"https://{dom}/api/vs"
            resp = requests.post(api_url, json=payload, headers=BUNKRR_DOWNLOAD_HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 502:
                _offline_subs.add(dom)
        except Exception:
            continue
    return None


def decrypt_url(api_resp: dict) -> str | None:
    try:
        timestamp = api_resp["timestamp"]
        encrypted_bytes = base64.b64decode(api_resp["url"])
        time_key = floor(timestamp / 3600)
        secret_key = f"SECRET_KEY_{time_key}"
        secret_key_bytes = secret_key.encode("utf-8")
        cycled_key = cycle(secret_key_bytes)
        decrypted_bytes = bytearray(b ^ next(cycled_key) for b in encrypted_bytes)
        return decrypted_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return None


def resolve_bunkr(url: str) -> str:
    api_resp = fetch_bunkr_api(url)
    if not api_resp:
        print("ERROR: Failed to fetch Bunkr API", file=sys.stderr)
        sys.exit(1)
    download_link = decrypt_url(api_resp)
    if not download_link:
        print("ERROR: Failed to decrypt URL", file=sys.stderr)
        sys.exit(1)
    print(download_link)
    sys.exit(0)


if __name__ == "__main__":
    url = sys.argv[1]
    if is_bunkr_url(url):
        resolve_bunkr(url)