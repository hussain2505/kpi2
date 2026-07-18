import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive EDA Dashboard", layout="wide")

st.title("📊 Interactive Exploratory Data Analysis Dashboard")
st.write("Upload your dataset to instantly inspect, clean, and visualize your data.")

# 1. File Upload Section
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    st.success("File uploaded successfully!")
    
    # 2. Data Inspection Section
    st.header("1. Data Inspection")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Duplicate Rows", df.duplicated().sum())
    
    st.subheader("Raw Data Preview (First 5 Rows)")
    st.dataframe(df.head())
    
    st.subheader("Data Types and Missing Values")
    missing_df = pd.DataFrame({
        'Data Type': df.dtypes.astype(str),
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(missing_df)

    # 3. Basic Data Cleaning Section
    st.header("2. Quick Data Cleaning")
    handle_missing = st.checkbox("Automatically fill numerical missing values with the column median?")
    if handle_missing:
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
        st.info("Numerical missing values have been replaced with their respective medians.")

    # 4. Statistical Summary Section
    st.header("3. Statistical Summary")
    st.write(df.describe(include='all').fillna('-'))

    # 5. Data Visualization Section
    st.header("4. Data Visualization")
    
    # Separate columns by type for plotting
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Dropdown for plot selection
    plot_type = st.selectbox("Select Plot Type", [
        "Histogram (Univariate Distribution)", 
        "Scatter Plot (Bivariate Relationship)", 
        "Correlation Heatmap"
    ])

    if plot_type == "Histogram (Univariate Distribution)":
        if numeric_columns:
            selected_col = st.selectbox("Select a numeric column to view its distribution:", numeric_columns)
            fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available for a histogram.")

    elif plot_type == "Scatter Plot (Bivariate Relationship)":
        if len(numeric_columns) >= 2:
            col_x = st.selectbox("Select X-axis column (Numeric):", numeric_columns, index=0)
            col_y = st.selectbox("Select Y-axis column (Numeric):", numeric_columns, index=min(1, len(numeric_columns)-1))
            
            # Optional color categorization
            color_col = None
            if categorical_columns:
                use_color = st.checkbox("Color points by a categorical column?")
                if use_color:
                    color_col = st.selectbox("Select category column:", categorical_columns)
            
            fig = px.scatter(df, x=col_x, y=col_y, color=color_col, title=f"{col_y} vs {col_x}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("You need at least 2 numeric columns to create a scatter plot.")

    elif plot_type == "Correlation Heatmap":
        if len(numeric_columns) >= 2:
            corr = df[numeric_columns].corr()
            fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', title="Correlation Heatmap Matrix")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough numeric data to generate a correlation heatmap.")

else:
    st.info("💡 Please upload a CSV file using the sidebar or upload box above to begin your analysis.")