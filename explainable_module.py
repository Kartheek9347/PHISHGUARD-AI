def explain(features):

    reasons = []

    if features.get("has_ip"):
        reasons.append("URL contains IP address")

    if features.get("domain_age") == 0:
        reasons.append("Newly registered domain")

    if features.get("redirect_count", 0) > 2:
        reasons.append("Multiple redirects detected")

    if features.get("contains_login_form"):
        reasons.append("Login form detected")

    return reasons