print("Behavioral Engine Running")
def behavioral_analysis(url):
    behavior = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)

        html = response.text.lower()

        behavior["redirect_count"] = len(response.history)
        behavior["contains_login_form"] = 1 if "password" in html else 0
        behavior["has_iframe"] = 1 if "<iframe" in html else 0
        behavior["has_js"] = 1 if "<script" in html else 0

    except:
        behavior = {
            "redirect_count": 0,
            "contains_login_form": 0,
            "has_iframe": 0,
            "has_js": 0
        }

    return behavior