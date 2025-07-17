
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Cleanser descriptions
descriptions = [
    "CeraVe Hydrating Facial Cleanser: Great for dry, eczema-prone skin. Fragrance-free and non-foaming.",
    "Neutrogena Oil-Free Acne Wash: Effective for breakouts. Contains salicylic acid. May dry sensitive skin.",
    "La Roche-Posay Toleriane Cleanser: Gentle on redness, good for sensitive combo skin.",
    "Vanicream Gentle Cleanser: No fragrance or sulfates. Ideal for allergy-prone users.",
    "COSRX Low pH Gel Cleanser: Tea tree and BHA for oily or acne-prone skin. pH balanced."
]

# Embed with sentence-transformers
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
vectors = embedding_model.encode(descriptions)
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors))
metadata = {i: descriptions[i] for i in range(len(descriptions))}

# Search function
def get_recommendation(query, top_k=3):
    query_vec = embedding_model.encode([query])
    D, I = index.search(np.array(query_vec), k=top_k)
    return [metadata[i] for i in I[0]]

# Streamlit UI
st.title("🧴 Smart Cleanser Finder")

skin_type = st.selectbox("What is your skin type?", ["Dry", "Oily", "Combination", "Sensitive"])
concern = st.selectbox("What is your main concern?", ["Acne", "Redness", "Dryness", "Fragrance sensitivity"])
budget = st.slider("What is your budget range?", 5, 30, 15)

query = f"I have {skin_type.lower()} skin and my concern is {concern.lower()}. I need a cleanser under ${budget}."

if st.button("Get Recommendations"):
    st.write("🔍 Searching for best matches...")
    recs = get_recommendation(query)
    for r in recs:
        st.success(r)
