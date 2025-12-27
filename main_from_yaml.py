import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS
import streamlit as st

# ✅ 1. ENVIRONMENT GUARDS
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

load_dotenv()

# ✅ 2. SEARCH TOOL
@tool("internet_search")
def internet_search(query: str) -> str:
    """Useful for searching the internet about a given topic."""
    results = DDGS().text(query, max_results=5)
    return "\n".join([
        f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}\n"
        for r in results
    ])

# ✅ 3. STABLE GEMINI MODEL (NO PREFIX, NO 404)
gemini_llm = LLM(
    model="gemini-pro",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ✅ 4. LOAD CONFIGS
with open('config/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

# ✅ 5. DEFINE AGENTS
researcher = Agent(
    config=agents_config['researcher'],
    llm=gemini_llm,
    tools=[internet_search],
    verbose=True,
    allow_delegation=False
)

strategist = Agent(
    role="Senior Industrial Strategist",
    goal="Refine research into actionable business insights",
    backstory="Expert at turning raw data into high-value strategy reports for the C-Suite.",
    llm=gemini_llm,
    verbose=True
)

# ✅ 6. DEFINE TASKS
research_task = Task(
    config=tasks_config['research_task'],
    agent=researcher
)

analysis_task = Task(
    description="Analyze the research findings on {topic} and create a 5-point strategic summary for industrial stakeholders.",
    expected_output="A high-level executive summary and actionable insights.",
    agent=strategist
)

# ✅ 7. CREW IGNITION
my_crew = Crew(
    agents=[researcher, strategist],
    tasks=[research_task, analysis_task],
    verbose=True
)

# ✅ 8. STREAMLIT UI
st.set_page_config(page_title="Global Agent Assembly Line", layout="centered")
st.title("🌐 Global Agent Assembly Line")
st.subheader("Autonomous Industrial Research & Strategy")

topic = st.text_input("🔍 Enter your research topic")

if st.button("🚀 Launch Autonomous Mission"):
    with st.spinner("Agents assembling, searching live web, and generating strategic report..."):
        result = my_crew.kickoff(inputs={"topic": topic})

        # Save output
        with open("mission_report.txt", "w", encoding="utf-8") as f:
            f.write(result)

        st.success("✅ Mission Complete")
        st.write(result)