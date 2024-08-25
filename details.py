import streamlit as st
import io
import base64
import pandas as pd
from PIL import Image

df = pd.DataFrame()
# Function to handle Base64 image data
def get_image_from_base64(base64_str):
    image_data = base64.b64decode(base64_str.split(",")[1])
    return Image.open(io.BytesIO(image_data))

# Function to display detailed information on a new page
def display_details(selected_row):
    st.write(f"### Issue: {selected_row['Issue']}")
    st.write(f"**Category:** {selected_row['Category']}")
    st.write(f"**Status:** {selected_row['Status']}")
    st.write(f"**Priority:** {selected_row['Priority']}")
    st.write(f"**Location:** {selected_row.get('location', 'Unknown')}")
    st.write("### Detailed Summary:")
    st.write(selected_row.get('text_summary', "No summary available."))

    if selected_row.get('file_data'):
        st.write("### Uploaded Media:")
        if 'image' in str(selected_row['file_data']).lower():
            image = get_image_from_base64(selected_row['file_data'])
            st.image(image, caption='Uploaded Image', use_column_width=True)
        elif 'video' in str(selected_row['file_data']).lower():
            st.video(io.BytesIO(base64.b64decode(selected_row['file_data'].split(",")[1])))

    st.write("### Original Complaint:")
    st.write(selected_row.get('original_complaint', "No original complaint available."))

# Check for query parameters to determine if we're on the details page
query_params = st.query_params()
if query_params.get("page") == ["details"]:
    index = int(query_params.get("id")[0])
    selected_row = df.iloc[index]
    display_details(selected_row)
else:
    st.write("No details to display.")
