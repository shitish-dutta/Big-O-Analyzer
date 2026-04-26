import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# --- UI Configuration ---
st.set_page_config(page_title="Big-O Code Analyzer", page_icon="⚡", layout="wide")

st.title("⚡ The 'Big-O' Code Analyzer")
st.markdown("Analyze your algorithms for Time & Space Complexity, discover edge cases, and generate tests.")

# --- Visual Complexity Graphing Engine ---
def plot_complexity_curves():
    st.markdown("### Mathematical Complexity Reference")
    st.caption("Visualizing how operations scale as input (N) grows from 1 to 20.")
    
    n = np.arange(1, 21)
    data = pd.DataFrame({
        'O(1) Constant': np.ones(20),
        'O(log N) Logarithmic': np.log2(n),
        'O(N) Linear': n,
        'O(N log N) Log-Linear': n * np.log2(n),
        'O(N²) Quadratic': n**2
    })
    
    st.line_chart(data)

# --- Main Interface ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("1. Input Your Code")
    code_input = st.text_area("Paste your function here. The language will be detected automatically:", height=400, placeholder="def two_sum(nums, target):\n    ...")
    
    # Moved features from the deleted sidebar to the main UI
    st.markdown("**Options:**")
    generate_tests = st.checkbox("Generate Unit Tests", value=False, help="Automatically write a robust test suite for the detected language.")
    
    analyze_button = st.button("Analyze Code", type="primary", use_container_width=True)
    
    st.markdown("---")
    plot_complexity_curves()

with col2:
    st.subheader("2. SDE Interview Analysis")
    
    if analyze_button:
        if not code_input.strip():
            st.warning("Please paste some code to analyze.")
        else:
            try:
                # Secure API Key fetching via Streamlit Secrets
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                # Upgraded System Prompt to handle Auto-Detection
                model = genai.GenerativeModel(
                    model_name="gemini-3.1-flash-lite-preview",
                    system_instruction="""You are an expert SDE technical interviewer. 
                    Analyze the provided code and strictly structure your response using these exact headings:
                    
                    ### 🔍 Language Detected
                    Identify the programming language used in the snippet.
                    
                    ### ⏱️ Time & Space Complexity
                    * **Time Complexity:** State the exact Big-O and explain why in one concise sentence.
                    * **Space Complexity:** State the exact Big-O and explain why in one concise sentence.
                    
                    ### 💡 Optimization
                    If a more optimal approach exists, provide the optimized code snippet and state its new Big-O. If it is already fully optimal, clearly state 'Code is highly optimal.'
                    
                    ### 🛡️ Edge Cases
                    Identify 3 specific edge cases the author must consider that could break this implementation.
                    """
                )
                
                with st.spinner("Detecting language and analyzing complexity..."):
                    # The prompt is now language-agnostic
                    prompt = f"Code to analyze:\n{code_input}"
                    
                    if generate_tests:
                        prompt += "\n\nAdditionally, write a complete and robust unit test suite for this code using the standard testing framework for the detected language (e.g., pytest, JUnit, Jest)."
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown(response.text)
                    
            except KeyError:
                st.error("API Key not found. Please configure your Streamlit Secrets.")
            except Exception as e:
                st.error(f"An error occurred: {e}")