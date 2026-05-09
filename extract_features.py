import re

def extract_features(url):
    features = {}


url_lower = url.lower()

# Basic features
features["has_http"] = 1 if url.startswith("http://") else 0
features["has_https"] = 1 if url.startswith("https://") else 0
features["has_at"] = 1 if "@" in url else 0
features["has_dash"] = 1 if "-" in url else 0
features["url_length"] = len(url)

# Suspicious keywords
suspicious_keywords = ["login", "verify", "bank", "update", "secure", "account"]
features["keyword_count"] = sum(word in url_lower for word in suspicious_keywords)

# Number of dots
features["dot_count"] = url.count(".")

# IP address detection
features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

# Suspicious TLDs
features["suspicious_tld"] = 1 if any(tld in url_lower for tld in [".tk", ".ml", ".ga", ".cf"]) else 0

return features


