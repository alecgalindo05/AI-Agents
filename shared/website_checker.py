import ssl
import socket
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


def _has_ssl(domain: str) -> bool:
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
        return True
    except Exception:
        return False


def _is_mobile_friendly(soup: BeautifulSoup) -> bool:
    return soup.find("meta", attrs={"name": "viewport"}) is not None


def _years_since_update(response: requests.Response) -> int | None:
    last_modified = response.headers.get("Last-Modified")
    if last_modified:
        try:
            dt = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
            return int((datetime.now() - dt).days / 365)
        except Exception:
            pass
    return None


def classify_website(url: str | None) -> dict:
    """
    Returns:
      {'status': 'none' | 'outdated' | 'modern', 'reasons': [list of strings]}
    """
    if not url:
        return {"status": "none", "reasons": []}

    try:
        response = requests.get(
            url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return {"status": "none", "reasons": ["website could not be reached"]}

    domain = urlparse(url).netloc
    reasons = []

    if not _has_ssl(domain):
        reasons.append("no SSL / not https")
    if not _is_mobile_friendly(soup):
        reasons.append("not mobile friendly")

    years_old = _years_since_update(response)
    if years_old and years_old >= 2:
        reasons.append(f"last updated ~{years_old} years ago")

    if soup.find("table", attrs={"cellpadding": True}) or soup.find("font"):
        reasons.append("uses outdated HTML")

    return {"status": "outdated" if reasons else "modern", "reasons": reasons}
