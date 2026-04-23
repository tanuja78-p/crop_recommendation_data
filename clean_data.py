import pandas as pd

data = pd.read_csv("crop-yield.csv")

# cleaning steps
data = data.dropna()
data = data.drop_duplicates()

data.columns = data.columns.str.strip().str.lower()

data = data[(data["temperature"] > 0) & (data["temperature"] < 50)]

data.to_csv("cleaned_data.csv", index=False)

print("Data cleaned successfully")