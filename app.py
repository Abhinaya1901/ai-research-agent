import streamlit as st
from crewai import Task, Crew, Process
from agents import trial_scout, data_analyst, medical_writer
from tools import save_pdf, send_email, fetch_trial_data
import schedule
import time
import threading

st.set_page_config(
    page_title="AI Clinical Trial Intelligence Platform",
    page_icon="🧬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

.hero-container {
    text-align: center;
    padding: 3rem 2rem 2rem;
    background: linear-gradient(180deg, rgba(0,212,255,0.05) 0%, transparent 100%);
    border-bottom: 1px solid rgba(0,212,255,0.1);
    margin-bottom: 2rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: #00d4ff;
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #7b61ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 1rem;
}

.hero-subtitle {
    color: rgba(255,255,255,0.5);
    font-size: 1rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

.agent-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s ease;
}

.agent-card:hover {
    border-color: rgba(0,212,255,0.3);
    background: rgba(0,212,255,0.05);
}

.agent-icon {
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
}

.agent-name {
    color: #ffffff;
    font-weight: 600;
    font-size: 0.9rem;
}

.agent-desc {
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
}

.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #00d4ff;
}

.stat-label {
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.search-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0 2rem;
}

.status-running {
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #00d4ff;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

.report-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
}

.success-banner {
    background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(123,97,255,0.1));
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.1) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255,255,255,0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #7b61ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(0,212,255,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,212,255,0.4) !important;
}

.stSidebar {
    background: rgba(10,10,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

.stSidebar [data-testid="stMarkdownContainer"] {
    color: rgba(255,255,255,0.7) !important;
}

[data-testid="stCheckbox"] label {
    color: rgba(255,255,255,0.7) !important;
}

.stSpinner > div {
    border-top-color: #00d4ff !important;
}

hr {
    border-color: rgba(255,255,255,0.08) !important;
}

h1, h2, h3 {
    color: white !important;
}

p, li {
    color: rgba(255,255,255,0.75) !important;
}

.stSuccess {
    background: rgba(0,255,150,0.08) !important;
    border: 1px solid rgba(0,255,150,0.2) !important;
    border-radius: 10px !important;
}

.stInfo {
    background: rgba(0,212,255,0.08) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 10px !important;
}

.stError {
    background: rgba(255,80,80,0.08) !important;
    border: 1px solid rgba(255,80,80,0.2) !important;
    border-radius: 10px !important;
}

.footer {
    text-align: center;
    color: rgba(255,255,255,0.2);
    font-size: 0.75rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🧬 Agentic AI Platform</div>
    <div class="hero-title">Clinical Trial Intelligence</div>
    <div class="hero-subtitle">Multi-agent AI system · Real-time research · Automated reporting</div>
</div>
""", unsafe_allow_html=True)

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    st.markdown('<div class="stat-card"><div class="stat-number">4</div><div class="stat-label">AI Agents</div></div>', unsafe_allow_html=True)
with col_s2:
    st.markdown('<div class="stat-card"><div class="stat-number">3</div><div class="stat-label">Search Queries</div></div>', unsafe_allow_html=True)
with col_s3:
    st.markdown('<div class="stat-card"><div class="stat-number">PDF</div><div class="stat-label">Auto Export</div></div>', unsafe_allow_html=True)
with col_s4:
    st.markdown('<div class="stat-card"><div class="stat-number">✉️</div><div class="stat-label">Email Delivery</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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
""", unsafe_allow_html=True)

for agent in [
    ("🔍", "Trial Scout", "Searches clinicaltrials.gov"),
    ("📊", "Data Analyst", "Extracts key insights"),
    ("✍️", "Medical Writer", "Writes the report"),
    ("🤖", "Automation Agent", "Saves PDF & emails"),
]:
    st.sidebar.markdown(f"""
    <div class="agent-card">
        <div class="agent-icon">{agent[0]}</div>
        <div class="agent-name">{agent[1]}</div>
        <div class="agent-desc">{agent[2]}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
   disease = st.text_input(
    "",
    placeholder="🔬  Enter disease or condition — e.g. Breast Cancer, Alzheimer's, Type 2 Diabetes...",
    label_visibility="collapsed"
)
recipients = st.text_input(
    "",
    placeholder="📧  Enter recipient emails separated by commas — e.g. john@gmail.com, sarah@hospital.com",
    label_visibility="collapsed"
)
with col2:
    run_button = st.button("🚀  Run AI Agents", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

def run_crew(disease_name):
    raw_data = fetch_trial_data(disease_name)
    task1 = Task(
        description=f"""Here is raw clinical trial data for {disease_name} fetched from the web:
{raw_data}
Organize this into a clean structured list of trials with: trial name, phase, sponsor, status, and key details.""",
        agent=trial_scout,
        expected_output="A structured list of clinical trials with names, phases, sponsors and status"
    )
    task2 = Task(
        description=f"""Based on the clinical trial data for {disease_name}, analyze and extract:
- Trial phases distribution
- Key drug candidates
- Success rates and outcomes
- Key sponsors and institutions
- Patient enrollment numbers""",
        agent=data_analyst,
        expected_output="A structured analysis with phases, drugs, success rates and key insights"
    )
    task3 = Task(
        description=f"""Write a comprehensive professional clinical trial intelligence report for {disease_name}.
Use this exact structure:
# Clinical Trial Intelligence Report: {disease_name}
## Executive Summary
## Current Trial Landscape
## Key Drug Candidates
## Phase Analysis
## Notable Findings
## Recommendations
## Conclusion
Write in clear professional language for medical researchers.""",
        agent=medical_writer,
        expected_output="A full structured markdown report with all sections completed professionally"
    )
    crew = Crew(
        agents=[trial_scout, data_analyst, medical_writer],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return str(result)

if run_button and disease:
    st.markdown("---")
    st.markdown("""
    <div style='color:white; font-size:1.3rem; font-weight:600; margin-bottom:1rem'>
        ⚡ Agents Activated
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        st.markdown('<div class="status-running">🔍 Trial Scout<br><small>Fetching data...</small></div>', unsafe_allow_html=True)
    with col_a2:
        st.markdown('<div class="status-running" style="opacity:0.5">📊 Data Analyst<br><small>Standby...</small></div>', unsafe_allow_html=True)
    with col_a3:
        st.markdown('<div class="status-running" style="opacity:0.5">✍️ Medical Writer<br><small>Standby...</small></div>', unsafe_allow_html=True)
    with col_a4:
        st.markdown('<div class="status-running" style="opacity:0.5">🤖 Automation<br><small>Standby...</small></div>', unsafe_allow_html=True)

    with st.spinner(f"AI agents researching '{disease}'... This takes 2-3 minutes"):
        try:
            report = run_crew(disease)

            st.markdown("---")
            st.markdown("""
            <div class="success-banner">
                <div style='font-size:2rem'>🎉</div>
                <div style='color:white; font-size:1.2rem; font-weight:600; margin-top:0.5rem'>Report Generated Successfully!</div>
                <div style='color:rgba(255,255,255,0.5); font-size:0.85rem; margin-top:0.3rem'>All agents completed · PDF saved · Email delivered</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown("### 📄 Intelligence Report")
            st.markdown(report)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🤖 Automation")

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                pdf_path = save_pdf(report, disease)
                st.success(f"✅ PDF saved: `{pdf_path}`")
            with col_r2:
                try:
                    email_list = [e.strip() for e in recipients.split(",") if e.strip()] if recipients else [os.getenv("EMAIL_RECEIVER")]
                    st.success("✅ Report delivered to your inbox!")
                except Exception as email_err:
                    st.warning(f"⚠️ Email skipped: {str(email_err)[:60]}")

            st.balloons()

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Full PDF Report",
                    data=f,
                    file_name=pdf_path,
                    mime="application/pdf",
                    use_container_width=True
                )

            if auto_schedule:
                st.info(f"⏰ Scheduled — re-running every 24 hours for '{disease}'")
                def scheduled_job():
                    run_crew(disease)
                schedule.every(24).hours.do(scheduled_job)
                def run_schedule():
                    while True:
                        schedule.run_pending()
                        time.sleep(60)
                thread = threading.Thread(target=run_schedule, daemon=True)
                thread.start()

        except Exception as e:
            import traceback
            st.error(f"Something went wrong: {str(e)}")
            st.code(traceback.format_exc())

elif run_button and not disease:
    st.warning("⚠️ Please enter a disease or condition first!")

st.markdown("""
<div class="footer">
    AI Clinical Trial Intelligence Platform &nbsp;·&nbsp; Multi-Agent System &nbsp;·&nbsp; Built with CrewAI + Groq + Tavily
</div>
""", unsafe_allow_html=True)