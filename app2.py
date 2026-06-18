import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("### Capstone Project - Sales Performance Analysis")

# Upload Dataset
uploaded_file = st.file_uploader(
    "Upload E-Commerce Dataset",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Convert Date
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        (df["Region"].isin(region)) &
        (df["Category"].isin(category))
    ]

    # KPIs
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = len(filtered_df)
    total_customers = filtered_df["Customer Name"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("📦 Total Orders", total_orders)
    col4.metric("👥 Customers", total_customers)

    st.markdown("---")

    # Sales Trend
    sales_trend = filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"].sum().reset_index()

    sales_trend["Order Date"] = sales_trend["Order Date"].astype(str)

    fig1 = px.line(
        sales_trend,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Category & Region Analysis
    col5, col6 = st.columns(2)

    with col5:
        cat_sales = filtered_df.groupby(
            "Category"
        )["Sales"].sum().reset_index()

        fig2 = px.bar(
            cat_sales,
            x="Category",
            y="Sales",
            title="Category Wise Sales",
            text_auto=True
        )

        st.plotly_chart(fig2, use_container_width=True)

    with col6:
        region_sales = filtered_df.groupby(
            "Region"
        )["Sales"].sum().reset_index()

        fig3 = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            title="Region Wise Contribution"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Top Products
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top Products by Sales"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Customer Analysis
    st.subheader("👥 Top Customers")

    top_customers = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        top_customers,
        x="Customer Name",
        y="Sales",
        title="Top Customers"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # Data Table
    st.subheader("📋 Dataset Preview")
    st.dataframe(filtered_df)

else:
    st.info("Upload an E-Commerce CSV dataset.")