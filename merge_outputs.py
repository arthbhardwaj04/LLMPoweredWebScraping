import pandas as pd
import pathlib

def main():
    bs4_file = pathlib.Path("outputs/nologin_validation_results.csv")
    scrapy_file = pathlib.Path("outputs/nologin_validation_results_scrapy.csv")
    merged_file = pathlib.Path("outputs/nologin_validation_results_merged.csv")

    if not bs4_file.exists() or not scrapy_file.exists():
        print("Error: run both BeautifulSoup and Scrapy first to generate results.")
        return

    bs4_df = pd.read_csv(bs4_file)
    bs4_df["Engine"] = "bs4"

    scrapy_df = pd.read_csv(scrapy_file)
    scrapy_df["Engine"] = "scrapy"

    merged = pd.concat([bs4_df, scrapy_df], ignore_index=True)
    merged.to_csv(merged_file, index=False)
    print(f"Merged results saved to {merged_file}")

if __name__ == "__main__":
    main()
