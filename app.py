import altair as alt
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from PIL import Image
import io
import base64

# MongoDB connection
def get_mongo_client():
    client = MongoClient('mongodb+srv://jawan2608:vgIsDeU7MZvmZXE5@railways.9alpg.mongodb.net/?retryWrites=true&w=majority&appName=Railways')
    return client

# Fetch data from MongoDB
def fetch_data():
    client = get_mongo_client()
    db = client['complaints_db']  # Database name
    collection = db['complaints']  # Collection name
    data = list(collection.find())
    return data

# Convert MongoDB data to DataFrame
def convert_to_dataframe(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.rename(columns={"_id": "ID", "category": "Category", "original_complaint": "Issue", "status": "Status", "timestamp": "Date Submitted", "text_summary": "Summary", "file_data": "File Data"}, inplace=True)
    df['Priority'] = df.apply(lambda x: "High" if "extremely negative" in str(x['Summary']).lower() else ("Medium" if "negative" in str(x['Summary']).lower() else "Low"), axis=1)
    return df

# Update status in MongoDB
def update_status(id, new_status):
    client = get_mongo_client()
    db = client['complaints_db']
    collection = db['complaints']
    print(new_status)
    collection.update_one({"_id": id}, {"$set": {"status": new_status}})

# Fetch and prepare the data
data = fetch_data()
df = convert_to_dataframe(data)

# Category filter
complaint_categories = [
    "All",
    "Food Quality",
    "Food Safety",
    "Service Quality",
    "Cleanliness",
    "Comfort",
    "Facilities",
    "Timeliness",
    "Safety and Security",
    "Noise Levels",
    "Accessibility",
    "Booking and Ticketing",
    "Luggage Handling",
    "Communication",
    "Temperature Control",
    "Food Availability"
]

# Show app title and description
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can view tickets, statistics, 
    and also view detailed information.
    """
)

# Category filter
category_filter = st.selectbox("Filter by Category", complaint_categories)
if category_filter != "All":
    df = df[df['Category'] == category_filter]

# Show section to view existing tickets in a table.
st.header("Existing Tickets")
st.write(f"Number of tickets: `{len(df)}`")

# Function to toggle status
def toggle_status(id, current_status):
    print(current_status)
    new_status = "Done" if current_status == "Done" else "Pending"
    with st.spinner("Updating status..."):
        update_status(id, new_status)
        st.success("Status updated successfully!")
    st.rerun()

# Function to decode base64 image data
def decode_base64_image(base64_data):
    try:
        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        st.error(f"Error decoding image: {e}")
        return None

# Display the complaints in boxes
def display_complaints():
    status_options = ["Pending", "Done"]
    
    for _, row in df.iterrows():
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.expander(f"Complaint ID: {row['ID']}"):
            st.write(f"**Issue:** {row['Issue']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Priority:** {row['Priority']}")
            st.write(f"**Date Submitted:** {row['Date Submitted']}")
            st.write(f"**Summary:** {row['Summary']}")
            
            # Display image if present
            if pd.notna(row["File Data"]):
                image = decode_base64_image(row["File Data"])
                if image:
                    st.image(image, caption="Complaint Image", use_column_width=True)
            
            # Dropdown for status update
            current_status = row["Status"]
            if current_status not in status_options:
                current_status = status_options[0]  # Default to "Pending" if status is unexpected
            
            selected_status = st.selectbox("Status", status_options, index=status_options.index(current_status), key=row["ID"])
            if st.button("Update Status", key=f"update_{row['ID']}"):
                if selected_status != current_status:
                    toggle_status(row["ID"], selected_status)

display_complaints()

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
# Show some metrics and charts about the tickets.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(df[df.Status == "Pending"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("")
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True)

st.write("")
st.write("")
st.write("")
st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True)
