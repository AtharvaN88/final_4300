import streamlit as st
from geopy.geocoders import Nominatim
import json
import pandas as pd


geolocator = Nominatim(user_agent="listings-coordinates")
# replace with actual fetch calls:
file = open('sample-json/test_data.json', 'r', encoding='utf-8').read()
data = json.loads(file)

def get_map_coordindates(listing):
    address = f"{listing['address']}, {listing['city']}, {listing['state']}"
    location = geolocator.geocode(address)

    return [location.latitude, location.longitude]

coordinates = [get_map_coordindates(x) for x in data]
df_coordinates = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])

st.write('Filters')
header_col1, header_col2, header_col3 = st.columns([1,1,1])
with header_col1:
    user_city = st.selectbox(
        # TODO: make this a list of cities within Mass?
        label="Area to search",
        options=("Boston", "Revere"),
        placeholder="Location or Point of interest",
    )

with header_col2:
    user_price_range = st.slider(
        "Schedule your appointment:", value=(0, 20)
    )

# TODO? -> maybe this values are not block scoped and I can add the data loading calls after this?


col1, col2 = st.columns([2, 1])

col1.subheader("A wide column with a chart")
# TODO: pretty sure these points on the map can't be accessed making this annoying to click on
col1.map(df_coordinates)

col2.subheader("A narrow column with the data")
# TODO: custom component
col2.write('no')

# load reuse the sidebar?
# there is a built in map function to plot things on a map
# sign-in/ sign up page?