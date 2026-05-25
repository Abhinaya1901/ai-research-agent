# 🧬 AI Clinical Trial Intelligence Platform

🔗 **Live Demo:** [Click here to try the app](https://ai-research-agent-hnmtmjaansskxulryvnquf.streamlit.app)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-research-agent-hnmtmjaansskxulryvnquf.streamlit.app)

An autonomous multi-agent AI system that researches clinical trials, 
analyzes data, and generates professional PDF reports automatically.

## 🤖 How It Works

Three specialized AI agents work sequentially:
- **Trial Scout** — Searches live clinical trial data from clinicaltrials.gov
- **Data Analyst** — Extracts phases, drug candidates, and success rates
- **Medical Writer** — Generates a structured 7-section intelligence report

## ⚡ Features

- Real-time web search via Tavily API
- LLM-powered report generation using Groq (Llama 3.3 70B)
- Automated PDF generation and saving
- Multi-recipient email delivery with PDF attachment
- 24-hour auto-scheduling
- Interactive Streamlit dashboard with dark-mode UI

## 🛠️ Tech Stack

- **Framework:** CrewAI (Multi-Agent)
- **LLM:** Groq API (Llama 3.3 70B)
- **Search:** Tavily Search API
- **UI:** Streamlit
- **PDF:** FPDF2
- **Email:** smtplib (Gmail SMTP)
- **Language:** Python 3.12

## 🚀 Setup & Run

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git
cd ai-research-agent

### 2. Create virtual environment
conda create -n aiagent python=3.12 -y
conda activate aiagent

### 3. Install dependencies
pip install crewai crewai-tools streamlit python-dotenv langchain-groq tavily-python fpdf2 gspread schedule litellm

### 4. Add your API keys
Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=your_gmail@gmail.com
OPENAI_API_KEY=your_groq_key_here

### 5. Run the app
streamlit run app.py

## 📸 Demo

Enter any disease → AI agents activate → Full report generated → PDF emailed automatically

## 📄 Output Sample

The platform generates reports with these sections:
1. Executive Summary
2. Current Trial Landscape
3. Key Drug Candidates
4. Phase Analysis
5. Notable Findings
6. Recommendations
7. Conclusion