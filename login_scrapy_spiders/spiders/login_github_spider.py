
import scrapy
import yaml
import pathlib

class GithubLoginSpider(scrapy.Spider):
    name = "github_login"

    def start_requests(self):
        creds_file = pathlib.Path("credentials.yaml")
        if not creds_file.exists():
            self.log("⚠️ credentials.yaml missing")
            return
        with open(creds_file, "r") as f:
            creds = yaml.safe_load(f)
        self.username = creds["github"]["username"]
        self.password = creds["github"]["password"]

        return [scrapy.Request("https://github.com/login", callback=self.parse_login)]

    def parse_login(self, response):
        auth_token = response.css('input[name="authenticity_token"]::attr(value)').get()

        formdata = {
            "login": self.username,
            "password": self.password,
            "authenticity_token": auth_token,
        }

        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.after_login
        )

    def after_login(self, response):
        if self.username.lower() in response.text.lower():
            self.log("✅ GitHub login successful")
        else:
            self.log("❌ GitHub login failed")
