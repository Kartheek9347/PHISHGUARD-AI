import re
from urllib.parse import urlparse

def extract_features(url):

    # ================= URL NORMALIZATION =================

    url = url.strip()

    url = url.replace("[.]", ".")

    url = url.replace("..", ".")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ================= INITIAL SETUP =================

    features = {}

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    # ================= BASIC FEATURES =================

    features["has_http"] = (
        1 if url.startswith("http://") else 0
    )

    features["has_https"] = (
        1 if url.startswith("https://") else 0
    )

    features["has_at"] = (
        1 if "@" in url else 0
    )

    features["has_dash"] = (
        1 if "-" in domain else 0
    )

    features["url_length"] = len(url)

    features["dot_count"] = url.count(".")

    # ================= SUSPICIOUS KEYWORDS =================

    suspicious_keywords = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "bank",
        "billing",
        "password",
        "tracking",
        "delivery",
        "support",
        "confirm"
    ]

    features["keyword_count"] = sum(
        word in url.lower()
        for word in suspicious_keywords
    )

    # ================= IP ADDRESS =================

    features["has_ip"] = (
        1 if re.search(
            r"\d+\.\d+\.\d+\.\d+",
            domain
        ) else 0
    )

    # ================= SUSPICIOUS TLD =================

    suspicious_tlds = [
        ".xyz",
        ".top",
        ".info",
        ".zip",
        ".click",
        ".gq",
        ".work"
    ]

    features["suspicious_tld"] = (
        1 if any(
            domain.endswith(tld)
            for tld in suspicious_tlds
        ) else 0
    )

    # ================= URL SHORTENER =================

    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "goo.gl",
        "t.co",
        "ow.ly"
    ]

    features["url_shortener"] = (
        1 if any(
            short in domain
            for short in shorteners
        ) else 0
    )

    # ================= PUNYCODE =================

    features["punycode_attack"] = (
        1 if "xn--" in domain else 0
    )

    # ================= DOUBLE EXTENSION =================

    features["double_extension"] = (
        1 if re.search(
            r"\.(pdf|doc|xls|jpg|png)\.exe$",
            path
        ) else 0
    )

    # ================= SUBDOMAIN COUNT =================

    features["subdomain_count"] = domain.count(".")

    # ================= OPEN REDIRECT =================

    redirect_keywords = [
        "redirect=",
        "url=",
        "next=",
        "return="
    ]

    features["open_redirect"] = (
        1 if any(
            word in url.lower()
            for word in redirect_keywords
        ) else 0
    )

    # ================= BRAND IMPERSONATION =================

    famous_brands = [
        "paypal",
        "google",
        "facebook",
        "microsoft",
        "amazon",
        "apple",
        "netflix",
        "fedex",
        "dhl",
        "ups"
    ]

    impersonation = 0

    for brand in famous_brands:

        if brand in domain:

            impersonation = 1
            break

    features["brand_impersonation"] = impersonation

    # ================= LOOKALIKE DOMAIN =================

    lookalikes = [
        "paypa1",
        "facebok",
        "micorsoft",
        "googl",
        "amazn",
        "fedexpress"
    ]

    features["lookalike_domain"] = (
        1 if any(
            fake in domain
            for fake in lookalikes
        ) else 0
    )

    return features