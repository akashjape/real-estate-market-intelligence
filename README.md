# real-estate-market-intelligence

📘 Project Title

Real Estate Pricing & Market Intelligence (Web Scraping + MySQL + Tableau)

📖 Project Overview

This project extracts real estate listings from MagicBricks / 99acres, cleans and stores them in MySQL, and builds interactive Tableau dashboards to analyze price trends, locality insights, amenity ROI, and builder comparisons.

The goal is to create a complete end-to-end Data Engineering + Data Analytics pipeline.

🎯 Objectives

Scrape real estate listings daily/weekly

Store raw + cleaned data in a structured MySQL database

Analyze pricing trends across neighborhoods

Identify which amenities drive price changes

Create visual dashboards for actionable insights

Build a scalable & re-usable data pipeline

🛠️ Tech Stack

Python (Web Scraping, Data Cleaning)

BeautifulSoup / Selenium

MySQL (Database & Querying)

Pandas / NumPy

Tableau (Visualization)

GitHub (Version Control & Documentation)
# 📂 Project Structure: Real Estate Market Intelligence

real-estate-market-intelligence/
│
├── scraper/                     # All web scraping scripts
│   ├── main_scraper.py          # Main scraper file
│   ├── config.py                # Headers, URLs, settings
│   ├── helpers/                 # Utility scripts
│   │   ├── utils.py
│   │   └── parser.py
│   └── raw_data/                # Raw scraped data before cleaning
│       └── *.json / *.csv
│
├── database/                    # MySQL schema and data
│   ├── schema.sql               # Full DB schema
│   ├── create_tables.sql        # DDL scripts
│   ├── insert_cleaned_data.sql  # Insert statements
│   └── cleaned_csvs/            # Cleaned datasets ready for upload
│       └── *.csv
│
├── notebooks/                   # Jupyter notebooks for analysis & cleaning
│   ├── data_cleaning.ipynb
│   ├── preprocessing.ipynb
│   └── exploratory_analysis.ipynb
│
├── tableau/                     # Tableau dashboards and extracts
│   ├── dashboards/              # Packaged workbooks
│   │   └── *.twbx
│   └── extracts/                # Tableau extract files
│       └── *.hyper
│
├── logs/                        # Daily Work Log – VERY important for progress
│   ├── day1.md
│   ├── day2.md
│   ├── day3.md
│   └── ...
│
├── notes/                       # Planning, ideas & documentation
│   ├── project_notes.md
│   ├── tasks_todo.md
│   └── meeting_notes.md
│
├── images/                      # Screenshots, ER diagrams, charts
│   └── *.png / *.jpg
│
└── README.md                    # Project documentation (main file)

📊 Dashboards to Build
1️⃣ Price Heatmap

City-level + locality-level heat visualization

Filters: BHK, property type, price range

2️⃣ Neighborhood Comparison

Avg price

Price per sq. ft.

Property size distribution

3️⃣ Amenity ROI Impact

Which amenities increase price?

Price difference for amenity vs no-amenity

4️⃣ Builder-Level Insights

Builder pricing patterns

Premium vs budget builders

5️⃣ Price Distribution Analysis

Histogram

Box plot for outliers

BHK-wise comparison

📥 Data Source

Websites: MagicBricks / 99acres

Data collected via scraping:

Property price

BHK

Area (sq.ft.)

Amenities

Locality

Builder

Listing date

⚠️ Scraped ethically with delays, user-agents, and no login-protected pages.

🗄️ Database Schema
Main Tables

property

locality

amenities

property_amenities

price_history

ER Diagram

(Add later under /images/schema.png)

📝 Daily Progress Log

Daily updates are available in:
/logs/day1.md
/logs/day2.md
...

🚀 How to Run the Project
1. Clone the Repository -> git clone https://github.com/<your-username>/real-estate-market-intelligence.git
2. Install requirements -> pip install -r requirements.txt
3. Run the scraper -> python scraper/main_scraper.py
4. Load cleaned data into MySQL
Run SQL scripts inside:
/database/create_tables.sql
/database/insert_cleaned_data.sql

5. Connect Tableau to MySQL

Use Tableau → MySQL connector → select views → build dashboards.

🔮 Future Enhancements

Predict price using ML models

Add rent vs buy comparison

Scheduler for automated scraping

Deploy dashboards publicly using Tableau Public



