import streamlit as st
import time
from datetime import datetime

# Optional: If you use LangChain or OpenAI API (don't hardcode key, use st.secrets)
# from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.llms import OpenAI

# App Config
st.set_page_config(page_title="Cleanser Product Page", page_icon="🛁")
st.title("Cleanser Product Page")

# Session state tracking
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "visit_count" not in st.session_state:
    st.session_state.visit_count = 1
else:
    st.session_state.visit_count += 1

# Time on page
elapsed_time = int(time.time() - st.session_state.start_time)
st.write(f"**Visit count:** {st.session_state.visit_count}")
st.write(f"**Time on page:** {elapsed_time} seconds")

# Assistant trigger logic
if st.session_state.visit_count > 2 or elapsed_time > 30:
    st.success("👉 Need help choosing a cleanser? I’m here to assist!")

# UI Inputs
skin_type = st.selectbox("What’s your skin type?", ["Dry", "Oily", "Combination", "Normal"])
skin_concerns = st.multiselect(
    "What’s your concern?", ["Acne", "Sensitivity", "Redness", "Wrinkles", "Dark Spots", "Open Pores"]
)

# Submit to get recommendation
if st.button("Find a Cleanser"):
    with st.spinner("Searching for best match..."):
        time.sleep(2)
        st.subheader("\ud83d\udd0d Recommended Cleanser")
        st.image("https://images.unsplash.com/photo-1600180758890-6b94519f735d", width=200)
        st.markdown("**Name:** Gentle Hydration Cleanser")
        st.markdown("**Price:** $18.99")
        st.markdown("**Skin Match:** Great for " + skin_type + " skin with concerns: " + ", ".join(skin_concerns))
        st.markdown("**Top Review:** \"Left my skin feeling clean but not dry!\"")

        # Feedback prompt
        st.markdown("---")
        st.subheader("\ud83d\udcca Was this recommendation helpful?")
        col1, col2 = st.columns([1, 4])
        with col1:
            helpful = st.radio("", ["👍 Yes", "👎 No"])
        with col2:
            comment = st.text_input("Any suggestions or feedback?")

        # Log the feedback (local simulation, normally you'd write this to a DB or file)
        if helpful or comment:
            feedback = {
                "datetime": str(datetime.now()),
                "visit_count": st.session_state.visit_count,
                "time_on_page": elapsed_time,
                "skin_type": skin_type,
                "concerns": skin_concerns,
                "was_helpful": helpful,
                "comment": comment
            }
            st.json(feedback)
          st.success("👉 Need help choosing a cleanser? I’m here to assist!")

