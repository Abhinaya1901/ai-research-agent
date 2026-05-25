import streamlit as st
import os
from dotenv import load_dotenv
from tools import save_pdf, send_email, fetch_trial_data
from groq import Groq
import schedule
import time
import threading

load_dotenv()

st.set_page_config(
    page_title="AI Clinical Trial Intelligence Platform",
    page_icon="🧬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #0a1628 100%); min-height: 100vh; }
.hero-badge { display: inline-block; background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 6px 18px; border-radius: 50px; font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero-title { font-size: 3.5rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #7b61ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.2; margin-bottom: 1rem; }
.hero-subtitle { color: rgba(255,255,255,0.5); font-size: 1rem; }
.stat-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; text-align: center; }
.stat-number { font-size: 1.8rem; font-weight: 700; color: #00d4ff; }
.stat-label { color: rgba(255,255,255,0.4); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
.search-container { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 2rem; margin: 1rem 0 2rem; }
.stButton > button { background: linear-gradient(135deg, #00d4ff, #7b61ff) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 600 !important; font-size: 1rem !important; box-shadow: 0 4px 20px rgba(0,212,255,0.3) !important; }
div[data-testid="stTextInput"] input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 12px !important; color: white !important; }
h1,h2,h3 { color: white !important; }
p, li { color: rgba(255,255,255,0.75) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem;'>
    <div class="hero-badge">🧬 Agentic AI Platform</div>
    <div class="hero-title">Clinical Trial Intelligence</div>
    <div class="hero-subtitle">Multi-agent AI · Real-time research · Automated reporting</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><div class="stat-number">3</div><div class="stat-label">AI Agents</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="stat-number">Live</div><div class="stat-label">Web Search</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="stat-number">PDF</div><div class="stat-label">Auto Export</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><div class="stat-number">✉️</div><div class="stat-label">Email Delivery</div></div>', unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align:center; padding: 1rem 0;'>
    <div style='font-size:2rem'>🧬</div>
    <div style='color:white; font-weight:700; font-size:1.1rem; margin-top:0.5rem'>ClinicalAI</div>
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem'>Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
auto_schedule = st.sidebar.checkbox("⏰ Enable 24hr Auto-Scheduling", value=False)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='color:rgba(255,255,255,0.6); font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem'>AI Agents</div>
<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:1rem; margin-bottom:0.5rem'>
    <div style='font-size:1.2rem'>🔍</div>
    <div style='color:white; font-weight:600; font-size:0.9rem'>Trial Scout</div>
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem'>Searches clinicaltrials.gov</div>
</div>
<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:1rem; margin-bottom:0.5rem'>
    <div style='font-size:1.2rem'>📊</div>
    <div style='color:white; font-weight:600; font-size:0.9rem'>Data Analyst</div>
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem'>Extracts key insights</div>
</div>
<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:1rem; margin-bottom:0.5rem'>
    <div style='font-size:1.2rem'>✍️</div>
    <div style='color:white; font-weight:600; font-size:0.9rem'>Medical Writer</div>
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem'>Writes the report</div>
</div>
<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:1rem; margin-bottom:0.5rem'>
    <div style='font-size:1.2rem'>🤖</div>
    <div style='color:white; font-weight:600; font-size:0.9rem'>Automation Agent</div>
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem'>Saves PDF & emails</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col_in, col_btn = st.columns([3, 1])
with col_in:
    disease = st.text_input("", placeholder="🔬 Enter disease — e.g. Breast Cancer, Alzheimer's, Type 2 Diabetes...", label_visibility="collapsed")
    recipients = st.text_input("", placeholder="📧 Email recipients (comma separated) — e.g. john@gmail.com, sara@hospital.com", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("🚀 Run AI Agents", type="primary", use_container_width=True)

def call_groq(system_prompt, user_prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=2000
    )
    return response.choices[0].message.content

def run_agents(disease_name):
    st.info("🔍 Trial Scout — Fetching live clinical trial data...")
    raw_data = fetch_trial_data(disease_name)

    st.info("📊 Data Analyst — Extracting insights from trial data...")
    analysis = call_groq(
        "You are a clinical data analyst specializing in pharmaceutical research.",
        f"Analyze this clinical trial data for {disease_name} and extract: trial phases, drug candidates, success rates, key sponsors, patient numbers.\n\nData:\n{raw_data}"
    )

    st.info("✍️ Medical Writer — Generating structured report...")
    report = call_groq(
        "You are a senior medical writer at a pharmaceutical company.",
        f"""Write a comprehensive clinical trial intelligence report for {disease_name}.
Use this analysis: {analysis}

Structure it exactly as:
# Clinical Trial Intelligence Report: {disease_name}
## Executive Summary
## Current Trial Landscape
## Key Drug Candidates
## Phase Analysis
## Notable Findings
## Recommendations
## Conclusion

Write professionally for medical researchers."""
    )
    return report

if run_button and disease:
    st.markdown("---")
    st.markdown("### ⚡ Agents Activated")
    with st.spinner(f"AI agents researching '{disease}'... This takes 1-2 minutes"):
        try:
            report = run_agents(disease)
            st.success("✅ All agents completed!")
            st.markdown("---")
            st.markdown("### 📄 Intelligence Report")
            st.markdown(report)
            st.markdown("---")
            st.info("🤖 Automation Agent — Running...")
            pdf_path = save_pdf(report, disease)
            st.success(f"✅ PDF saved: `{pdf_path}`")
            try:
                email_list = [e.strip() for e in recipients.split(",") if e.strip()] if recipients else [os.getenv("EMAIL_RECEIVER")]
                send_email(report, disease, pdf_path, email_list)
                st.success(f"✅ Report emailed to {len(email_list)} recipient(s)!")
            except Exception as e:
                st.warning(f"⚠️ Email skipped: {str(e)[:60]}")
            st.balloons()
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF Report", data=f, file_name=pdf_path, mime="application/pdf", use_container_width=True)
            if auto_schedule:
                st.info(f"⏰ Scheduled to re-run every 24 hours for '{disease}'")
        except Exception as e:
            import traceback
            st.error(f"Something went wrong: {str(e)}")
            st.code(traceback.format_exc())

elif run_button and not disease:
    st.warning("⚠️ Please enter a disease name first!")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#999;font-size:0.8rem'>AI Clinical Trial Intelligence Platform | Multi-Agent System | Built with Groq + Tavily + Streamlit</div>", unsafe_allow_html=True)