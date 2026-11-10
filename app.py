import cv2
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from features import extract_features

st.set_page_config(page_title="QR-Shield", layout="centered")

st.markdown(
    """
    <style>
    .block-container {max-width: 640px; padding-top: 3rem;}
    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    return joblib.load("model.joblib")


model = load_model()

st.title("QR-Shield")
st.caption("Check whether the link inside a QR code looks like phishing.")

uploaded = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])

if uploaded is not None:
    file_bytes = np.frombuffer(uploaded.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    url, _, _ = cv2.QRCodeDetector().detectAndDecode(img)

    st.divider()

    if not url:
        st.write("No QR code found. Try a clearer, larger image.")
    else:
        features = extract_features(url)
        score = model.predict_proba(pd.DataFrame([features]))[0][1]

        if score >= 0.7:
            verdict, color = "Likely phishing", "#b42318"
        elif score >= 0.4:
            verdict, color = "Suspicious", "#b54708"
        else:
            verdict, color = "Looks low-risk", "#067647"

        st.markdown(
            f"<h2 style='color:{color}; margin-bottom:0'>{verdict}</h2>",
            unsafe_allow_html=True,
        )
        st.caption(f"Phishing score: {score:.0%}")

        st.write("Link inside the QR code (do not open it):")
        st.code(url, language=None)

        flags = []
        if features["uses_ip"]:
            flags.append("Uses an IP address instead of a domain name")
        if features["has_at"]:
            flags.append("Contains an @ symbol, which can hide the real destination")
        if features["suspicious_words"] > 0:
            flags.append(
                f"Contains {features['suspicious_words']} suspicious word(s), such as login or verify"
            )
        if features["subdomains"] >= 3:
            flags.append("Has many subdomains")
        if features["is_shortener"]:
            flags.append("Uses a link shortener that hides the destination")
        if features["url_length"] > 75:
            flags.append("Very long URL")
        if features["hyphens"] >= 3:
            flags.append("Many hyphens in the URL")

        st.subheader("Red flags")
        if flags:
            for f in flags:
                st.write("- " + f)
        else:
            st.write("None of the simple red-flag checks fired.")

        st.caption(
            "This is a model estimate, not a guarantee. "
            "Be careful with any link you do not recognise."
        )

st.divider()

with st.expander("How to stay safe from QR code phishing"):
    st.write("- Be careful with QR codes from strangers, flyers, emails, or random posters.")
    st.write("- Check whether a sticker has been placed over the original code in a public place.")
    st.write("- Look at the link preview your phone shows before opening it.")
    st.write("- Never enter a password or payment details on a page you reached through a QR code. Go to the official site yourself instead.")
    st.write("- Be suspicious of urgent messages, such as 'verify now' or 'account suspended'.")
    st.write("- If something looks wrong, do not open it. Report it to the organisation it pretends to be.")
    