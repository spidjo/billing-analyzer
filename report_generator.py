from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import pandas as pd
from datetime import datetime

def generate_pdf_report(anomalies: pd.DataFrame, stats: dict, output_file='anomaly_report.pdf'):
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("📊 Billing Anomaly Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Summary Stats
    elements.append(Paragraph("📌 Summary Statistics", styles['Heading2']))
    summary_data = [
        ["Mean Cost", f"{stats['mean']:.2f}"],
        ["Standard Deviation", f"{stats['std']:.2f}"],
        ["Total Anomalies", str(stats['outlier_count'])]
    ]
    summary_table = Table(summary_data, hAlign='LEFT')
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    # Anomalies Table
    elements.append(Paragraph("🚨 Anomalous Records", styles['Heading2']))

    # Limit to 10 rows for readability
    display_df = anomalies.head(10).copy()
    display_df = display_df.fillna("").astype(str)
    table_data = [display_df.columns.tolist()] + display_df.values.tolist()

    anomaly_table = Table(table_data, repeatRows=1)
    anomaly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(anomaly_table)
    elements.append(Spacer(1, 12))

    # Footer
    elements.append(Paragraph(f"📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    
    doc.build(elements)
    return output_file
