# Cyclistic Bike-Share Analysis

**Google Data Analytics Capstone Case Study**

How do annual members and casual riders use Cyclistic bikes differently? This project analyzes 12 months (Aug 2025–Jul 2026) of real Chicago bike-share trip data — over 6 million rides — to answer that question and recommend a marketing strategy for converting casual riders into annual members.

📄 **[Read the full report](./Cyclistic_Case_Study.docx)**

## Business Task

Cyclistic's Director of Marketing believes converting casual riders into annual members is key to future growth. This analysis identifies the behavioral differences between the two rider types to inform that strategy.

## Tools Used

- **SQL (DuckDB)** — combining, cleaning, and aggregating 6M+ rows across 12 monthly CSV files
- **Python** — running the SQL pipeline and exporting summary tables
- **Matplotlib** — data visualization
- **Git / GitHub** — version control

## Data Source

[Divvy trip data](https://divvy-tripdata.s3.amazonaws.com/index.html), provided under license by Motivate International Inc. Raw data files are excluded from this repo via `.gitignore` due to size; scripts (`clean_data.py`) will regenerate the cleaned dataset from the source CSVs.

## Process

1. **Prepare & Process** (`clean_data.py`) — combined 12 monthly CSVs (6,037,968 rows), removed duplicates and invalid records, added calculated fields (ride length, day of week, month) → 6,037,904 clean rows
2. **Analyze** (`analyze.py`) — aggregated ride length, day-of-week patterns, seasonality, top stations, and bike type preference by rider type; exported results as `summary_*.csv`
3. **Share** — findings and visualizations compiled into the final report

## Key Findings

| Dimension | Annual Members | Casual Riders |
|---|---|---|
| Avg. ride length | 12.4 min | 21.2 min |
| Day-of-week pattern | Weekday-heavy (commuting) | Weekend-heavy (leisure) |
| Seasonality | Relatively stable year-round | Extreme summer spike, near-zero in winter |
| Top stations | Downtown business district | Lakefront & tourist landmarks (Navy Pier, Millennium Park) |

**Members use Cyclistic as reliable, everyday transportation. Casual riders use it recreationally, concentrated on summer weekends near tourist attractions.**

## Recommendations

1. Launch a discounted "Weekend Rider" membership tier
2. Target marketing at top casual-rider stations (Navy Pier, lakefront, Millennium Park)
3. Run a summer "lock in your rate" campaign to capture casual riders during peak engagement

Full detail, charts, and methodology in the [final report](./Cyclistic_Case_Study.docx).