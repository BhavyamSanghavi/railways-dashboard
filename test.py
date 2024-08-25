import datetime
import io

import altair as alt
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from PIL import Image

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
    df.rename(columns={"_id": "ID", "category": "Category", "original_complaint": "Issue", "status": "Status", "timestamp": "Date Submitted"}, inplace=True)
    df['Priority'] = df.apply(lambda x: "High" if "extremely negative" in str(x['text_summary']).lower() else ("Medium" if "negative" in str(x['text_summary']).lower() else "Low"), axis=1)
    return df

# Fetch and prepare the data
data = fetch_data()
df = convert_to_dataframe(data)

# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can view tickets, statistics, 
    and also view detailed information including any uploaded media.
    """
)

# Show section to view and edit existing tickets in a table.
st.header("Existing tickets")
st.write(f"Number of tickets: `{len(df)}`")

st.info(
    "Click on the Issue to view detailed information and any uploaded media. You can also sort the table by clicking on the column headers.",
    icon="📋",
)

# Function to display detailed information including media
def display_details(row):
    print(row)
    st.write(f"### Issue: {row['Issue']}")
    st.write(f"**Category:** {row['Category']}")
    st.write(f"**Status:** {row['Status']}")
    st.write(f"**Date Submitted:** {row['Date Submitted']}")
    st.write(f"**Priority:** {row['Priority']}")
    st.write("### Detailed Summary:")
    st.write(row['text_summary'] or "No summary available.")

    if row['file_data']:
        st.write("### Uploaded Media:")
        if row['file_data'] and 'image' in row['file_data']:
            image = Image.open(io.BytesIO(row['file_data']))
            st.image(image, caption='Uploaded Image', use_column_width=True)
        elif row['file_data'] and 'video' in row['file_data']:
            st.video(io.BytesIO(row['file_data']))

# Create an editable data editor with clickable issues
edited_df = st.data_editor(
    df[["ID", "Issue", "Category", "Status", "Priority", "Date Submitted"]],
    use_container_width=True,
    hide_index=True,
)

# Check if a row is clicked
selected_row = st.session_state.get("selected_row", None)
if selected_row:
    display_details(selected_row)

# Listen for row clicks
for index, row in edited_df.iterrows():
    if st.button(f"View Details of {row['ID']}", key=index):
        st.session_state.selected_row = row
        display_details(row)

# Show some metrics and charts about the tickets.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(df[df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
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
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

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
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")













import datetime
import io

import altair as alt
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from PIL import Image

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
    df.rename(columns={"_id": "ID", "category": "Category", "original_complaint": "Issue", "status": "Status", "timestamp": "Date Submitted"}, inplace=True)
    df['Priority'] = df.apply(lambda x: "High" if "extremely negative" in str(x['text_summary']).lower() else ("Medium" if "negative" in str(x['text_summary']).lower() else "Low"), axis=1)
    return df

# Fetch and prepare the data
data = fetch_data()
df = convert_to_dataframe(data)

# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can view tickets, statistics, 
    and also view detailed information including any uploaded media.
    """
)

# Show section to view and edit existing tickets in a table.
st.header("Existing tickets")
st.write(f"Number of tickets: `{len(df)}`")

st.info(
    "Click on the 'View Details' button to view detailed information and any uploaded media.",
    icon="📋",
)

# Function to display detailed information on a new page
def display_details(row):
    st.write(f"### Issue: {row['Issue']}")
    st.write(f"**Category:** {row['Category']}")
    st.write(f"**Status:** {row['Status']}")
    st.write(f"**Date Submitted:** {row['Date Submitted']}")
    st.write(f"**Priority:** {row['Priority']}")
    st.write(f"**Location:** {row.get('location', 'Unknown')}")
    st.write(f"**MongoDB ID:** {row['ID']}")
    st.write("### Detailed Summary:")
    st.write(row.get('text_summary', "No summary available."))

    if row.get('file_data'):
        st.write("### Uploaded Media:")
        if 'image' in str(row['file_data']).lower():
            image = Image.open(io.BytesIO(row['file_data']))
            st.image(image, caption='Uploaded Image', use_column_width=True)
        elif 'video' in str(row['file_data']).lower():
            st.video(io.BytesIO(row['file_data']))

    st.write("### Original Complaint:")
    st.write(row.get('original_complaint', "No original complaint available."))

# Display the table with an added button for viewing details
for index, row in df.iterrows():
    with st.expander(f"Issue ID: {row['ID']}"):
        st.write(f"**Issue:** {row['Issue']}")
        st.write(f"**Category:** {row['Category']}")
        st.write(f"**Status:** {row['Status']}")
        st.write(f"**Priority:** {row['Priority']}")
        st.write(f"**Date Submitted:** {row['Date Submitted']}")

        if st.button("View Details", key=f"button_{index}"):
            # Redirect to a new page with detailed information
            st.write("Redirecting to the detailed page...")
            display_details(row)

# Show some metrics and charts about the tickets.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(df[df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
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
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

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
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")





# image is gettin gdiaplayed

import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient
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
    df.rename(columns={"_id": "ID", "category": "Category", "original_complaint": "Issue", "status": "Status", "timestamp": "Date Submitted"}, inplace=True)
    df['Priority'] = df.apply(lambda x: "High" if "extremely negative" in str(x['text_summary']).lower() else ("Medium" if "negative" in str(x['text_summary']).lower() else "Low"), axis=1)
    return df

# Convert Base64 to Image
def base64_to_image(base64_str):
    try:
        # Check if the string has a prefix and remove it
        if base64_str.startswith('data:image'):
            base64_str = base64_str.split(',')[1]
        
        # Decode the Base64 string to binary data
        img_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(img_data))
    except Exception as e:
        st.error(f"Error decoding image: {e}")
        return None

# Fetch and prepare the data
data = fetch_data()
df = convert_to_dataframe(data)

# Show app title and description
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can view tickets, statistics, 
    and also view detailed information including any uploaded media.
    """
)

# Show section to view existing tickets in a table.
st.header("Existing Tickets")
st.write(f"Number of tickets: `{len(df)}`")

# Display the table with the relevant information
st.info(
    "You can sort the table by clicking on the column headers.",
    icon="📋",
)

# Add the "View" column with a button
def display_table():
    # Define the view_button function
    def view_button(row):
        if row['file_data']:
            with st.expander("View"):
                try:
                    # Decode and display the image
                    image = base64_to_image(row['file_data'])
                    if image:
                        st.image(image, caption='Uploaded Image', use_column_width=True)
                    else:
                        st.write("Error displaying image.")
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
        else:
            st.write("NA")

    # Display table with the "View" button
    df['View'] = df.apply(view_button, axis=1)
    st.dataframe(df[["Issue", "Category", "Status", "Priority", "Date Submitted", "View"]])

display_table()

# Show some metrics and charts about the tickets.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(df[df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
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





# all working fine withour image


import altair as alt
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    df.rename(columns={"_id": "ID", "category": "Category", "original_complaint": "Issue", "status": "Status", "timestamp": "Date Submitted", "text_summary": "Summary"}, inplace=True)
    df['Priority'] = df.apply(lambda x: "High" if "extremely negative" in str(x['Summary']).lower() else ("Medium" if "negative" in str(x['Summary']).lower() else "Low"), axis=1)
    return df

# Update status in MongoDB
def update_status(id, new_status):
    client = get_mongo_client()
    db = client['complaints_db']
    collection = db['complaints']
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

# Debugging step: print unique status values
# st.write(f"Unique Status Values in DataFrame: {df['Status'].unique()}")

# Function to toggle status
def toggle_status(id, current_status):
    new_status = "Done" if current_status == "Pending" else "Pending"
    update_status(id, new_status)
    st.experimental_rerun()

# Display the complaints in boxes
def display_complaints():
    status_options = ["Pending", "Done"]
    
    for _, row in df.iterrows():
        with st.expander(f"Complaint ID: {row['ID']}"):
            st.write(f"**Issue:** {row['Issue']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Priority:** {row['Priority']}")
            st.write(f"**Date Submitted:** {row['Date Submitted']}")
            st.write(f"**Summary:** {row['Summary']}")
            
            # Ensure the status value matches options
            current_status = row["Status"]
            if current_status not in status_options:
                current_status = status_options[0]  # Default to "Pending" if status is unexpected
            
            selected_status = st.selectbox("Status", status_options, index=status_options.index(current_status), key=row["ID"])
            if st.button("Update Status", key=f"update_{row['ID']}"):
                if selected_status != current_status:
                    toggle_status(row["ID"], selected_status)

display_complaints()

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
