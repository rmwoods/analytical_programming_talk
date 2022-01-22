import pandas as pd

df = pd.read_csv("my_data.csv", index_col=0)
df = df.reset_index()
df["index"] = df["index"] / 1e3
df["a"] = df["Velocity (m/s)"] / df["index"].diff()
# df["a"]=df["a"].rolling(window=5).mean()
df2 = df[df["a"] > 9.81]
df2.to_csv("high_accels.csv")
