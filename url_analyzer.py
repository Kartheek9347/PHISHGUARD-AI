import re
from urllib.parse import urlparse


def analyze_url(url):

    score = 0
    reasons = []

    # ================= DEFANGED URL DETECTION =================

    if "[.]" in url:

        score += 35

        reasons.append(
            "Defanged URL notation commonly used in phishing/threat reports"
        )

    # ================= URL NORMALIZATION =================

    url = url.strip()

    url = url.replace("[.]", ".")

    url = url.replace("..", ".")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ================= URL PARSING =================

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    main_domain = domain.split(".")[0]

    # ================= SUSPICIOUS DATA =================

    suspicious_tlds = [
        ".xyz",
        ".top",
        ".info",
        ".zip",
        ".click",
        ".gq",
        ".work",
        ".support",
        ".country",
        ".review"
    ]

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

    url_shorteners = [
        "bit.ly",
        "tinyurl.com",
        "goo.gl",
        "t.co",
        "ow.ly",
        "is.gd"
    ]

    famous_brands = [
        "paypal",
        "google",
        "facebook",
        "microsoft",
        "apple",
        "amazon",
        "netflix",
        "fedex",
        "dhl",
        "ups",
        "bankofamerica",
        "chase"
    ]

    lookalike_domains = {
        "paypa1": "paypal",
        "facebok": "facebook",
        "micorsoft": "microsoft",
        "googl": "google",
        "amazn": "amazon",
        "fedexpress": "fedex"
    }

    # ================= BASIC RULES =================

    if "@" in url:

        score += 20

        reasons.append(
            "URL contains @ symbol"
        )

    if url.startswith("http://"):

        score += 25

        reasons.append(
            "Uses insecure HTTP"
        )

    if len(url) > 75:

        score += 10

        reasons.append(
            "URL is unusually long"
        )

    if url.count(".") > 5:

        score += 10

        reasons.append(
            "Too many subdomains"
        )

    # ================= ADVANCED RULES =================

    # Hyphen + phishing keyword

    if "-" in domain and any(
        word in domain
        for word in suspicious_keywords
    ):

        score += 15

        reasons.append(
            "Hyphen with suspicious keyword detected"
        )

    # ================= SUSPICIOUS TLD =================

    for tld in suspicious_tlds:

        if domain.endswith(tld):

            score += 20

            reasons.append(
                f"Suspicious domain extension: {tld}"
            )

            break

    # ================= URL SHORTENER =================

    for shortener in url_shorteners:

        if shortener in domain:

            score += 25

            reasons.append(
                "URL shortener detected"
            )

            break

    # ================= IP ADDRESS =================

    if re.search(
        r"\d+\.\d+\.\d+\.\d+",
        domain
    ):

        score += 30

        reasons.append(
            "IP address used instead of domain"
        )

    # ================= PUNYCODE / HOMOGRAPH =================

    if "xn--" in domain:

        score += 35

        reasons.append(
            "Possible homograph attack detected"
        )

    # ================= PHISHING KEYWORDS =================

    keyword_hits = 0

    for word in suspicious_keywords:

        if word in url.lower():
            keyword_hits += 1

    if keyword_hits >= 2:

        score += 20

        reasons.append(
            "Multiple phishing-related keywords detected"
        )

    # ================= BRAND IMPERSONATION =================

    for brand in famous_brands:

        legit_domains = [
            f"{brand}.com",
            f"www.{brand}.com"
        ]

        # Ignore legitimate domains
        if domain in legit_domains:
            continue

        if brand in domain:

            if any(
                word in domain
                for word in suspicious_keywords
            ):

                score += 25

                reasons.append(
                    f"Possible impersonation of {brand}"
                )

                break

    # ================= LOOKALIKE DETECTION =================

    for fake, original in lookalike_domains.items():

        if (
            main_domain == fake or
            main_domain.startswith(fake + "-")
        ):

            score += 40

            reasons.append(
                f"Lookalike domain detected ({fake} → {original})"
            )

            break

    # ================= DOUBLE EXTENSION =================

    if re.search(
        r"\.(pdf|doc|xls|jpg|png)\.exe$",
        path
    ):

        score += 40

        reasons.append(
            "Double file extension detected"
        )

    # ================= OPEN REDIRECT =================

    redirect_patterns = [
        "redirect=",
        "url=",
        "next=",
        "return=",
        "target="
    ]

    for pattern in redirect_patterns:

        if pattern in url.lower():

            score += 15

            reasons.append(
                "Possible open redirect detected"
            )

            break

    # ================= SUBDOMAIN PADDING =================

    for brand in famous_brands:

        if (
            brand in domain and
            domain.count(".") >= 3
        ):

            score += 20

            reasons.append(
                "Possible subdomain padding attack"
            )

            break

    # ================= FINAL SCORE =================

    score = min(score, 100)

    # ================= SEVERITY =================

    if score < 40:

        severity = "Low Risk"

    elif score < 65:

        severity = "Moderate Risk"

    elif score < 85:

        severity = "High Risk"

    else:

        severity = "Critical Threat"

    return score, severity, reasons