import streamlit as st

# call to upload boto3 ->
# call to get data -> (think that's it lol)
# have to wait until it resolves?
# -> refresh feed button ->

def upload_obj_to_s3():
    # make a json file -> then upload that:

    pass

with st.form(key="upload_form", clear_on_submit=False):
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
    price = st.number_input("Insert a number")
    # maybe something for the ammentities (amt of bathrooms/bedrooms? -> or leave that for the upload)

    # address = st.text_input(
    #     "Enter Address"
    # )
    # address = st.text_input(
    #     "Enter Address"
    # )

    uploaded_files = st.file_uploader(
        "Upload Images", accept_multiple_files=True
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        # write the json file then upload it
        # eventual AWS calls to actually upload data
        upload_obj_to_s3()
        st.success('Listing Created, it may take some time for it to appear', icon="✅")