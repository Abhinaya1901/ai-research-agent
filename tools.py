from tavily import TavilyClient
import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetch_trial_data(disease: str) -> str:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    queries = [
        f"{disease} clinical trials clinicaltrials.gov phases",
        f"{disease} drug candidates trial results",
    ]
    output = ""
    for query in queries:
        results = client.search(query=query, search_depth="basic", max_results=2)
        for r in results["results"]:
            content = r['content'][:400]
            output += f"Title: {r['title']}\nContent: {content}\n\n"
    return output[:3000]

def save_pdf(report_text: str, disease: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Clinical Trial Report: {disease}", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    for line in report_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            if line.startswith("##"):
                pdf.set_font("Arial", "B", 13)
                pdf.multi_cell(0, 8, line.replace("##", "").strip())
                pdf.set_font("Arial", size=11)
            elif line.startswith("#"):
                pdf.set_font("Arial", "B", 15)
                pdf.multi_cell(0, 10, line.replace("#", "").strip())
                pdf.set_font("Arial", size=11)
            else:
                pdf.multi_cell(0, 7, line.encode('latin-1', 'replace').decode('latin-1'))
        except Exception:
            continue
    filename = f"clinical_trial_report_{disease.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    return filename

def send_email(report_text: str, disease: str, pdf_path: str, receivers: list = None):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not receivers:
        receivers = [os.getenv("EMAIL_RECEIVER")]
    
    for receiver in receivers:
        receiver = receiver.strip()
        if not receiver:
            continue
            
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = f"Clinical Trial Report: {disease} — {datetime.now().strftime('%Y-%m-%d')}"
        
        body = f"""Hello,

Your automated Clinical Trial Intelligence Report for "{disease}" is ready.

SUMMARY:
{report_text[:500]}...

Full report is attached as PDF.

Regards,
AI Research Agent"""
        msg.attach(MIMEText(body, "plain"))
        
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf_path}")
            msg.attach(part)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
    
    return f"Email sent to {len(receivers)} recipient(s)!"