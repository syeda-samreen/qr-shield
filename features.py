import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update",
                    "bank", "paypal", "signin", "confirm", "password"]
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]


def get_hostname(url):
    if "://" not in url:
        url = "http://" + url
    try:
        return urlparse(url).netloc
    except ValueError:
        rest = url.split("://", 1)[1]
        return rest.split("/")[0]


def url_length(url):
    return len(url)


def count_dots(url):
    return url.count(".")  


def count_hyphens(url):
    return url.count("-")


def has_at_symbol(url):
    return 1 if "@" in url else 0


def uses_ip_address(url):
    host = get_hostname(url)
    return 1 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host) else 0


def count_subdomains(url):
    host = get_hostname(url)
    parts = host.split(".")
    return max(len(parts) - 2, 0)


def count_suspicious_words(url):
    lower = url.lower()
    return sum(1 for word in SUSPICIOUS_WORDS if word in lower)


def is_shortener(url):
    host = get_hostname(url).lower()
    return 1 if host in SHORTENERS else 0


def count_digits(url):
    return sum(ch.isdigit() for ch in url)

def count_slashes(url):
    return url.count("/")


def count_special_chars(url):
    return sum(url.count(c) for c in "?=&%_")


def hostname_length(url):
    return len(get_hostname(url))


def extract_features(url):
    return {
        "url_length": url_length(url),
        "dots": count_dots(url),
        "has_at": has_at_symbol(url),
        "uses_ip": uses_ip_address(url),
        "subdomains": count_subdomains(url),
        "suspicious_words": count_suspicious_words(url),
        "is_shortener": is_shortener(url),
        "digits": count_digits(url),
        "hyphens": count_hyphens(url),
                "slashes": count_slashes(url),
        "special_chars": count_special_chars(url),
        "hostname_length": hostname_length(url),
    }


if __name__ == "__main__":
    test_urls = [
        "google.com",
        "paypal.com.secure-login.example.xyz/verify",
        "http://192.168.1.1/login@bank.com",
        "bit.ly/3abcXYZ",
    ]
    for u in test_urls:
        print(u)
        print("  ", extract_features(u))



