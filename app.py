import streamlit as st
import pandas as pd
from pandasai import Agent
from pandasai.llm import LLM
from openai import OpenAI
import yaml
import os


# Page Config
st.set_page_config(page_title="Student Info System", page_icon="🎓", layout="wide")

def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"api_key": "", "model_name": "xiaomi/mimo-v2-flash:free"}


class OpenRouterLLM(LLM):
    """Custom LLM class for OpenRouter API compatibility with PandasAI 3.0"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
    
    @property
    def type(self) -> str:
        return "openrouter"
    
    def call(self, instruction: str, context: str = None, suffix: str = "") -> str:
        """Generate a response from the LLM."""
        prompt = instruction
        if context:
            prompt = f"{context}\n\n{instruction}"
        if suffix:
            prompt = f"{prompt}\n\n{suffix}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful data analysis assistant. Generate Python code to answer questions about pandas DataFrames. Return only valid Python code without markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content


def main():
    config = load_config()

    st.title("🎓 Student Info System - Talk to Your Data")
    st.markdown("""
    Welcome! Upload your student data (Excel) and ask questions in plain English.
    """)

    # Sidebar for API Configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Load defaults from config if available
        default_api_key = config.get("api_key", "")
        default_model = config.get("model_name", "xiaomi/mimo-v2-flash:free")

        api_key = st.text_input("OpenRouter API Key", value=default_api_key, type="password", help="Enter your OpenRouter API key.")
        model_name = st.text_input("Model Name", value=default_model, help="e.g., openai/gpt-4o, xiaomi/mimo-v2-flash:free")
        st.markdown("---")
        st.markdown("**Example Queries:**")
        st.markdown("- Show students from Chennai")
        st.markdown("- Count students by gender")
        st.markdown("- List parents names for students in Grade 10")

    # Main Area
    uploaded_file = st.file_uploader("Upload your student data (.xlsx)", type=['xlsx'])

    if uploaded_file is not None:
        try:
            # Load Data
            df = pd.read_excel(uploaded_file)
            
            # Preprocess column names for PandasAI compatibility
            # Must only contain letters, numbers, and underscores
            import re
            def clean_column_name(col):
                # Replace spaces with underscores
                col = str(col).strip().replace(' ', '_')
                # Remove any character that isn't a letter, number, or underscore
                col = re.sub(r'[^a-zA-Z0-9_]', '', col)
                # Ensure it doesn't start with a number
                if col and col[0].isdigit():
                    col = '_' + col
                return col
            
            df.columns = [clean_column_name(col) for col in df.columns]
            
            # Convert Aadhar number to string if it exists
            if 'STUDENT_AADHAR_NUMBER' in df.columns:
                df['STUDENT_AADHAR_NUMBER'] = df['STUDENT_AADHAR_NUMBER'].astype(str)
                        
            # Display Raw Data Preview
            with st.expander("Preview Validated Data"):
                st.dataframe(df.head())
                st.caption(f"Total Records: {len(df)}")

            # Query Section
            st.divider()
            st.subheader("Ask your query")
            
            query = st.text_area("Enter your question:", placeholder="e.g., Show me all students living in Coimbatore")
            
            if st.button("Generate Response"):
                if not api_key:
                    st.error("Please enter your OpenRouter API Key in the sidebar to proceed.")
                elif not query:
                    st.warning("Please enter a query.")
                else:
                    with st.spinner("Analyzing data..."):
                        try:
                            # Initialize custom OpenRouter LLM
                            llm = OpenRouterLLM(api_key=api_key, model=model_name)
                            
                            # Initialize PandasAI Agent (v3.0 API)
                            agent = Agent([df], config={"llm": llm})
                            
                            # Chat with data
                            response = agent.chat(query)
                            
                            # Display Response
                            st.success("Analysis Complete!")
                            
                            if isinstance(response, pd.DataFrame):
                                st.dataframe(response)
                            else:
                                st.write(response)
                                
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()
