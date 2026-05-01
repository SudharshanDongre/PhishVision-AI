import pandas as pd
df = pd.read_csv('Phishing.csv')
print("--- Result Column Analysis ---")
print(df['Result'].value_counts())
print("\nMapping -1 to 0 (Phishing) and 1 to 1 (Safe)...")
mapped_y = df['Result'].map({-1: 0, 1: 1})
print(mapped_y.value_counts())