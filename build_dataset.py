import pandas as pd
from features import extract_features

df = pd.read_csv(r"C:\Users\DELL\Downloads\archive\phishing_site_urls.csv")
df = df.drop_duplicates(subset="URL")
df = df.sample(n=100000, random_state=42)

rows = df["URL"].apply(extract_features).tolist()
data = pd.DataFrame(rows)
data["label"] = (df["Label"] == "bad").astype(int).values

data.to_csv("features.csv", index=False)

print(data.head())
print()
print(data["label"].value_counts())
