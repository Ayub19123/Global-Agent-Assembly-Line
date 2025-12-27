import streamlit as st
from crew import MyIndustrialCrew
import os

st.set_page_config(page_title="Industrial AI Architect Portal", layout="wide", page_icon="🚀")

st.title("🚀 Global Agent Assembly Line")
st.subheader("Autonomous Industrial Research & Strategy")
st.markdown("---")

# User Input Section
with st.sidebar:
    st.header("Mission Parameters")
    topic = st.text_input("Research Topic:", "OpenUSD 1.0 Industrial Impact")
    st.info("This agent uses DuckDuckGo Live Search to generate C-Suite ready reports.")

# Main Cockpit
if st.button("Launch Autonomous Mission"):
    if topic:
        with st.status("🛠️ Agents Assembling...", expanded=True) as status:
            try:
                st.write("Reading configurations...")
                crew_instance = MyIndustrialCrew()
                
                st.write("Agents are searching the live web...")
                result = crew_instance.run(inputs={'topic': topic})
                
                status.update(label="✅ Mission Complete!", state="complete", expanded=False)
                
                # Display Results
                st.success("Strategic Report Generated")
                st.markdown(result.raw)
                
                # Expandable Export Option
                with st.expander("📥 Export & Download Report"):
                    st.download_button(
                        label="Download as Text File",
                        data=result.raw,
                        file_name=f"{topic.replace(' ', '_')}_report.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Operational Error: {e}")
    else:
        st.warning("Please enter a mission topic to begin.")

st.markdown("---")
st.caption("Standard-Setting AI Architecture | Powered by CrewAI & Gemini")