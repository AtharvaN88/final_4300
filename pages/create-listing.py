import streamlit as st
import base64
from utils.utils import upload_obj_to_s3

def convert_images_to_bytes(file):
    bytes_data = file.read()
    encoded_str = base64.b64encode(bytes_data).decode("utf-8")
    return encoded_str

with st.form(key="upload_form", clear_on_submit=False):
    st.subheader('Apartment Details')

    address = st.text_input(
        "Enter Address"
    )
    city = st.text_input(
        "Enter city"
    )
    # TODO: get lists for both the cities/ states and make this a selectbox
    state = st.text_input(
        "Enter State"
    )

    price = st.number_input("Enter rent amount", max_value=999999)

    zip_code = st.number_input("Enter a Zip code", max_value=99999)

    st.subheader('Seller Information')
    col1, col2 = st.columns([1,1])
    with col1:
        first_name = st.text_input("First Name")

    with col2:
        last_name = st.text_input("Last Name")

    phone_number = st.number_input("Phone Number", max_value=999999999)

    st.subheader("Unit information")

    col1, col2 = st.columns([1,1])
    with col1:
        bedrooms = st.number_input("Bedrooms", max_value=10)

    with col2:
        bathrooms = st.number_input("Bathrooms", max_value=10)

    uploaded_files = st.file_uploader(
        "Upload Images", accept_multiple_files=True
    )

    submitted = st.form_submit_button("Submit")
    if submitted:
        name = f'{first_name} {last_name}'
        images = []
        for uploaded_file in uploaded_files:
            encoding = convert_images_to_bytes()
            images.append(encoding)

        phone_converted = str(phone_number)

        json_payload = {
            "city": city,
            "state": state,
            "address": address,
            "zip": zip_code,
            "rent": price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "appliances": ["diswasher"],
            "images": images,
            "seller": {
            "name": name,
            "contact": phone_converted
            }
        }

        upload_obj_to_s3(json_payload)
        st.success('Listing Created, it may take some time for it to appear', icon="✅")