import sys
import cv2
import joblib
import pandas as pd
from features import extract_features


def decode_qr(path):
    img = cv2.imread(path)
    if img is None:
        return None
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return data or None


def phishing_score(url, model):
    features = pd.DataFrame([extract_features(url)])
    return model.predict_proba(features)[0][1]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "test_qr.png"
    url = decode_qr(path)
    if url is None:
        print("No QR code found in", path)
    else:
        model = joblib.load("model.joblib")
        score = phishing_score(url, model)
        print("URL inside QR:", url)
        print(f"Phishing score: {score:.0%}")
        print("Features:", extract_features(url))
        