import scrapy, time, requests, yaml
from bs4 import BeautifulSoup

class ValidatorSpider(scrapy.Spider):
    name = "validator"

    def start_requests(self):
        with open("sites.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.global_cfg = cfg.get("global", {})
        for site in cfg.get("sites", []):
            yield scrapy.Request(site["url"], callback=self.parse, meta={"site": site, "start_time": time.time()})

    def parse(self, response):
        site = response.meta["site"]
        url = site["url"]
        result = {
            "SiteURL": url,
            "Success/Fail": "Fail",
            "TimeTaken": 0,
            "ValidatedText": ""
        }

        start_time = response.meta["start_time"]
        validations = []
        try:
            soup = BeautifulSoup(response.text, "html.parser")

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

            # Security headers via HEAD
            try:
                head_response = requests.head(url, timeout=10)
                security_headers = ['Content-Security-Policy', 'X-Frame-Options', 'Strict-Transport-Security']
                for header in security_headers:
                    if head_response.headers.get(header):
                        validations.append(f"{header} present")
            except Exception:
                pass

            # Robots.txt
            robots_url = url.rstrip('/') + "/robots.txt"
            try:
                robots_response = requests.get(robots_url, timeout=5)
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
        yield result
