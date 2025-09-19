
import requests, yaml, time

API_URL = "https://en.wikipedia.org/w/api.php"

def wiki_login():
    with open("credentials.yaml", "r") as f:
        creds = yaml.safe_load(f)
    USERNAME = creds["wikipedia"]["username"]
    PASSWORD = creds["wikipedia"]["password"]

    session = requests.Session()
    start_time = time.time()

    try:
        # Step 1: Get login token
        res = session.get(API_URL, params={
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }, timeout=15)
        login_token = res.json()["query"]["tokens"]["logintoken"]

        # Step 2: Send login request
        payload = {
            "action": "login",
            "lgname": USERNAME,
            "lgpassword": PASSWORD,
            "lgtoken": login_token,
            "format": "json",
        }
        r2 = session.post(API_URL, data=payload, timeout=15)

        elapsed = round(time.time() - start_time, 2)
        if r2.json().get("login", {}).get("result") == "Success":
            print(f"✅ Wikipedia login successful in {elapsed} sec")
            return True, elapsed
        else:
            print("❌ Wikipedia login failed")
            return False, elapsed
    except Exception as e:
        print(f"Error during login: {e}")
        return False, 0

if __name__ == "__main__":
    wiki_login()
