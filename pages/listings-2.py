from geopy.geocoders import Nominatim
import json
import pandas as pd
import pydeck
import base64
import streamlit as st
import mysql.connector

db_config = {
    "host": "final-project-rds.c6xqceq2g4jn.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "password",
    "database": "ProjectDB",
    "port": 3306
}

# @st.cache_data
def get_df_values():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query data
    query = "SELECT * FROM listings"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Convert rows directly into a DataFrame
    df = pd.DataFrame(rows)

    df['appliances'] = df['appliances'].apply(lambda x: json.loads(x) if x else [])
    df['images'] = df['images'].apply(lambda x: json.loads(x) if x else [])

    df['seller'] = df.apply(lambda row: {'name': row['seller_name'], 'contact': row['seller_contact']}, axis=1)
    df = df.drop(columns=['seller_name', 'seller_contact'])

    geolocator = Nominatim(user_agent="listings-coordinates")
    
    def get_map_coordinates(listing):
        address = f"{listing['address']}, {listing['city']}, {listing['state']}"
        location = geolocator.geocode(address)
        return [location.latitude, location.longitude] if location else [None, None]

    coords = df.apply(lambda row: get_map_coordinates(row), axis=1)
    df[['Latitude', 'Longitude']] = pd.DataFrame(coords.tolist(), index=df.index)

    return df


def get_starting_position(df):
    avg_lat = df['Latitude'].mean()
    avg_long = df['Longitude'].mean()
    return avg_lat, avg_long

df = get_df_values()
start_lat, start_long = get_starting_position(df)
areas = ["All Cities"] + df["city"].unique().tolist()
min_range = df['rent'].min()
max_range = df['rent'].max()
max_beds = df['bedrooms'].max()

st.header("Available Apartments")

st.write('Filters')
header_col1, header_col2, header_col3 = st.columns([1,1,1])
with header_col1:
    user_city = st.selectbox(
        # TODO: make this a list of cities within Mass?
        label="Area to search",
        index=0,
        options=areas,
        placeholder="Location or Point of interest",
    )

with header_col2:
    user_price_range = st.slider(
        label="Price range",
        value=max_range,
        min_value=min_range,
        max_value=max_range
    )

with header_col3:
    user_bedrooms = st.number_input("Max Bedrooms",
    value=max_beds,
    max_value=9)


filtered_df = df[
    (df["city"] == user_city if user_city != "All Cities" else True)
    & (df["rent"] <= user_price_range)
    & (df["bedrooms"] <= user_bedrooms)
]

point_layer = pydeck.Layer(
    'ScatterplotLayer',
    data=filtered_df,
    id='apartments',
    get_position=['Longitude', 'Latitude'],
    pickable=True,
    auto_highlight=True,
    get_color='[200, 30, 0, 160]',
    get_radius=500
)

view_state = pydeck.ViewState(
    latitude=start_lat, longitude=start_long, controller=True, zoom=11, pitch=50
)

tooltip = {
    "html": "<b>${rent}</b><br>{bedrooms} Bed(s) {bathrooms} Bath(s)<br>{address}, {city}, {state}",
    "style": {"color": "white"}
}

chart= pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip=tooltip
)

event = st.pydeck_chart(chart, on_select="rerun", selection_mode='single-object')

if event and event.selection.objects:
    apartment = event.selection.objects['apartments'][0]

    st.markdown("## Apartment Listing Details")

    if apartment.get('images'):
        first_image = apartment['images'][0]
        st.image(base64.b64decode(first_image), use_container_width=True)
    else:
        st.write('No Images Available')

    st.subheader(f"{apartment['rent']} / month")

    st.markdown("### Location")
    st.write(f"{apartment['address']}, {apartment['city']}, {apartment['state']} {apartment['zip']}")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Bedrooms:** {apartment['bedrooms']}")
    with col2:
        st.write(f"**Bathrooms:** {apartment['bathrooms']}")

    if apartment.get("appliances"):
        st.markdown("###  Features")
        st.markdown(
            "\n".join([f"- {appliance}" for appliance in apartment['appliances']])
        )

    st.markdown("### Contact")
    st.write(f"**Name:** {apartment.get('seller.name', 'N/A')}")
    st.write(f"**Phone:** {apartment.get('seller.contact', 'N/A')}")

    if apartment.get('images'):
        st.markdown("Images")
        image_cols = st.columns(3)
        for idx, img_data in enumerate(apartment['images']):
            with image_cols[idx % 3]:
                st.image(base64.b64decode(img_data), use_container_width=True)

    

# Button to clear/reset the DataFrame
if st.button("Clear DataFrame"):
    # Establish MySQL connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # SQL query to delete all records from the listings table
    query = "DELETE FROM listings"

    # Execute the query
    cursor.execute(query)
    conn.commit()  # Commit the transaction to the database
    st.success("Database records cleared successfully!")
    cursor.close()
    conn.close()

    # Reset the local DataFrame
    df = pd.DataFrame()  # Clear the DataFrame

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Query to fetch all records from the listings table
cursor.execute("SELECT * FROM listings")
rows = cursor.fetchall()

# Convert rows to DataFrame for display
df_display = pd.DataFrame(rows)

# Close the cursor and the connection
cursor.close()
conn.close()

st.markdown("### Current Listings in Database")
st.dataframe(pd.DataFrame(rows)) 
