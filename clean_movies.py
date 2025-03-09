import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("movies.csv", delimiter=",", skipinitialspace=True)

# Clean YEAR (remove parentheses)
df["YEAR"] = df["YEAR"].str.replace(r"[()]", "", regex=True).astype(str)

# Clean GENRE (remove extra spaces)
df["GENRE"] = df["GENRE"].str.strip()

# Clean VOTES (remove commas, convert to integer)
df["VOTES"] = df["VOTES"].replace(",", "", regex=True).replace("", np.nan).astype(float).fillna(0).astype(int)

# Clean RATING (convert to float)
df["RATING"] = pd.to_numeric(df["RATING"], errors="coerce")

# Clean RunTime (replace NaN with 0 and convert to integer)
df["RunTime"] = df["RunTime"].fillna(0).astype(int)

# Extract STARS (remove unnecessary text)
df["STARS"] = df["STARS"].str.replace("\n", "").str.replace("    Stars:", "").str.strip()

# Extract DIRECTOR (if present)
df["DIRECTOR"] = df["ONE-LINE"].astype(str).fillna("").str.extract(r"Director:\s*([^\|]*)")[0].str.strip()

# Keep only relevant columns
df_cleaned = df[["MOVIES", "YEAR", "GENRE", "RATING", "STARS", "VOTES", "RunTime", "DIRECTOR"]]

# Normalize GENRE (each genre as a separate row)
df_genres = df_cleaned[["MOVIES", "GENRE"]].explode("GENRE")

# Save cleaned data
cleaned_csv_path = "cleaned_movies.csv"
df_cleaned.to_csv(cleaned_csv_path, index=False)
df_genres.to_csv("cleaned_genres.csv", index=False)

print(f"Cleaned data saved to {cleaned_csv_path} and cleaned_genres.csv")
