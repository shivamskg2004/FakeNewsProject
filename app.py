import streamlit as st
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.title("Fake News Detection App")

news = st.text_area("Enter News Text")

if st.button("Check"):
    vec = vectorizer.transform([news])
    prediction = model.predict(vec)

    if prediction[0] == 0:
        st.error("This is FAKE News")
    else:
        st.success("This is REAL News")