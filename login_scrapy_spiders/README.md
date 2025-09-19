
# Scrapy Login Spiders

This folder contains **sample Scrapy spiders** for logging into websites (eBay, GitHub, Wikipedia)
using credentials loaded from a `credentials.yaml` file.

## 📂 Files
- `spiders/login_ebay_spider.py` - Scrapy spider for eBay login
- `spiders/login_github_spider.py` - Scrapy spider for GitHub login
- `spiders/login_wiki_spider.py` - Scrapy spider for Wikipedia login
- `credentials.yaml.example` - Template credentials file (rename to `credentials.yaml` and fill in)

## ⚠️ Important
- Never commit your real `credentials.yaml` to GitHub. 
- Only commit the example file (`credentials.yaml.example`) and add `credentials.yaml` to your `.gitignore`.

## ▶️ How to Run
From your project root (where `scrapy.cfg` is located), run:

```bash
scrapy crawl ebay_login
scrapy crawl github_login
scrapy crawl wiki_login
```

## 🔑 Setting Up Credentials
Copy the example file and edit with your test credentials:

```bash
cp credentials.yaml.example credentials.yaml
```

Then open `credentials.yaml` and fill in your username/password for each site.
