import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Sales Forecast Dashboard",
    layout="wide"
)

# ----------------------------
# Load Dataset
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv", encoding="latin1")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d/%m/%Y"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d/%m/%Y"
    )

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()

    return df

df = load_data()

# ----------------------------
# Sidebar
# ----------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Demand Segments"
    ]
)

# ======================================================
# PAGE 1
# ======================================================

if page == "Sales Overview":

    st.title("Sales Overview Dashboard")

    st.write("Interactive dashboard for Superstore sales analysis.")

    # ------------------------
    # Total Sales
    # ------------------------

    st.subheader("Total Sales by Year")

    yearly_sales = (
        df.groupby("Year")["Sales"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(8,4))

    yearly_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Sales")

    st.pyplot(fig)

    # ------------------------
    # Monthly Trend
    # ------------------------

    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        )["Sales"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        monthly_sales.index,
        monthly_sales.values,
        linewidth=2
    )

    ax.set_ylabel("Sales")

    st.pyplot(fig)

    # ------------------------
    # Interactive Filters
    # ------------------------

    st.subheader("Sales by Region & Category")

    region = st.selectbox(
        "Select Region",
        sorted(df["Region"].unique())
    )

    category = st.selectbox(
        "Select Category",
        sorted(df["Category"].unique())
    )

    filtered = df[
        (df["Region"] == region) &
        (df["Category"] == category)
    ]

    st.write(
        "Number of Orders:",
        len(filtered)
    )

    st.write(
        "Total Sales:",
        round(filtered["Sales"].sum(),2)
    )

    fig, ax = plt.subplots(figsize=(10,4))

    sns.lineplot(
        data=filtered,
        x="Order Date",
        y="Sales",
        ax=ax
    )

    st.pyplot(fig)