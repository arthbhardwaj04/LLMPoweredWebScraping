
import scrapy
import yaml
import pathlib

class EbayLoginSpider(scrapy.Spider):
    name = "ebay_login"

    def start_requests(self):
        creds_file = pathlib.Path("credentials.yaml")
        if not creds_file.exists():
            self.log("⚠️ credentials.yaml not found")
            return
        with open(creds_file, "r") as f:
            creds = yaml.safe_load(f)
        self.username = creds["ebay"]["username"]
        self.password = creds["ebay"]["password"]

        yield scrapy.Request("https://signin.ebay.com/ws/eBayISAPI.dll?SignIn", callback=self.login)

    def login(self, response):
        formdata = {
            "userid": self.username,
            "pass": self.password,
        }
        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.after_login
        )

    def after_login(self, response):
        if "My eBay" in response.text or "Sign out" in response.text:
            self.log("✅ eBay login successful")
        else:
            self.log("❌ eBay login failed")
