import time, requests
from bs4 import BeautifulSoup
from typing import Dict, Any

def validate_site(site: Dict[str, Any], global_cfg: Dict[str, Any]) -> Dict[str, Any]:
    url = site["url"]
    start_time = time.time()
    result = {
        "SiteURL": url,
        "Success/Fail": "Fail",
        "TimeTaken": 0,
        "ValidatedText": ""
    }

    try:
        headers = {"User-Agent": global_cfg.get("user_agent")}
        timeout = int(global_cfg.get("timeout_sec", 10))

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        validations = []

        # Title
        title = soup.title.string.strip() if soup.title else None
        if title:
            validations.append(f"Title: {title}")

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            validations.append(f"Meta Description: {meta_desc['content']}")

        # Nav and footer
        if soup.find('nav'):
            validations.append("Navigation bar found")
        if soup.find('footer'):
            validations.append("Footer found")

        # Canonical link
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            validations.append(f"Canonical URL: {canonical['href']}")

        # Security headers
        head_response = requests.head(url, headers=headers, timeout=timeout)
        security_headers = ['Content-Security-Policy', 'X-Frame-Options', 'Strict-Transport-Security']
        for header in security_headers:
            if head_response.headers.get(header):
                validations.append(f"{header} present")

        # Robots.txt
        robots_url = url.rstrip('/') + "/robots.txt"
        try:
            robots_response = requests.get(robots_url, headers=headers, timeout=5)
            if robots_response.status_code == 200:
                validations.append("robots.txt found")
        except Exception:
            pass

        # Visible text sample
        text = soup.get_text(separator=' ', strip=True)
        if text:
            validations.append(f"Sample Text: {text[:300]}")

        result["Success/Fail"] = "Success"
        result["ValidatedText"] = " | ".join(validations)

    except Exception as e:
        result["ValidatedText"] = f"Error: {str(e)}"

    result["TimeTaken"] = round(time.time() - start_time, 2)
    return result
