
import requests, yaml, time
from bs4 import BeautifulSoup

LOGIN_URL = "https://github.com/session"
HOME_URL = "https://github.com/"

def github_login():
    with open("credentials.yaml", "r") as f:
        creds = yaml.safe_load(f)
    USERNAME = creds["github"]["username"]
    PASSWORD = creds["github"]["password"]

    session = requests.Session()
    start_time = time.time()

    try:
        login_page = session.get("https://github.com/login", timeout=15)
        soup = BeautifulSoup(login_page.text, "html.parser")
        token = soup.find("input", {"name": "authenticity_token"}).get("value")

        payload = {
            "login": USERNAME,
            "password": PASSWORD,
            "authenticity_token": token,
        }

        response = session.post(LOGIN_URL, data=payload, timeout=15)

        elapsed = round(time.time() - start_time, 2)
        if USERNAME.lower() in response.text.lower():
            print(f"✅ GitHub login successful in {elapsed} sec")
            return True, elapsed
        else:
            print("❌ GitHub login failed")
            return False, elapsed
    except Exception as e:
        print(f"Error during login: {e}")
        return False, 0

if __name__ == "__main__":
    github_login()
