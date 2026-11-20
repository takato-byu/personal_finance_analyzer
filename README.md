# Personal Finance Analyzer

## Project Overview

Personal Finance Analyzer is a Python program developed for the BYU CS 111 Free Coding Project.

The program automatically processes bank transaction data from a CSV file, categorizes expenses, analyzes spending patterns, creates visualizations, and generates an HTML financial report.

The main goal of this project is to simplify personal financial analysis by allowing users to update a transaction CSV file and automatically generate a new report with minimal manual work.

## Features

- **Data Cleaning:** Imports CSV transaction data and processes dates, transaction amounts, and descriptions.
- **Transaction Categorization:** Automatically assigns spending categories based on keywords in transaction descriptions.
- **Category Analysis:** Calculates total spending for each expense category.
- **Monthly Analysis:** Summarizes spending by month and identifies changes in spending patterns.
- **Monthly Comparison:** Calculates dollar and percentage changes between consecutive months.
- **Data Visualization:** Creates bar charts showing monthly spending and spending by category.
- **HTML Report Generation:** Automatically generates a financial report containing summary statistics, visualizations, and spending tables.

## Main Functions

The program is organized into several functions, each responsible for a specific task.

| Function | Description |
|---|---|
| `load_transactions()` | Reads transaction data from a CSV file using pandas. |
| `clean_transactions()` | Cleans transaction data, converts dates and amounts, and creates additional variables for analysis. |
| `categorize_transaction()` | Assigns a spending category based on keywords found in a transaction description. |
| `analyze_category_spending()` | Calculates total spending for each transaction category. |
| `analyze_monthly_spending()` | Calculates monthly spending totals while excluding identified transfers. |
| `compare_monthly_spending()` | Calculates monthly changes in spending, including dollar and percentage differences. |
| `plot_monthly_spending()` | Generates a bar chart of monthly spending totals. |
| `plot_category_spending()` | Generates a bar chart showing spending by category. |
| `export_uncategorized_transactions()` | Exports transactions that could not be automatically categorized for further review. |
| `generate_html_report()` | Combines summary statistics, charts, and tables into an HTML financial report. |
| `main()` | Coordinates the entire workflow, from loading the data to generating the final report. |

## Sample Data and Privacy

The program was originally designed to analyze real bank transaction data exported as a CSV file.

**The program can process real transaction data, but the version published on GitHub uses synthetic sample data to protect personal financial information.**

The sample dataset, `data/sample_transactions.csv`, contains fictional transactions created for demonstration purposes.

Importantly, **the sample dataset follows the same CSV structure as the original bank export**, including the same column names and data formats.

The dataset includes the following columns:

| Column | Description |
|---|---|
| `Details` | Transaction details |
| `Posting Date` | Date when the transaction was posted |
| `Description` | Transaction description |
| `Amount` | Transaction amount |
| `Type` | Transaction type |
| `Balance` | Account balance |
| `Check or Slip #` | Check or slip number, when applicable |

Because the sample data follows the same format as the original CSV file, the program can run the same analysis without requiring changes to its data-processing logic.

This approach allows the complete workflow to be demonstrated publicly without exposing actual banking activity or personal financial information.

The program is designed for CSV files that follow this structure. CSV exports from other banks may require adjustments to column names or transaction formatting.

## How to Run

### 1. Install Python Libraries

The program requires Python 3 and the following libraries:

- pandas
- matplotlib

Install the dependencies by running:

```bash
pip install -r requirements.txt
```

### 2. Prepare the Data

The repository includes a synthetic dataset:

```text
data/sample_transactions.csv
```

The program can also be used with real transaction data that follows the same CSV format.

### 3. Run the Program

From the project directory, execute:

```bash
python main.py
```

Make sure the CSV file path specified in `main.py` matches the dataset you want to analyze.

### 4. View the Results

After execution, the program generates:

| Output | Description |
|---|---|
| `reports/financial_report.html` | HTML financial report |
| `reports/monthly_comparison.csv` | Monthly spending comparison |
| `reports/uncategorized_transactions.csv` | Transactions requiring manual categorization |
| `figures/monthly_spending.png` | Monthly spending visualization |
| `figures/category_spending.png` | Category spending visualization |

## Example Financial Report

A demonstration report generated using the synthetic dataset is available through GitHub Pages:

[View the Personal Finance Report](https://takato-byu.github.io/personal_finance_analyzer/)

The report includes summary statistics, spending visualizations, category breakdowns, and month-to-month comparisons.

## Limitations

The program uses keyword-based rules for transaction categorization. As a result, some transactions may be incorrectly categorized or remain uncategorized.

The accuracy of the analysis depends on the quality and consistency of the input data. In addition, transactions classified as transfers are excluded from monthly spending calculations.

The project is intended for educational purposes and personal financial exploration rather than professional financial reporting.

## Project Information

**Course:** CS 111 — Introduction to Computer Science, Brigham Young University

**Project:** Free Coding Project

**Language:** Python

**Libraries:** pandas, matplotlib

**Data:** Synthetic bank transaction dataset for privacy protection
