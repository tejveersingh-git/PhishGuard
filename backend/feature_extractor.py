import re
import socket
import urllib.parse
from datetime import datetime

import requests
import whois
from bs4 import BeautifulSoup


def get_domain(url):
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc
    except:
        return ""


def fetch_page(url, timeout=5):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        return resp.text
    except:
        return ""


# ── 30 FEATURE FUNCTIONS ──────────────────────────────────────────

def having_ip_address(url):
    pattern = re.compile(
        r"(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])"
    )
    return -1 if pattern.search(url) else 1


def url_length(url):
    l = len(url)
    if l < 54:
        return 1
    elif l <= 75:
        return 0
    return -1


def shortening_service(url):
    pattern = r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|tiny\.cc|bitly\.com"
    return -1 if re.search(pattern, url) else 1


def having_at_symbol(url):
    return -1 if "@" in url else 1


def double_slash_redirecting(url):
    pos = url.rfind("//")
    return -1 if pos > 6 else 1


def prefix_suffix(url):
    domain = get_domain(url)
    return -1 if "-" in domain else 1


def having_sub_domain(url):
    domain = get_domain(url)
    dots = domain.count(".")
    if dots == 1:
        return 1
    elif dots == 2:
        return 0
    return -1


def ssl_final_state(url):
    return 1 if url.startswith("https") else -1


def domain_registration_length(url):
    try:
        domain = get_domain(url)
        w = whois.whois(domain)
        exp = w.expiration_date
        if isinstance(exp, list):
            exp = exp[0]
        if exp:
            remaining = (exp - datetime.now()).days
            return 1 if remaining > 365 else -1
    except:
        pass
    return -1


def favicon(url, page=""):
    try:
        if not page:
            page = fetch_page(url)
        soup = BeautifulSoup(page, "html.parser")
        icon = soup.find("link", rel=lambda r: r and "icon" in r.lower())
        if icon and icon.get("href"):
            href = icon["href"]
            domain = get_domain(url)
            if domain in href or href.startswith("/"):
                return 1
            return -1
    except:
        pass
    return 1


def port(url):
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.port:
            safe_ports = {80, 443, 21, 22, 25, 53, 110, 143}
            return 1 if parsed.port in safe_ports else -1
    except:
        pass
    return 1


def https_token(url):
    domain = get_domain(url)
    return -1 if "https" in domain.lower() else 1


def request_url(url, page=""):
    try:
        if not page:
            page = fetch_page(url)
        soup = BeautifulSoup(page, "html.parser")
        domain = get_domain(url)
        total, external = 0, 0
        for tag in soup.find_all(["img", "script", "link"], src=True):
            src = tag.get("src", "")
            total += 1
            if src and domain not in src and src.startswith("http"):
                external += 1
        if total == 0:
            return 1
        ratio = external / total
        if ratio < 0.22:
            return 1
        elif ratio < 0.61:
            return 0
        return -1
    except:
        return 1


def url_of_anchor(url, page=""):
    try:
        if not page:
            page = fetch_page(url)
        soup = BeautifulSoup(page, "html.parser")
        domain = get_domain(url)
        anchors = soup.find_all("a", href=True)
        total = len(anchors)
        unsafe = sum(1 for a in anchors if (
            a["href"] in ["#", "javascript:void(0)"] or
            (a["href"].startswith("http") and domain not in a["href"])
        ))
        if total == 0:
            return 1
        ratio = unsafe / total
        if ratio < 0.31:
            return 1
        elif ratio < 0.67:
            return 0
        return -1
    except:
        return 1


def links_in_tags(url, page=""):
    try:
        if not page:
            page = fetch_page(url)
        soup = BeautifulSoup(page, "html.parser")
        domain = get_domain(url)
        total, external = 0, 0
        for tag in soup.find_all(["meta", "script", "link"]):
            src = tag.get("src") or tag.get("href") or ""
            if src:
                total += 1
                if domain not in src and src.startswith("http"):
                    external += 1
        if total == 0:
            return 1
        ratio = external / total
        if ratio < 0.17:
            return 1
        elif ratio < 0.81:
            return 0
        return -1
    except:
        return 1


def sfh(url, page=""):
    try:
        if not page:
            page = fetch_page(url)
        soup = BeautifulSoup(page, "html.parser")
        domain = get_domain(url)
        for form in soup.find_all("form", action=True):
            action = form["action"]
            if action in ["", "about:blank"]:
                return -1
            if domain not in action and action.startswith("http"):
                return 0
        return 1
    except:
        return 1


def submitting_to_email(url, page=""):
    if not page:
        page = fetch_page(url)
    return -1 if "mailto:" in page.lower() else 1


def abnormal_url(url):
    try:
        domain = get_domain(url)
        w = whois.whois(domain)
        if w.domain_name:
            reg = w.domain_name
            if isinstance(reg, list):
                reg = reg[0]
            return 1 if reg.lower() in domain.lower() else -1
    except:
        pass
    return -1


def redirect(url):
    try:
        resp = requests.get(url, timeout=5, allow_redirects=True)
        if len(resp.history) <= 1:
            return 1
        elif len(resp.history) <= 4:
            return 0
        return -1
    except:
        return 1


def on_mouseover(url, page=""):
    if not page:
        page = fetch_page(url)
    return -1 if "onmouseover" in page.lower() else 1


def right_click(url, page=""):
    if not page:
        page = fetch_page(url)
    return -1 if "event.button==2" in page else 1


def popup_window(url, page=""):
    if not page:
        page = fetch_page(url)
    return -1 if "prompt(" in page else 1


def iframe(url, page=""):
    if not page:
        page = fetch_page(url)
    return -1 if "<iframe" in page.lower() else 1


def age_of_domain(url):
    try:
        domain = get_domain(url)
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        if created:
            age = (datetime.now() - created).days
            return 1 if age >= 180 else -1
    except:
        pass
    return -1


def dns_record(url):
    try:
        socket.gethostbyname(get_domain(url))
        return 1
    except:
        return -1


def web_traffic(url):
    try:
        socket.gethostbyname(get_domain(url))
        return 1
    except:
        return -1


def page_rank(url):
    return 1 if url.startswith("https") else -1


def google_index(url):
    try:
        query = f"site:{get_domain(url)}"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(search_url, headers=headers, timeout=5)
        return 1 if "did not match any documents" not in resp.text else -1
    except:
        return -1


def links_pointing_to_page(url, page=""):
    return 0


def statistical_report(url):
    suspicious_tlds = [".xyz", ".top", ".club", ".online",
                       ".site", ".info", ".tk", ".ml", ".ga", ".cf"]
    domain = get_domain(url).lower()
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            return -1
    return 1


# ── MAIN EXTRACT FUNCTION ─────────────────────────────────────────

def extract_features(url):
    page = fetch_page(url)

    features = {
        "having_IP_Address":           having_ip_address(url),
        "URL_Length":                   url_length(url),
        "Shortening_Service":           shortening_service(url),
        "having_At_Symbol":             having_at_symbol(url),
        "double_slash_redirecting":     double_slash_redirecting(url),
        "Prefix_Suffix":                prefix_suffix(url),
        "having_Sub_Domain":            having_sub_domain(url),
        "SSLfinal_State":               ssl_final_state(url),
        "Domain_registeration_length":  domain_registration_length(url),
        "Favicon":                      favicon(url, page),
        "port":                         port(url),
        "HTTPS_token":                  https_token(url),
        "Request_URL":                  request_url(url, page),
        "URL_of_Anchor":                url_of_anchor(url, page),
        "Links_in_tags":                links_in_tags(url, page),
        "SFH":                          sfh(url, page),
        "Submitting_to_email":          submitting_to_email(url, page),
        "Abnormal_URL":                 abnormal_url(url),
        "Redirect":                     redirect(url),
        "on_mouseover":                 on_mouseover(url, page),
        "RightClick":                   right_click(url, page),
        "popUpWidnow":                  popup_window(url, page),
        "Iframe":                       iframe(url, page),
        "age_of_domain":                age_of_domain(url),
        "DNSRecord":                    dns_record(url),
        "web_traffic":                  web_traffic(url),
        "Page_Rank":                    page_rank(url),
        "Google_Index":                 google_index(url),
        "Links_pointing_to_page":       links_pointing_to_page(url, page),
        "Statistical_report":           statistical_report(url),
    }

    feature_vector = list(features.values())
    return features, feature_vector


# ── QUICK TEST ────────────────────────────────────────────────────

if __name__ == "__main__":
    test_url = "https://www.google.com"
    print(f"\nTesting: {test_url}\n")
    feats, vec = extract_features(test_url)
    for name, val in feats.items():
        status = "SAFE" if val == 1 else ("SUSPICIOUS" if val == 0 else "PHISHING")
        print(f"  {name:<35} {val:>2}   {status}")
    print(f"\nDone. Feature vector length: {len(vec)}")