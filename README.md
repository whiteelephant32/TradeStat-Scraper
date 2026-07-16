# TradeStat Scraper

A Python-based web scraper for downloading **Indian Import and Export commodity reports** from the **TradeStat Portal** provided by the **Department of Commerce, Government of India**.

The project automates form submission, handles CSRF tokens and HTTP sessions, extracts tabular data, and saves the results as structured CSV files for further analysis.

---

## Features

- Scrapes **Export** and **Import** commodity reports.
- Handles CSRF tokens automatically.
- Maintains HTTP sessions using `requests.Session()`.
- Extracts:
  - Category-wise commodity data
  - Detailed commodity data
- Cleans and structures scraped data using Pandas.
- Generates separate CSV files for every month and year.
- Covers historical data from **2010 onwards**.

---

## Current Scraping Configuration

The scraper is currently configured for the following TradeStat report:

| Setting | Value |
|---------|-------|
| Module | System on Foreign Trade Performance Analysis (FTPA) |
| Report | Commodity Group-wise |
| Report Type | Detailed Report |
| Trade Value | US$ Millions |
| Trade Types | Export & Import |
| Time Period | January 2010 – Present (Currently up to 2026) |
| Output Format | CSV |

---

## Repository Structure

```
TradeStat-Scraper/
│
├── scrape_export.py
├── scrape_import.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

- Python 3
- Requests
- BeautifulSoup4
- Pandas

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/TradeStat-Scraper.git
```

Move into the project directory:

```bash
cd TradeStat-Scraper
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

---

## Usage

### Export Data

```bash
python scrape_export.py
```

### Import Data

```bash
python scrape_import.py
```

---

## Output

For each selected month and year, the scraper generates two CSV files:

### Detailed Commodity Report

```
outputDetailed_<year>_<month>.csv
```

### Category-wise Commodity Report

```
outputCategory_<year>_<month>.csv
```

Example:

```
outputDetailed_2026_1.csv
outputCategory_2026_1.csv
```

---

## Data Source

Department of Commerce, Government of India

TradeStat Portal

https://tradestat.commerce.gov.in/

---

## Disclaimer

This project is intended for educational, research, and data analysis purposes only.

The scraped data belongs to the Government of India. Users should comply with the website's terms of use and applicable policies when using the data.

---


## Author

Developed by **whiteelephant32**
