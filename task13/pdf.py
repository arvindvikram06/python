from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, chart_path, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph(f"Monthly Sales Report - {data['month']}", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Summary Table
    summary_data = [
        ["Metric", "Value"],
        ["Total Revenue", f"${data['total_revenue']}"],
        ["Units Sold", str(data['total_units'])],
        ["Avg Order Value", f"${data['avg_order_value']}"],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Chart Image
    elements.append(Paragraph("Revenue by Region", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(Image(chart_path, width=400, height=200))
    elements.append(Spacer(1, 20))

    # Conditional Warning
    if data.get("west_decline"):
        elements.append(Paragraph(
            f"West region declined {data['west_decline']}% MoM",
            styles["Normal"]
        ))

    doc.build(elements)