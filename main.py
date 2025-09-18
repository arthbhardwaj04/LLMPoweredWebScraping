
import argparse, csv, pathlib, subprocess, sys, pandas as pd
from typing import List, Dict, Any
from logger_setup import setup_logger
from config_loader import load_config
from scraper import validate_site

def run_bs4(config: str, out_path: str, logger):
    cfg = load_config(config)
    global_cfg = cfg["global"]
    sites: List[Dict[str, Any]] = cfg["sites"]
    results: List[Dict[str, Any]] = []

    for i, site in enumerate(sites, 1):
        logger.info("(BS4 %d/%d) Validating %s", i, len(sites), site.get("url"))
        res = validate_site(site, global_cfg)
        logger.info("Result for %s: %s", site.get("url"), res["Success/Fail"])
        results.append(res)

    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["SiteURL", "Success/Fail", "TimeTaken", "ValidatedText"])
        writer.writeheader()
        writer.writerows(results)
    logger.info("BS4 results saved to %s", out_path)

def run_scrapy(out_path: str, logger):
    logger.info("Running Scrapy spider...")
    cmd = ["scrapy", "runspider", "scrapy_project/spiders/validator_spider.py", "-o", out_path]
    subprocess.run(cmd, check=False)
    logger.info("Scrapy results saved to %s", out_path)

def merge_outputs(bs4_file: str, scrapy_file: str, merged_file: str, logger):
    if not pathlib.Path(bs4_file).exists() or not pathlib.Path(scrapy_file).exists():
        logger.error("Both BS4 and Scrapy outputs must exist before merging.")
        return
    bs4_df = pd.read_csv(bs4_file)
    bs4_df["Engine"] = "bs4"
    scrapy_df = pd.read_csv(scrapy_file)
    scrapy_df["Engine"] = "scrapy"
    merged = pd.concat([bs4_df, scrapy_df], ignore_index=True)
    merged.to_csv(merged_file, index=False)
    logger.info("Merged results saved to %s", merged_file)

def main():
    p = argparse.ArgumentParser(description="Validate multiple sites with BeautifulSoup, Scrapy, or both.")
    p.add_argument("--config", default="sites.yaml", help="YAML config with sites list")
    p.add_argument("--out", default="outputs/nologin_validation_results.csv", help="Output CSV for BeautifulSoup")
    p.add_argument("--loglevel", default="INFO")
    p.add_argument("--engine", choices=["bs4", "scrapy", "both"], default="bs4", help="Which engine(s) to run")
    args = p.parse_args()

    logger = setup_logger(level=args.loglevel)

    if args.engine == "bs4":
        run_bs4(args.config, args.out, logger)
    elif args.engine == "scrapy":
        run_scrapy("outputs/nologin_validation_results_scrapy.csv", logger)
    elif args.engine == "both":
        bs4_out = "outputs/nologin_validation_results.csv"
        scrapy_out = "outputs/nologin_validation_results_scrapy.csv"
        merged_out = "outputs/nologin_validation_results_merged.csv"
        run_bs4(args.config, bs4_out, logger)
        run_scrapy(scrapy_out, logger)
        merge_outputs(bs4_out, scrapy_out, merged_out, logger)
    else:
        sys.exit("Unknown engine option.")

if __name__ == "__main__":
    main()
