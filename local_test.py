import pandas as pd
from handler import clean
df = pd.read_csv("../sample_data/sales.csv")
print(clean(df).head()); print("Rows:", len(clean(df)))
