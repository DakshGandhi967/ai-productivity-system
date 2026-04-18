import streamlit as st
import google.generativeai as genai
import os
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"

# 1. Setup API
# Secure your key: In a real app, use st.secrets!

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 2. Page Config
st.set_page_config(page_title="Optima AI Coach", page_icon="🚀")
st.title("AI Productivity Optimization System")

# 3. Sidebar Configuration (Satisfies Assessment Section 7)
with st.sidebar:
    st.header("Model Settings")
    temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.4)
    top_p = st.slider("Top-p (Sampling)", 0.0, 1.0, 0.8)
    st.info("Lower temperature = More factual/stable advice.")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# 4. Initialize the Model Object (Domain-Specific Control)
# We define the model here so it uses the slider values above
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config={
        "temperature": temp,
        "top_p": top_p,
    },
    system_instruction=(
        "You are the Optima AI Productivity Coach. Your domain is time management, "
        "focus techniques (Pomodoro, Eisenhower Matrix), and habit building. "
        "You must remain professional and redirect any non-productivity questions "
        "back to the user's goals."
    )
)

# 5. Initialize Memory (Satisfies Optional Enhancements)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Chat Interface Logic
if prompt := st.chat_input("How can I optimize my day?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    try:
        with st.spinner("Analyzing productivity patterns..."):
            # Use the session-based chat for memory
            response = st.session_state.chat_session.send_message(prompt)
            assistant_reply = response.text
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check your API key and internet connection.")