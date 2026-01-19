import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
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
                            # Initialize LLM with OpenRouter Base URL
                            llm = OpenAI(
                                api_token=api_key,
                                api_base="https://openrouter.ai/api/v1",
                                model=model_name
                            )
                            
                            # Initialize SmartDataframe
                            sdf = SmartDataframe(df, config={"llm": llm})
                            
                            # Chat with data
                            response = sdf.chat(query)
                            
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
