import streamlit as st
from geopy.geocoders import Nominatim
import json
import pandas as pd
import mysql.connector


geolocator = Nominatim(user_agent="listings-coordinates")
# replace with actual fetch calls:
file = open('sample-json/test_data.json', 'r', encoding='utf-8').read()
data = json.loads(file)

db_config = {
    "host": "localhost/IP",
    "user": "username",
    "password": "password",
    "database": "db-name"
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def get_map_coordindates(listing):
    address = f"{listing['address']}, {listing['city']}, {listing['state']}"
    location = geolocator.geocode(address)

    return [location.latitude, location.longitude]


def fetch_listings_from_db():
    conn = get_db_connection()
    query = """
    SELECT 
        id, address, city, state, zip, rent, bedrooms, bathrooms, appliances, images, seller_name, seller_contact
    FROM listings;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df['appliances'] = df['appliances'].apply(lambda x: x.split(','))
    df['images'] = df['images'].apply(lambda x: x.split(','))

    df['seller'] = df.apply(lambda row: {'name': row['seller_name'], 'contact': row['seller_contact']}, axis=1)
    df = df.drop(columns=['seller_name', 'seller_contact'])

    return df

df = fetch_listings_from_db()

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