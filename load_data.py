import pandas as pd

df = pd.read_csv(r"C:\Users\DELL\Downloads\archive\phishing_site_urls.csv")

print("Shape (rows, columns):", df.shape)
print()
print(df.head())
print()
print("Missing values:")
print(df.isnull().sum())
print()
print("Class balance:")
print(df["Label"].value_counts())
import matplotlib.pyplot as plt

print()
print("Duplicate URLs:", df["URL"].duplicated().sum())

df = df.drop_duplicates(subset="URL")
print("Rows after removing duplicates:", len(df))
print(df["Label"].value_counts())

df["Label"].value_counts().plot(kind="bar")
plt.title("Class balance")
plt.ylabel("Number of URLs")
plt.tight_layout()
plt.savefig("class_balance.png")
plt.show()

