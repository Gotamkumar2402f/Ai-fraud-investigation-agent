from fpdf import FPDF
from datetime import datetime
import re

def clean_text_for_pdf(text: str) -> str:
    """Remove emojis and unsupported characters."""
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # ASCII only
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = text.replace('`', '')
    text = text.replace('\t', '    ')
    return text

def create_pdf_report(transaction_id: str, report_text: str) -> bytes:
    """Create a clean PDF report."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 12, "AI Fraud Investigation Report", ln=True, align="C")
    
    # Date
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(6)
    
    # Transaction ID
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Transaction ID: {transaction_id}", ln=True)
    pdf.ln(4)
    
    # Body
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    
    clean_text = clean_text_for_pdf(report_text)
    
    # Use effective page width
    effective_width = pdf.w - pdf.l_margin - pdf.r_margin
    
    for line in clean_text.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
        
        # Break very long lines safely
        pdf.multi_cell(effective_width, 6, line)
    
    return bytes(pdf.output())