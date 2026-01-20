# Sales Analytics System

**Author:** Rahul Sharma
**Date:** 2026-01-20

## Project Overview
This project implements a modular sales analytics system that processes raw sales data to generate actionable insights. It reads sales records, enriches the data using an external currency API, and generates comprehensive reports.

## Repository Structure
```text
sales-analytics-system/
├── data/
│   └── sales_data.txt       # Raw input data
├── output/                  # Generated reports (gitignored)
├── utils/
│   ├── api_handler.py       # Handles currency conversion API
│   ├── data_processor.py    # Logic for calculating sales stats
│   └── file_handler.py      # Reads and writes files safely
├── main.py                  # Entry point of the application
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

Setup Instructions
1. Clone the repository:
git clone [https://github.com/YourUsername/sales-analytics-system.git](https://github.com/YourUsername/sales-analytics-system.git)
cd sales-analytics-system

2. Install dependencies:
pip install -r requirements.txt

How to Run
Run the main script from the root directory:
python main.py

Outputs
After running the script, the output/ folder will contain:
1. enriched_sales_data.txt: Data with converted currency values.
2. sales_report.txt: A summary report including total sales and top products.

Dependencies
1. Python 3.x
2. requests library
