
import scrapy
import yaml
import pathlib

class WikiLoginSpider(scrapy.Spider):
    name = "wiki_login"

    def start_requests(self):
        creds_file = pathlib.Path("credentials.yaml")
        if not creds_file.exists():
            self.log("⚠️ credentials.yaml missing")
            return
        with open(creds_file, "r") as f:
            creds = yaml.safe_load(f)
        self.username = creds["wikipedia"]["username"]
        self.password = creds["wikipedia"]["password"]

        return [scrapy.FormRequest(
            url="https://en.wikipedia.org/w/api.php",
            formdata={
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json",
            },
            callback=self.get_token
        )]

    def get_token(self, response):
        token = response.json()["query"]["tokens"]["logintoken"]

        return scrapy.FormRequest(
            url="https://en.wikipedia.org/w/api.php",
            formdata={
                "action": "login",
                "lgname": self.username,
                "lgpassword": self.password,
                "lgtoken": token,
                "format": "json",
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if response.json().get("login", {}).get("result") == "Success":
            self.log("✅ Wikipedia login successful")
        else:
            self.log("❌ Wikipedia login failed")
