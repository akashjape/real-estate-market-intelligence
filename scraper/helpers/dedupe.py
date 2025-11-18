import pandas as pd

df = pd.read_csv("../../data/parsed/pune/listings_cleaned.csv")
print("Before:", len(df))

df = df.drop_duplicates(subset=["listing_url"])
print("After:", len(df))

df.to_csv("../../data/parsed/pune/listings_cleaned_dedup.csv", index=False)
