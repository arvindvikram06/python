# Task 13: Automated Sales Report Generator

An end-to-end automation tool built in **Python** that fetches sales data from a database, processes it into metrics, generates visual charts, and compiles everything into a professional **PDF report**.

---

## Features

- **Database Integration**
  - Connects to **SQLite** to fetch monthly sales records.
  - Queries raw data including product details, units sold, and revenue per region.

- **Data Processing Service**
  - Aggregates raw records into key performance indicators (KPIs).
  - Calculates Total Revenue, Total Units Sold, and Average Order Value.
  - Performs region-wise performance analysis.

- **Data Visualization**
  - Uses **Matplotlib** to generate dynamic bar charts.
  - Automatically saves visualizations to a dedicated `charts/` directory.

- **PDF Report Generation**
  - Uses **ReportLab** to create structured PDF documents.
  - Includes headers, summary tables, embedded charts, and conditional warnings based on data analysis.

- **CLI Interface**
  - Simple command-line interface to trigger reports for specific months.

---

## Tech Stack

- **Python 3**
- **SQLite3**
- **Matplotlib** (for charting)
- **ReportLab** (for PDF generation)
- **Argparse** (for CLI)

---

## Project Workflow

1. **Input**: User provides a target month via CLI (e.g., `--month 2024-05`).
2. **Fetch**: `db.py` retrieves all sales entries for that month from the database.
3. **Process**: `service.py` calculates summary statistics and identifies performance trends.
4. **Visualize**: `charts.py` creates a bar chart comparing revenue across different regions.
5. **Compile**: `pdf.py` assembles the data and the chart into a formatted PDF file.
6. **Output**: The final report is saved in the `reports/` folder.

---

## Report Logic

- **Summary Table**: Displays high-level metrics at the top of the report.
- **Dynamic Charting**: Automatically adjusts scales based on monthly data.
- **Insights**: Detects specific trends, such as a decline in a particular region, and adds them to the report.

---

## Installation

```bash
pip install matplotlib reportlab
python generate_report.py --month 2024-01
```
