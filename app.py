import streamlit as st
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["target_inventory"]

def load_data(collection_name):
    collection = db[collection_name]
    data = pd.DataFrame(list(collection.find()))
    if not data.empty:
        data['_id'] = data['_id'].astype(str)
        for column in data.columns:
            if data[column].dtype == 'object':
                try:
                    data[column] = data[column].apply(lambda x: str(x).encode('utf-8', 'ignore').decode('utf-8'))
                except Exception as e:
                    st.error(f"Error processing column {column}: {e}")
    return data

def add_custom_css(is_welcome_screen=False):
    if is_welcome_screen:
        gradient = "linear-gradient(to right, #e0f8f9, #e0f8f9)"
    else:
        gradient = "linear-gradient(to right, #e0f8f9, #e0f8f9)" 

    st.markdown(f"""
    <style>
    .stApp {{
        background: {gradient} !important;
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #000 !important;  /* Make all header levels black */
    }}
    .stButton>button {{
        width: 100% !important;
    }}
    .back-button {{
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: lightgray !important;
    }}
    .blue-button {{
        background-color: blue;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }}
    .green-button {{
        background-color: green;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }}
    .red-button {{
        background-color: red;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }}
    .left-shift {{
        margin-left: -30px;  /* Adjust this value to move the image more to the left */
    }}
    </style>
    """, unsafe_allow_html=True)

# Screen 1: Welcome Screen
def welcome_screen():
    add_custom_css(is_welcome_screen=True)
    image_path = "C:/Users/Lenovo/Documents/APIIT/Top-Up/Semester 2/Decision Alanytics/Target/target-inventory/assets/target.jpg"  # Use the uploaded image path
    col1, col2 = st.columns([1, 2]) 

    with col1:
        
        st.image(image_path, width=250)

    with col2:
        st.markdown("<h1 style='text-align: center;'>Data Management System for Target Corporation</h1>", unsafe_allow_html=True)

        
        st.markdown("<br><br>", unsafe_allow_html=True) 
        if st.button("Manage Customers"):
            st.session_state.selected_dataset = "customers"
            st.rerun()
        if st.button("Manage Orders"):
            st.session_state.selected_dataset = "orders"
            st.rerun()
        if st.button("Manage Payments"):
            st.session_state.selected_dataset = "payments"
            st.rerun()
        if st.button("Manage Products"):
            st.session_state.selected_dataset = "products"
            st.rerun()
        if st.button("Manage Sellers"):
            st.session_state.selected_dataset = "sellers"
            st.rerun()

# Screen 2: Dataset Selection
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def dataset_selection_screen():
    dataset = st.session_state.selected_dataset
    add_custom_css()  
    st.title(f"Managing {dataset}")

   
    data = load_data(dataset)

    if not data.empty:
        
        col1, col2, col3 = st.columns(3)  
        with col1:
            st.markdown("<h4 style='text-align: center;'>Total Entries</h4>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #1e90ff;'>{len(data)}</h2>", unsafe_allow_html=True)  
        
        with col2:
            st.markdown("<h4 style='text-align: center;'>Total Columns</h4>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #32cd32;'>{len(data.columns)}</h2>", unsafe_allow_html=True)  

        with col3:
            if "_id" in data.columns:
                st.markdown("<h4 style='text-align: center;'>Unique IDs</h4>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: #ff6347;'>{data['_id'].nunique()}</h2>", unsafe_allow_html=True)  

        
        st.markdown("<h5>Choose Columns to Display</h5>", unsafe_allow_html=True)
        selected_columns = st.multiselect(
            "Select columns to view",
            options=data.columns.tolist(),
            default=data.columns.tolist()
        )
        filtered_data = data[selected_columns]

        
        search_term = st.text_input("Search data", "")
        
        if search_term:
            filtered_data = filtered_data[filtered_data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        
        st.markdown("""
        <style>
        /* Style the entire table */
        .stDataFrame { 
            border: 1px solid #ddd !important;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Table header style */
        .stDataFrame thead th {
            background-color: #1e90ff;
            color: white;
            font-size: 1rem;
            text-align: center;
            padding: 10px;
        }

        /* Table row hover effect */
        .stDataFrame tbody tr:hover {
            background-color: #f0f8ff;
            cursor: pointer;
        }

        /* Alternate row shading */
        .stDataFrame tbody tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        /* Table cells styling */
        .stDataFrame tbody td {
            text-align: center;
            padding: 10px;
            font-size: 0.95rem;
        }

        /* Scrollbar styling */
        .stDataFrame::-webkit-scrollbar {
            width: 8px;
        }
        .stDataFrame::-webkit-scrollbar-thumb {
            background-color: #1e90ff;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        
        col_data, col_actions = st.columns([4, 1], gap="large")

        with col_data:
            st.dataframe(filtered_data)  

        with col_actions:
            st.markdown("<h5>Actions</h5>", unsafe_allow_html=True)
            if st.button("Add Data", key="add", use_container_width=True):
                st.session_state.action = "add"
                st.rerun()
            if st.button("Update Data", key="update", use_container_width=True):
                st.session_state.action = "update"
                st.rerun()
            if st.button("Delete Data", key="delete", use_container_width=True):
                st.session_state.action = "delete"
                st.rerun()

            
            if st.button("Back", key="back", use_container_width=True):
                del st.session_state.selected_dataset
                st.rerun()
    else:
        st.write("No data available in this collection.")

# Screen 3: Add Data
def add_data_screen():
    dataset = st.session_state.selected_dataset
    add_custom_css()  
    st.title(f"Add Data to {dataset}")

    
    col_back, col_title = st.columns([0.1, 0.9])
    with col_back:
        if st.button("Back", key="back-button"):
            del st.session_state.action
            st.rerun()  

    with st.form("add_form"):
        new_data = {}
        columns = load_data(dataset).columns
        for column in columns:
            if column != "_id":  
                new_data[column] = st.text_input(f"Enter {column}:")
        
        if st.form_submit_button("Submit"):
            db[dataset].insert_one(new_data)  
            st.success("Data added successfully!")  
            st.stop()  

# Screen 4: Update Data
def update_data_screen():
    dataset = st.session_state.selected_dataset
    add_custom_css()  
    st.title(f"Update Data in {dataset}")

    
    col_back, col_title = st.columns([0.1, 0.9])
    with col_back:
        if st.button("Back", key="back-button"):
            del st.session_state.action
            st.rerun() 

    data = load_data(dataset)
    if data.empty:
        st.write("No data available to update.")
        return


    search_term = st.text_input("Search:", "")
    if search_term:
        data = data[data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    if not data.empty:
        selected_id = st.selectbox("Select Data ID to Update:", data['_id'])
        if selected_id:
            try:
                selected_object_id = ObjectId(selected_id)
                selected_data = data[data['_id'] == selected_id].iloc[0]
                
                with st.form("update_form"):
                    updated_data = {}
                    for column in selected_data.index:
                        updated_data[column] = st.text_input(f"Update {column}:", selected_data[column])
                    
                    if '_id' in updated_data:
                        del updated_data['_id']

                    if st.form_submit_button("Submit"):
                        db[dataset].update_one({"_id": selected_object_id}, {"$set": updated_data})
                        st.success("Data updated successfully!")
                        st.stop()  

            except InvalidId:
                st.error(f"'{selected_id}' is not a valid ObjectId. Please select a valid ID.")
    else:
        st.error("No records found matching the search term.")

# Screen 5: Delete Data
def delete_data_screen():
    dataset = st.session_state.selected_dataset
    add_custom_css()  
    st.title(f"Delete Data from {dataset}")

    
    col_back, col_title = st.columns([0.1, 0.9])
    with col_back:
        if st.button("Back", key="back-button"):
            del st.session_state.action
            st.rerun() 

    data = load_data(dataset)
    if data.empty:
        st.write("No data available to delete.")
        return


    search_term = st.text_input("Search:", "")
    if search_term:
        data = data[data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    if not data.empty:
        selected_id = st.selectbox("Select Data ID to Delete:", data['_id'])
        if selected_id:
            if st.button("Delete"):
                db[dataset].delete_one({"_id": ObjectId(selected_id)})
                st.success("Data deleted successfully!")
                st.stop()  
    else:
        st.error("No records found matching the search term.")

# Main Application Logic
if "selected_dataset" not in st.session_state:
    welcome_screen()
elif "action" not in st.session_state:
    dataset_selection_screen()
elif st.session_state.action == "add":
    add_data_screen()
elif st.session_state.action == "update":
    update_data_screen()
elif st.session_state.action == "delete":
    delete_data_screen()
