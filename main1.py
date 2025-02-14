import time

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
def generate_data():
    np.random.seed(42)
    return pd.DataFrame({
        'Time': list(range(1, 11)),
        'Value': np.random.randint(1, 100, 10)
    })

df = generate_data()

# Streamlit App
st.title("Animated Chart with Pandas and Matplotlib")

st.write("### Sample DataFrame:")
st.dataframe(df)

# Animated Chart using Matplotlib
st.write("### Animated Chart:")
chart_placeholder = st.empty()

for i in range(1, 11):
    plt.clf()
    plt.plot(df['Time'][:i], df['Value'][:i], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Real-Time Data Plot")
    chart_placeholder.pyplot(plt)
    time.sleep(0.5)