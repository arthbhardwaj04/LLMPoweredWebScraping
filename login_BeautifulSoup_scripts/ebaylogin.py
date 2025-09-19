
import requests
from bs4 import BeautifulSoup
import time, yaml

LOGIN_URL = "https://signin.ebay.com/ws/eBayISAPI.dll?SignIn"
HOME_URL = "https://www.ebay.com/"

def ebay_login():
    with open("credentials.yaml", "r") as f:
        creds = yaml.safe_load(f)
    EMAIL = creds["ebay"]["username"]
    PASSWORD = creds["ebay"]["password"]

    session = requests.Session()
    start_time = time.time()

    try:
        login_page = session.get(LOGIN_URL, timeout=15)
        soup = BeautifulSoup(login_page.text, "html.parser")

        form = soup.find("form")
        if not form:
            print("Login form not found!")
            return False, 0

        payload = {}
        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            value = input_tag.get("value", "")
            if name:
                payload[name] = value

        payload["userid"] = EMAIL
        payload["pass"] = PASSWORD

        action = form.get("action")
        post_url = action if "http" in action else LOGIN_URL
        response = session.post(post_url, data=payload, timeout=15)

        elapsed = round(time.time() - start_time, 2)
        if "Sign out" in response.text or "My eBay" in response.text:
            print(f"✅ eBay login successful in {elapsed} sec")
            return True, elapsed
        else:
            print("❌ eBay login failed")
            return False, elapsed
    except Exception as e:
        print(f"Error during login: {e}")
        return False, 0

if __name__ == "__main__":
    ebay_login()
