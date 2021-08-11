import streamlit as st
import folium 
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
from .utils import *

# st.set_page_config(layout="wide")

def app():
    german_geo = f"georef-germany-kreis/georef-germany-kreis.geojson"
    gdf = gpd.read_file(german_geo)

    m=folium.Map(location=[51.16,10.45], tiles="CartoDB positron", name="Test Map",
                attr="My Data attribution",
                no_touch=True,
                zoom_start=6,
                zoom_control=True,
                scrollWheelZoom=False,
                dragging=True,
                control_scale=True)

    df = pd.read_csv("data/pred_output_full.csv")
    df['ags5'] = df['ags5'].apply(fix_ags5) #convert to match geojson
    merged = pd.merge(df, gdf, left_on='ags5', right_on='krs_code')

    choices = list(df.columns)[4:]
    choice_selected = st.selectbox("Select Column to Visualize", choices)

    folium.Choropleth(
        geo_data=german_geo,
        name="choropleth",
        data=df,
        columns=["ags5", choice_selected],
        key_on="feature.properties.krs_code",
        fill_color="YlOrRd",
        fill_opactity=.05,
        legend_name=choice_selected
    ).add_to(m)
    
    # style_function = lambda x: {'fillColor': '#ffffff'}
    # style_function = lambda x: {'fillColor': '#0000ff' if
    #                     x['properties']['name']=='Alabama' else
    #                     '#00ff00'}
    folium.features.GeoJson(data=(open(merged, "r", encoding="utf-8-sig")).read(),
                            name="States", 
                            # style_function=style_function,
                            popup=folium.GeoJsonPopup(fields=["krs_name_short"])).add_to(m)

    folium_static(m, width=1600, height=950)



    # url = (
    #     "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    # )
    # state_geo = f"{url}/us-states.json"
    # state_unemployment = f"{url}/US_Unemployment_Oct2012.csv"
    # state_data = pd.read_csv(state_unemployment)

    # m = folium.Map(location=[48, -102], zoom_start=3)

    # folium.Choropleth(
    #     geo_data=state_geo,
    #     name="choropleth",
    #     data=state_data,
    #     columns=["State", "Unemployment"],
    #     key_on="feature.id",
    #     fill_color="YlGn",
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name="Unemployment Rate (%)",
    # ).add_to(m)

    # folium.LayerControl().add_to(m)
    # folium_static(m, width=1600, height=950)