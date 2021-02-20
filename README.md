# About
Scraping tool for [Yahoo!不動産](https://realestate.yahoo.co.jp/).

# Requirements
This tool has been tested in environment with the following configuration:

- Python 3.7.3
- Chromium 87.0.4280.141
- Chromedriver 87.0.4280.141

# Installation

```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install .
```

# Usage

## Scraping rental page URLs for given prefecture in batch
The following command will scrape rental page URLS for certain prefecture.
The scraped URLs will be outputted into pickle formatted files with filename
`rent_<city_name>.pkl` (e.g. rent_千代田区.pkl).

```bash
   $ yahoo_fudosan rent listing-urls-batch [OPTIONS] RENT_CATEGORY_SEARCH_URL
```

Example

```bash
   $ yahoo_fudosan rent listing-urls-batch https://realestate.yahoo.co.jp/rent/03/13/a/
```

### OPTIONS

```
   -h, --help                       Print this help text and exit
   -p, --pause                      Scraping pause interval in seconds
   -m, --max_retry                  Maximum retry count if scraper
                                    unable to fetch the target data
   -o, --output_dir                 Output directory path for pickle
                                    formatted file containing scraped
                                    rental page URLs
```

## Scraping rental data to CSV files in batch

```bash
   $ yahoo_fudosan rent listing-data-batch [OPTIONS]
```

### OPTIONS

```
   -h, --help                       Print this help text and exit
   -p, --pause                      Scraping pause interval in seconds
   -m, --max_retry                  Maximum retry count if scraper
                                    unable to fetch the target data
   -P, --prefix                     Scrape rental page URLs from pickle
                                    formatted file with filename starts
                                    with `prefix` value.
                                    Default value is `rent_`.
   -i, --input_dir                  Input directory path containing pickle
                                    formatted file of rental page URL list
   -o, --output_dir                 Output directory path for CSV file
                                    containing scraped rental data
```
