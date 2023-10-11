import streamlit as st
import pandas as pd
import io

# Title of the app
st.title('Excel Data Viewer')

# Add a file uploader to the app
file = st.file_uploader('Upload an Excel file', type=['xlsx', 'xls'])

# Check if a file is uploaded
if file:
    # Load the Excel file
    excel_data = pd.read_excel(file)

    # Display the dataframe
    st.write('Data from Excel file:')
    st.write(excel_data)
