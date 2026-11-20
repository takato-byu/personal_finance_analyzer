
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Load Transaction Data
# --------------------------------------------------

def load_transactions(file_path):
    """
    Load bank transaction data from a CSV file.

    Args:
        file_path: The path to the transaction CSV file.

    Returns:
        A DataFrame containing the transaction data.
    """
    return pd.read_csv(file_path)


# --------------------------------------------------
# 2. Clean Transaction Data
# --------------------------------------------------

def clean_transactions(df):
    """
    Clean and prepare transaction data for analysis.

    Args:
        df: The original transaction DataFrame.

    Returns:
        A cleaned DataFrame with additional analysis columns.
    """
    df = df.copy()

    # Convert dates to datetime
    df["Posting Date"] = pd.to_datetime(
        df["Posting Date"],
        format="%m/%d/%Y",
        errors="coerce"
    )

    # Convert amounts to numeric values
    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    # Clean transaction descriptions
    df["Description"] = (
        df["Description"]
        .fillna("")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Remove invalid transactions
    df = df.dropna(
        subset=["Posting Date", "Amount"]
    )

    # Create month column
    df["Month"] = (
        df["Posting Date"].dt.strftime("%Y-%m")
    )

    # Identify transaction direction
    df["Transaction Type"] = df["Amount"].apply(
        lambda amount: (
            "Expense" if amount < 0 else "Inflow"
        )
    )

    # Convert outgoing amounts to positive values
    df["Expense"] = df["Amount"].apply(
        lambda amount: abs(amount) if amount < 0 else 0
    )

    return df


# --------------------------------------------------
# 3. Categorize Transactions
# --------------------------------------------------

def categorize_transaction(description):
    """
    Categorize a transaction using merchant keywords.

    Args:
        description: The description of a bank transaction.

    Returns:
        The assigned transaction category.
    """
    categories = {
        "Cafe": [
            "STARBUCKS",
            "DUTCH BROS",
            "JAVA JUNKIE",
            "LIBRARY CAFE",
            "MOON PEAK COFFEE"
        ],

        "Groceries": [
            "TRADER JOE",
            "WALMART",
            "COSTCO",
            "SMITHS",
            "ASIAN MARKET"
        ],

        "Dining": [
            "TOUS LES JOURS",
            "MCDONALD",
            "CHIPOTLE",
            "RESTAURANT",
            "RESTAURAN",
            "COSTA VIDA",
            "COUGAR EXPRESS",
            "FIRST WATCH",
            "TWO JACKS PIZZA",
            "PARLOR DOUGHNUTS",
            "JAPANESE KITCH",
            "WENDYS",
            "VEGAN SUN"
        ],

        "Transportation": [
            "UBER",
            "LYFT",
            "GAS STATION"
        ],

        "Shopping": [
            "AMAZON",
            "TARGET"
        ],

        "Subscriptions": [
            "OPENAI",
            "CHATGPT",
            "NETFLIX",
            "SPOTIFY",
            "SUIKA VPN",
            "64PERSONALITY",
            "ASKDOCTORS TRIAL"
        ],

        "Housing": [
            "BRITTANYSTUDENTREN",
            "APARTMENT",
            "RENT"
        ],

        "Bank Fees": [
            "FOREIGN EXCHANGE RATE ADJUSTMENT FEE",
            "SERVICE FEE"
        ],

        "Transfer": [
            "TRANSFER",
            "ZELLE"
        ]
    }

    description = str(description).upper()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Uncategorized"


# --------------------------------------------------
# 4. Analyze Spending by Category
# --------------------------------------------------

def analyze_category_spending(df):
    """
    Calculate total outgoing amounts by category.

    Args:
        df: The cleaned and categorized transaction DataFrame.

    Returns:
        A Series containing total outflows by category.
    """
    expenses = df[
        df["Transaction Type"] == "Expense"
    ]

    category_spending = (
        expenses.groupby("Category")["Expense"]
        .sum()
        .sort_values(ascending=False)
    )

    return category_spending


# --------------------------------------------------
# 5. Analyze Monthly Spending
# --------------------------------------------------

def analyze_monthly_spending(df):
    """
    Calculate monthly spending excluding identified transfers.

    Args:
        df: The cleaned and categorized transaction DataFrame.

    Returns:
        A Series containing monthly spending totals.
    """
    expenses = df[
        (df["Transaction Type"] == "Expense") &
        (df["Category"] != "Transfer")
    ]

    monthly_spending = (
        expenses.groupby("Month")["Expense"]
        .sum()
        .sort_index()
    )

    return monthly_spending


# --------------------------------------------------
# 6. Compare Monthly Spending
# --------------------------------------------------

def compare_monthly_spending(monthly_spending):
    """
    Calculate monthly spending changes in dollars and percentages.

    Args:
        monthly_spending: A Series of monthly spending totals.

    Returns:
        A DataFrame containing monthly spending comparisons.
    """
    comparison = monthly_spending.to_frame(
        name="Total Spending"
    )

    comparison["Dollar Change"] = (
        comparison["Total Spending"].diff()
    )

    comparison["Percent Change"] = (
        comparison["Total Spending"].pct_change(
            fill_method=None
        ) * 100
    )

    return comparison


# --------------------------------------------------
# 7. Create Monthly Spending Chart
# --------------------------------------------------

def plot_monthly_spending(monthly_spending):
    """
    Create and save a monthly spending bar chart.

    Args:
        monthly_spending: A Series of monthly spending totals.

    Returns:
        The path to the saved chart image.
    """
    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "monthly_spending.png"

    plt.figure(figsize=(12, 6))

    monthly_spending.plot(
        kind="bar",
        color="steelblue"
    )

    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Total Spending ($)")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(output_file, dpi=300)
    plt.close()

    return output_file


# --------------------------------------------------
# 8. Create Category Spending Chart
# --------------------------------------------------

def plot_category_spending(category_spending):
    """
    Create and save a category spending bar chart.

    Args:
        category_spending: A Series of total outflows by category.

    Returns:
        The path to the saved chart image.
    """
    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "category_spending.png"

    # Exclude transfers
    spending = category_spending.drop(
        labels=["Transfer"],
        errors="ignore"
    )

    plt.figure(figsize=(10, 6))

    spending.sort_values().plot(
        kind="barh",
        color="seagreen"
    )

    plt.title("Spending by Category")
    plt.xlabel("Total Spending ($)")
    plt.ylabel("Category")

    plt.tight_layout()

    plt.savefig(output_file, dpi=300)
    plt.close()

    return output_file


# --------------------------------------------------
# 9. Export Uncategorized Transactions
# --------------------------------------------------

def export_uncategorized_transactions(df):
    """
    Export uncategorized outgoing transactions to a CSV file.

    Args:
        df: The cleaned and categorized transaction DataFrame.

    Returns:
        The path to the exported CSV file.
    """
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    output_file = (
        output_dir / "uncategorized_transactions.csv"
    )

    uncategorized = df[
        (df["Transaction Type"] == "Expense") &
        (df["Category"] == "Uncategorized")
    ]

    uncategorized[
        ["Posting Date", "Description", "Amount"]
    ].to_csv(output_file, index=False)

    return output_file


# --------------------------------------------------
# 10. Generate HTML Financial Report
# --------------------------------------------------

def generate_html_report(
    monthly_spending,
    comparison,
    category_spending,
    df
):
    """
    Generate an HTML report with financial statistics and charts.

    Args:
        monthly_spending: A Series of monthly spending totals.
        comparison: A DataFrame of monthly spending changes.
        category_spending: A Series of category outflow totals.
        df: The cleaned and categorized transaction DataFrame.

    Returns:
        The path to the generated HTML report.
    """
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    report_file = output_dir / "financial_report.html"

    total_transactions = len(df)

    average_spending = monthly_spending.mean()

    highest_month = monthly_spending.idxmax()
    highest_amount = monthly_spending.max()

    # Calculate category spending percentages
    spending_only = category_spending.drop(
        labels=["Transfer"],
        errors="ignore"
    )

    category_summary = spending_only.to_frame(
        name="Total Spending"
    )

    total_spending = category_summary[
        "Total Spending"
    ].sum()

    category_summary["Percentage"] = (
        category_summary["Total Spending"]
        / total_spending
        * 100
    )

    # Create HTML tables with corrected headers
    comparison_html = (
        comparison
        .rename_axis("Month")
        .reset_index()
        .round(2)
        .to_html(
            index=False,
            classes="data-table",
            border=0,
            na_rep="—"
        )
    )

    category_html = (
        category_summary
        .rename_axis("Category")
        .reset_index()
        .round(2)
        .to_html(
            index=False,
            classes="data-table",
            border=0
        )
    )

    # Generate HTML document
    html = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Personal Finance Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                margin: 40px;
                color: #333;
            }}

            .container {{
                max-width: 1100px;
                margin: auto;
                background: white;
                padding: 35px;
                border-radius: 12px;
            }}

            h1 {{
                color: #1f3a5f;
            }}

            h2 {{
                margin-top: 35px;
                color: #1f3a5f;
            }}

            .summary {{
                display: flex;
                gap: 20px;
                margin: 25px 0;
            }}

            .card {{
                flex: 1;
                background: #eef3f8;
                padding: 20px;
                border-radius: 8px;
            }}

            .card h3 {{
                font-size: 14px;
            }}

            .card h2 {{
                margin: 5px 0;
            }}

            .data-table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 15px;
            }}

            .data-table th,
            .data-table td {{
                border-bottom: 1px solid #ddd;
                padding: 10px;
                text-align: right;
            }}

            .data-table th {{
                background-color: #eef3f8;
            }}

            img {{
                width: 100%;
                margin-top: 20px;
            }}

            .note {{
                margin-top: 30px;
                color: #666;
                font-size: 13px;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Personal Finance Report</h1>

            <p>
                Generated on:
                {datetime.now().strftime("%Y-%m-%d %H:%M")}
            </p>

            <div class="summary">

                <div class="card">
                    <h3>Total Transactions</h3>
                    <h2>{total_transactions}</h2>
                </div>

                <div class="card">
                    <h3>Average Monthly Spending</h3>
                    <h2>${average_spending:,.2f}</h2>
                </div>

                <div class="card">
                    <h3>Highest Spending Month</h3>
                    <h2>{highest_month}</h2>
                    <p>${highest_amount:,.2f}</p>
                </div>

            </div>

            <h2>Monthly Spending</h2>

            <img
                src="../figures/monthly_spending.png"
                alt="Monthly Spending Chart"
            >

            <h2>Spending by Category</h2>

            <img
                src="../figures/category_spending.png"
                alt="Category Spending Chart"
            >

            <h2>Category Spending Summary</h2>

            {category_html}

            <h2>Monthly Spending Comparison</h2>

            {comparison_html}

            <p class="note">
                Note: Spending totals are estimates based on
                current transaction categorization rules.
                Identified transfers are excluded from monthly
                spending. The first and last months may be
                incomplete.
            </p>

        </div>
    </body>
    </html>
    """

    report_file.write_text(
        html,
        encoding="utf-8"
    )

    return report_file


# --------------------------------------------------
# 11. Main Program
# --------------------------------------------------

def main():
    """
    Run the personal finance analysis program.

    Args:
        None.

    Returns:
        None.
    """
    print("Personal Finance Analyzer")
    print("-------------------------")

    file_path = Path("data/sample_transactions.csv")

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return

    # Load data
    transactions = load_transactions(file_path)

    print(f"\nOriginal transactions: {len(transactions)}")

    # Clean data
    cleaned = clean_transactions(transactions)

    print(f"Cleaned transactions: {len(cleaned)}")

    if cleaned.empty:
        print("Error: No valid transactions found.")
        return

    # Categorize transactions
    cleaned["Category"] = (
        cleaned["Description"].apply(
            categorize_transaction
        )
    )

    print("\nTransaction Categories:")
    print(cleaned["Category"].value_counts())

    # Analyze spending by category
    category_spending = analyze_category_spending(
        cleaned
    )

    print("\nTotal Outflows by Category:")
    print(category_spending.round(2))

    # Analyze monthly spending
    monthly_spending = analyze_monthly_spending(
        cleaned
    )

    if monthly_spending.empty:
        print("No outgoing transactions found.")
        return

    print("\nMonthly Spending Summary:")
    print(monthly_spending.round(2))

    print("\nAverage Monthly Spending:")
    print(f"${monthly_spending.mean():,.2f}")

    print("\nHighest Spending Month:")
    print(monthly_spending.idxmax())
    print(f"${monthly_spending.max():,.2f}")

    # Compare monthly spending
    comparison = compare_monthly_spending(
        monthly_spending
    )

    print("\nMonthly Spending Comparison:")
    print(comparison.round(2))

    # Generate charts
    monthly_chart = plot_monthly_spending(
        monthly_spending
    )

    category_chart = plot_category_spending(
        category_spending
    )

    print(f"\nMonthly chart saved to: {monthly_chart}")
    print(f"Category chart saved to: {category_chart}")

    # Export uncategorized transactions
    uncategorized_file = (
        export_uncategorized_transactions(cleaned)
    )

    print(
        f"\nUncategorized transactions saved to: "
        f"{uncategorized_file}"
    )

    # Save monthly comparison
    comparison_file = Path(
        "reports/monthly_comparison.csv"
    )

    comparison.to_csv(comparison_file)

    print(
        f"Monthly comparison saved to: "
        f"{comparison_file}"
    )

    # Generate HTML report
    report_file = generate_html_report(
        monthly_spending,
        comparison,
        category_spending,
        cleaned
    )

    print(f"\nHTML report saved to: {report_file}")

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
