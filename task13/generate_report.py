import argparse
import os

from db import get_sales_data
from service import process_data
from charts import generate_bar_chart
from pdf import generate_pdf


def main():
    parser = argparse.ArgumentParser(description="Generate Monthly Sales Report") 
    parser.add_argument("--month", required=True, help="Format: YYYY-MM") # add argument for month

    args = parser.parse_args() # parse the arguments

    print("[1/4] Fetching data...")
    data = get_sales_data(args.month) # fetch raw data for the given month

    if not data:
        print("No data found for given month") #
        return

    print("[2/4] Processing data...")
    processed = process_data(data)# process the raw data to get summary metrics and region-wise data

    print("[3/4] Generating chart...")
    chart_path = generate_bar_chart(processed["region_data"]) # generate bar chart for revenue by region

    print("[4/4] Generating PDF...")

    os.makedirs("reports", exist_ok=True)
    output_path = f"reports/sales_report_{args.month}.pdf" 

    generate_pdf(
        data={
            "month": args.month,
            **processed
        },
        chart_path=chart_path,
        output_path=output_path
    ) # generate the PDF report with the processed data and chart

    print(f"✅ Report generated successfully: {output_path}")


if __name__ == "__main__":
    main()