from geopy.geocoders import Nominatim
import json
import pandas as pd
import pydeck
import base64
import streamlit as st


@st.cache_data
def get_df_values():
    # TODO: replace this with the database calls to load in the data
    # TODO: idk, but maybe caching could be a little buggy with a deployed instance?
    file = open('sample-json/test_data.json', 'r', encoding='utf-8').read()
    geolocator = Nominatim(user_agent="listings-coordinates")
    data = json.loads(file)

    df = pd.json_normalize(data)
    def get_map_coordindates(listing):
        address = f"{listing['address']}, {listing['city']}, {listing['state']}"

        # TODO: this geocode lowkey sucks sometimes and can block requests
        location = geolocator.geocode(address)
        return [location.latitude, location.longitude]

    coords = df.apply(lambda row: get_map_coordindates(row), axis=1)
    df[['Latitude', 'Longitude']] = pd.DataFrame(coords.tolist(), index=df.index)

    return df

def get_starting_position(df):
    avg_lat = df['Latitude'].mean()
    avg_long = df['Longitude'].mean()
    return avg_lat, avg_long

df = get_df_values()
start_lat, start_long = get_starting_position(df)

point_layer = pydeck.Layer(
    'ScatterplotLayer',
    data=df,
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


st.header("Available Apartments")

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
    
