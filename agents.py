from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

trial_scout = Agent(
    role="Clinical Trial Scout",
    goal="Summarize and organize clinical trial information provided to you",
    backstory="""You are an expert medical researcher specializing in clinical trials 
    at top pharmaceutical companies. You organize and summarize trial data clearly.""",
    llm=llm,
    verbose=True
)

data_analyst = Agent(
    role="Clinical Data Analyst",
    goal="Analyze clinical trial data and extract key insights about phases, drugs, and success rates",
    backstory="""You are a biostatistician with deep expertise in interpreting 
    clinical trial results, extracting meaningful patterns from complex medical data.""",
    llm=llm,
    verbose=True
)

medical_writer = Agent(
    role="Medical Writer",
    goal="Write a clear structured professional report about clinical trials",
    backstory="""You are a senior medical writer who translates complex clinical 
    trial data into clear actionable reports for medical researchers.""",
    llm=llm,
    verbose=True
)