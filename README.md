# Refactored Site Validator

This version keeps exactly the same CSV columns and validation logic as your original script, but is split into multiple files and uses a config file.

## Files
- `logger_setup.py` – logging setup
- `config_loader.py` – loads sites.yaml
- `scraper.py` – validation logic (same as original)
- `main.py` – orchestrator, writes CSV

## Config
Edit `sites.yaml` to set which sites to check.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python main.py --config sites.yaml --out outputs/nologin_validation_results.csv
```

Logs go to `logs/run.log`. Results CSV has same 4 columns: SiteURL, Success/Fail, TimeTaken, ValidatedText.


## Run with Scrapy
Install scrapy if not already:

```bash
pip install scrapy
```

Run the spider:

```bash
scrapy runspider scrapy_project/spiders/validator_spider.py -o outputs/nologin_validation_results_scrapy.csv
```

## Merge Results
After running both BeautifulSoup and Scrapy:

```bash
pip install pandas
python merge_outputs.py
```

This creates `outputs/nologin_validation_results_merged.csv` with all results combined and an extra column `Engine` (bs4 or scrapy).


## Unified Usage with --engine

Now you can choose which engine(s) to run using `--engine`:

- Run BeautifulSoup only:
  ```bash
  python main.py --engine bs4 --config sites.yaml --out outputs/nologin_validation_results.csv
  ```

- Run Scrapy only:
  ```bash
  python main.py --engine scrapy
  ```

- Run both (BeautifulSoup + Scrapy) and auto-merge:
  ```bash
  python main.py --engine both
  ```

Outputs:
- `outputs/nologin_validation_results.csv` → BeautifulSoup
- `outputs/nologin_validation_results_scrapy.csv` → Scrapy
- `outputs/nologin_validation_results_merged.csv` → Combined with Engine column
