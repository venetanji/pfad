import streamlit as st
import pandas as pd

# load csv and display graph
df = pd.read_csv("tides.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# a date range to select a week 
if date_range := st.date_input("Select a date range", [df.index.min(), df.index.max()]):
    if len(date_range) == 2:
        df = df.loc[date_range[0]:date_range[1]]

st.line_chart(df["Height"])