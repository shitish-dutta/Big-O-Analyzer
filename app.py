import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Big-O Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* =========================
   GLOBAL
========================= */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 45%,
            #ffffff 100%
        );

    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);

    background-size: 40px 40px;

    color: #0f172a;
    overflow-x: hidden;
}

/* =========================
   FLOATING BLOBS
========================= */

.stApp::before {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.10), transparent 70%);
    top: -120px;
    left: -120px;
    animation: float1 10s ease-in-out infinite alternate;
    z-index: -1;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.08), transparent 70%);
    bottom: -120px;
    right: -100px;
    animation: float2 12s ease-in-out infinite alternate;
    z-index: -1;
}

@keyframes float1 {
    from {
        transform: translate(0px, 0px);
    }
    to {
        transform: translate(40px, 30px);
    }
}

@keyframes float2 {
    from {
        transform: translate(0px, 0px);
    }
    to {
        transform: translate(-30px, -40px);
    }
}

/* =========================
   MAIN CONTAINER
========================= */

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px;
}

/* =========================
   TITLE
========================= */

.main-title {
    font-size: 4rem;
    font-weight: 800;
    text-align: center;
    color: #312e81;
    margin-bottom: 8px;
    animation: fadeUp 0.8s ease;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1.05rem;
    margin-bottom: 45px;
    animation: fadeUp 1.2s ease;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* =========================
   SECTION HEADINGS
========================= */

.section-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    color: #111827;
}

/* =========================
   GLASS CARD
========================= */

.glass {
    background: rgba(255,255,255,0.62);
    border: 1px solid rgba(255,255,255,0.8);
    backdrop-filter: blur(8px);
    border-radius: 24px;
    padding: 24px;

    box-shadow:
        0 4px 20px rgba(15,23,42,0.04),
        0 1px 2px rgba(15,23,42,0.04);

    transition: all 0.25s ease;
}

.glass:hover {
    transform: translateY(-2px);
    box-shadow:
        0 10px 30px rgba(99,102,241,0.08);
}

/* =========================
   TEXT AREA
========================= */

textarea {
    background: rgba(255,255,255,0.55) !important;
    color: #0f172a !important;

    border-radius: 20px !important;
    border: 1px solid #dbeafe !important;

    font-size: 15px !important;
    line-height: 1.7 !important;

    padding: 18px !important;
}

/* =========================
   BUTTON
========================= */

.stButton > button {
    width: 100%;
    height: 3.2em;

    border-radius: 14px;
    border: none;

    font-size: 1rem;
    font-weight: 600;

    color: white;

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );

    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 24px rgba(99,102,241,0.25);
}

/* =========================
   RESULT BOX
========================= */

.result-box {
    background: rgba(255,255,255,0.65);

    border-radius: 22px;
    padding: 28px;

    border: 1px solid rgba(226,232,240,1);

    backdrop-filter: blur(10px);

    line-height: 1.8;
}

.result-box h3 {
    color: #4338ca;
    margin-top: 1.5rem;
}

.result-box p,
.result-box li {
    color: #334155;
    line-height: 1.8;
}

/* =========================
   CHECKBOX
========================= */

.stCheckbox label {
    color: #334155 !important;
}

/* =========================
   METRICS
========================= */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(226,232,240,1);

    padding: 14px;
    border-radius: 16px;

    box-shadow: 0 2px 8px rgba(15,23,42,0.03);
}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #c7d2fe;
    border-radius: 20px;
}

/* =========================
   HIDE STREAMLIT ELEMENTS
========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="main-title">
⚡ Big-O Analyzer
</div>

<div class="subtitle">
Modern AI-Powered Complexity Analysis • Edge Case Detection • Test Generation
</div>
""", unsafe_allow_html=True)

# =========================
# COMPLEXITY GRAPH
# =========================
def plot_complexity_curves():

    st.markdown("### 📈 Complexity Growth")

    n = np.arange(1, 21)

    data = pd.DataFrame({
        'O(1)': np.ones(20),
        'O(log N)': np.log2(n),
        'O(N)': n,
        'O(N log N)': n * np.log2(n),
        'O(N²)': n**2
    })

    st.line_chart(data, height=320)

# =========================
# LAYOUT
# =========================
left, right = st.columns([1.05, 1])

# =========================
# LEFT PANEL
# =========================
with left:

    st.markdown("""
    <div class="section-title">
    💻 Paste Your Code
    </div>
    """, unsafe_allow_html=True)

    code_input = st.text_area(
        "",
        height=430,
        placeholder="""def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        diff = target - num

        if diff in seen:
            return [seen[diff], i]

        seen[num] = i""",
        label_visibility="collapsed"
    )

    generate_tests = st.checkbox(
        "Generate Unit Tests"
    )

    analyze_button = st.button(
        "⚡ Analyze Code"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # COMPLEXITY METRICS
    # =========================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("O(1): Constant", "")

    with c2:
        st.metric("O(log N): Fast", "")

    with c3:
        st.metric("O(N): Scalable", "")

    with c4:
        st.metric("O(N²): Expensive", "")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # GRAPH SECTION
    # =========================

    plot_complexity_curves()

# =========================
# RIGHT PANEL
# =========================
with right:

    st.markdown("""
    <div class="section-title">
    🧠 AI Interview Analysis
    </div>
    """, unsafe_allow_html=True)

    if analyze_button:

        if not code_input.strip():
            st.warning("Please paste some code first.")

        else:
            try:

                api_key = st.secrets["GEMINI_API_KEY"]

                genai.configure(api_key=api_key)

                model = genai.GenerativeModel(
                    model_name="gemini-3.1-flash-lite-preview",

                    system_instruction="""
You are an expert SDE technical interviewer.

Analyze the provided code and STRICTLY structure your response using these exact headings:

### 🔍 Language Detected
Identify the programming language used.

### ⏱️ Time & Space Complexity
* **Time Complexity:** State the exact Big-O and explain why briefly.
* **Space Complexity:** State the exact Big-O and explain why briefly.

### 💡 Optimization
If a better approach exists, provide optimized code and explain the new complexity.
If already optimal, say 'Code is highly optimal.'

### 🛡️ Edge Cases
Mention 3 important edge cases.

### 🧪 Unit Tests
Only include if requested.
"""
                )

                with st.spinner("⚡ Running Deep AI Analysis..."):

                    prompt = f"""
Analyze this code:

{code_input}
"""

                    if generate_tests:
                        prompt += """

Also generate a complete robust unit test suite
using the standard framework for the language.
"""

                    response = model.generate_content(prompt)

                    st.markdown(
                        f"""
                        <div class="result-box">
                        {response.text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except KeyError:
                st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")

            except Exception as e:
                st.error(f"Error: {e}")

    else:

        st.markdown("""
        <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        height:600px;
        flex-direction:column;
        text-align:center;
        ">

        <div class="pulse-ring">
        ⚡
        </div>

        <h2 style="
        margin-top:20px;
        color:#475569;
        ">
        Ready for Analysis
        </h2>

        <p style="
        color:#64748b;
        max-width:400px;
        line-height:1.7;
        ">
        Paste your algorithm and get AI-powered
        complexity insights, optimization ideas,
        and edge case analysis.
        </p>

        </div>

        <style>

        .pulse-ring{
            width:100px;
            height:100px;

            border-radius:50%;

            display:flex;
            align-items:center;
            justify-content:center;

            font-size:48px;

            background:rgba(99,102,241,0.1);

            animation:pulse 2s infinite;
        }

        @keyframes pulse{

            0%{
                box-shadow:0 0 0 0 rgba(99,102,241,0.3);
            }

            70%{
                box-shadow:0 0 0 25px rgba(99,102,241,0);
            }

            100%{
                box-shadow:0 0 0 0 rgba(99,102,241,0);
            }
        }

        </style>
        """, unsafe_allow_html=True)
