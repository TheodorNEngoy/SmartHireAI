import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="SmartHireAI", layout="centered")
st.title("🧠 SmartHireAI")
st.subheader("Create tailored resumes and cover letters instantly.")

job_description = st.text_area("Paste the job description here:")

if st.button("Generate Resume & Cover Letter"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Generating resume and cover letter..."):

            prompt_resume = f"""Create a resume tailored to the following job listing:
            {job_description}
            Format it professionally with name, summary, skills, experience, education."""
            
            prompt_cover = f"""Write a personalized cover letter for the following job:
            {job_description}
            Keep it concise, confident, and aligned with the role."""

            try:
                resume_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_resume}],
                    temperature=0.7
                )

                cover_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_cover}],
                    temperature=0.7
                )

                resume = resume_response['choices'][0]['message']['content']
                cover_letter = cover_response['choices'][0]['message']['content']

                st.success("Done! Here's your resume and cover letter:")

                st.subheader("📄 Resume")
                st.code(resume, language="markdown")

                st.subheader("✉️ Cover Letter")
                st.code(cover_letter, language="markdown")

            except Exception as e:
                st.error("An error occurred. Check your API key or try again later.")
