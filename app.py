import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our app
st.set_page_config(page_title="📊 Data Sweeper", layout="wide")
st.title("📊 Data Sweeper")
st.write("✨ Transform your file between CSV and Excel formats with built-in data cleaning and visualization! ✨")

# File uploader
uploaded_files = st.file_uploader("📂 Upload your file (CSV or Excel):", 
                                  type=["csv", "xlsx"], 
                                  accept_multiple_files=True)

# Process files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display Data
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of our df
        st.write("🔎 **Preview the head of the Dataframe:**")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("⚒️ Data Cleaning Options")
        if st.checkbox(f"🧹 Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"❌ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🔄 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

        # Choose specific columns to keep or convert
        st.subheader("🧭 Select Columns to Convert")
        if not df.empty:
            columns = st.multiselect(f"📌 Choose columns for {file.name}", df.columns, default=list(df.columns))
            if columns:
                df = df[columns]
            else:
                st.warning("⚠️ Please select at least one column!")
        else:
            st.warning(f"⚠️ {file.name} has no data!")

        # Create some visualizations
        st.subheader("📈 Data Visualizations")
        if st.checkbox(f"📊 Show visualizations for {file.name}"):
            numeric_cols = df.select_dtypes(include='number')
            if not numeric_cols.empty:
                st.bar_chart(numeric_cols.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization!")

        # Convert the file CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"🔧 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"🛠️ Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉🥳 All files successfully processed! 🎉🥳")