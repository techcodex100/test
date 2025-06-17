from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = FastAPI()

@app.get("/generate-pdf")
async def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>SELLER INVOICE</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Table Data (as per your image)
    data = [
        ["EXPORTER", "NOTIFY PARTY"],
        ["SHRADDHA IMPEX", "SAME AS CONSIGNEE"],
        ["308, THIRD FLOOR, FORTUNE BUSINESS CENTER,", ""],
        ["165 R.N.T. MARG, INDORE-452001, M.P., INDIA", ""],
        ["Invoice No. & Date:", "SI 19/21-22  Dated  24.05.2021"],
        ["I.E. Code No.:", "1103004999"],
        ["Buyer's Order No. & Date:", "SI/SG/02/21-22  23.04.2021"],
        ["Country Of Origin:", "INDIA"],
        ["CONSIGNEE", "Country Of Final Destination:"],
        ["ALLIANCE DIVINE IMPEX PTE LTD", "SINGAPORE"],
        ["No 160 Kallang Way #01-02, Singapore 349246", ""],
        ["VESSEL / VOYAGE:", "Port of Loading: NHAVA SHEVA"],
        ["TERMS OF DELIVERY:", "CIF (INCO TERMS 2010)"],
        ["Pre-carriage By:", "----------------------"],
        ["Place of Receipt:", "----------------------"],
        ["Port of Discharge:", "SINGAPORE"],
        ["FINAL DESTINATION:", "SINGAPORE"],
        ["Terms of Payment:", "10% Advance and balance on scan copy of documents"],
    ]

    # Table Style
    table = Table(data, colWidths=[270, 270])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 18))

    # Product Table
    product_data = [
        ["Sr No & Marks", "Description of Goods", "NO. OF UNITS", "RATE PER UNIT (USD)", "Amount (USD)"],
        ["05 X 20' FCL", "2700 BAGS INDIAN WHITE CANE SUGAR S30\nICUMSA LESS THAN 100\nHS CODE: 17019910\nPACKED IN 50 KG PP BAGS\nTOTAL NET WEIGHT: 135.00 MTS\nTOTAL GROSS WEIGHT: 135.430 MTS", "135,000", "470.00", "63,450.00"],
        ["", "", "", "TOTAL AMOUNT", "63,450.00"]
    ]
    product_table = Table(product_data, colWidths=[80, 220, 70, 80, 90])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (0,2), (3,2)),  # Merge TOTAL AMOUNT row
        ('ALIGN', (3,2), (4,2), 'RIGHT'),
        ('FONTNAME', (3,2), (4,2), 'Helvetica-Bold'),
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 18))

    # Extra fields (as per your image)
    extra_data = [
        ["BIN No.:", ""],
        ["Drawback Sr. No.:", ""],
        ["Shipment under MAEQ scheme", ""]
    ]
    extra_table = Table(extra_data, colWidths=[150, 390])
    extra_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(extra_table)

    doc.build(elements)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=invoice.pdf"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 