import streamlit as st

st.markdown("<h1 style='text-align: center;'>Welcome to CNA Housing</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Whether you're looking to <strong>buy</strong> or <strong>sell</strong>, we've got you covered.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("I'm a Seller")
    st.write("Create and manage property listings easily.")
    st.page_link("pages/create-listing.py", label="Create a New Listing")

with col2:
    st.subheader("I'm a Buyer")
    st.write("Browse listings to find your perfect apartment.")
    st.page_link("pages/listings.py", label="View Available Listings")