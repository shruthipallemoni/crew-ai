from pathlib import Path
import streamlit as st
from crewai.project import load_crew

st.set_page_config(page_title="Blog Writer Crew", layout="wide")
st.title("🖋️ AI Blog Writing Crew")

topic = st.text_input("Enter a blog topic", placeholder="e.g. The role of engineering in nation building")

TASK_STEPS = {
    "research_task": "🔎 Researcher gathering information...",
    "writing_task": "✍️ Writer drafting the blog post...",
    "editing_task": "🧐 Editor polishing the final draft...",
}

if st.button("Generate Blog Post", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status_box = st.status("Starting crew...", expanded=True)

        def on_task_complete(task_output):
            name = getattr(task_output, "name", None) or str(task_output.description)[:40]
            status_box.write(f"✅ Finished: {name}")

        try:
            # crew.jsonc is at the project root, same folder as app.py
            crew, default_inputs = load_crew(Path(__file__).with_name("crew.jsonc"))
            crew.task_callback = on_task_complete

            status_box.write(TASK_STEPS.get("research_task", "Working..."))
            result = crew.kickoff(inputs={**default_inputs, "topic": topic})

            status_box.update(label="✅ Crew finished!", state="complete", expanded=False)
            st.markdown("### Result")
            st.markdown(str(result))

        except Exception as e:
            status_box.update(label="❌ Something went wrong", state="error")
            st.error(str(e))