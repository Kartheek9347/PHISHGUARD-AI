import pandas as pd

datasets = []

# 1️⃣ phishing_email.csv
df1 = pd.read_csv("dataset/phishing_email.csv")
df1 = df1.rename(columns={"text_combined": "email_text"})
df1 = df1[["email_text", "label"]]
datasets.append(df1)

# 2️⃣ Enron.csv
df2 = pd.read_csv("dataset/Enron.csv")
df2["email_text"] = df2["subject"].fillna("") + " " + df2["body"].fillna("")
df2 = df2[["email_text", "label"]]
datasets.append(df2)

# 3️⃣ CEAS_08.csv
df3 = pd.read_csv("dataset/CEAS_08.csv")
df3["email_text"] = df3["subject"].fillna("") + " " + df3["body"].fillna("")
df3 = df3[["email_text", "label"]]
datasets.append(df3)

# 4️⃣ Nigerian_Fraud.csv
df4 = pd.read_csv("dataset/Nigerian_Fraud.csv")
df4["email_text"] = df4["subject"].fillna("") + " " + df4["body"].fillna("")
df4 = df4[["email_text", "label"]]
datasets.append(df4)

# 5️⃣ SpamAssasin.csv
df5 = pd.read_csv("dataset/SpamAssasin.csv")
df5["email_text"] = df5["subject"].fillna("") + " " + df5["body"].fillna("")
df5 = df5[["email_text", "label"]]
datasets.append(df5)

# 🔥 Combine all datasets
final_dataset = pd.concat(datasets, ignore_index=True)

# Remove empty rows
final_dataset.dropna(inplace=True)

# Save
final_dataset.to_csv("dataset/final_dataset.csv", index=False)

print("✅ Final dataset created successfully!")
print("Class distribution:")
print(final_dataset["label"].value_counts())