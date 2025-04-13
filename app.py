import streamlit as st
import openai
import textwrap
from datetime import datetime
import base64

# --- App Configuration ---
st.set_page_config(page_title="SmartHireAI", page_icon="🧠", layout="centered")
st.title("🧠 SmartHireAI")
st.markdown("### Create tailored resumes and cover letters instantly using AI")
st.markdown("---")

# --- Sidebar Instructions ---
st.sidebar.title("How to Use SmartHireAI")
st.sidebar.info(
    """
    **Steps:**
    
    1. Enter your OpenAI API key below (it’s hidden for security).  
    2. Paste a job description in the main text area.  
    3. Click "Generate Resume & Cover Letter" to see the AI-generated output.
    
    **Note:** Your API key is used only for your session and is not stored.
    """
)

# --- Input Fields ---
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
job_description = st.text_area("Paste the job description here:", height=200)

# --- Helper Function to Generate Download Links ---
def generate_download_link(text, filename):
    """Generates a link allowing the text to be downloaded as a file."""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'

# --- Button Action ---
if st.button("Generate Resume & Cover Letter"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    elif not openai_api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        # Set the API key for OpenAI
        openai.api_key = openai_api_key
        with st.spinner("Generating resume and cover letter..."):

            # Cleanly format the prompts
            prompt_resume = textwrap.dedent(f"""\
                Create a resume tailored to the following job listing:
                {job_description}
                
                Format it professionally with the following sections:
                - Name
                - Summary
                - Skills
                - Experience
                - Education
                """)
            
            prompt_cover = textwrap.dedent(f"""\
                Write a personalized cover letter for the following job:
                {job_description}
                
                The letter should be concise, confident, and aligned with the role.
                """)

            try:
                # Generate the resume using GPT
                resume_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_resume}],
                    temperature=0.7,
                    max_tokens=500,
                )

                # Generate the cover letter using GPT
                cover_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_cover}],
                    temperature=0.7,
                    max_tokens=500,
                )

                # Extract the generated text
                resume = resume_response['choices'][0]['message']['content']
                cover_letter = cover_response['choices'][0]['message']['content']

                st.success("Done! Here's your generated content:")

                # Display the outputs
                st.subheader("📄 Resume")
                st.code(resume, language="markdown")
                
                st.subheader("✉️ Cover Letter")
                st.code(cover_letter, language="markdown")
                
                # Create downloadable files for the outputs
                resume_filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                cover_filename = f"cover_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                
                st.markdown(generate_download_link(resume, resume_filename), unsafe_allow_html=True)
                st.markdown(generate_download_link(cover_letter, cover_filename), unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Something went wrong. Please check your API key or try again.")
