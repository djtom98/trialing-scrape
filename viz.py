# visualization.py
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely.geometry import Point
import pandas as pd

def create_folium_map(df, spain_geojson):
    m = folium.Map(location=[40, -4], zoom_start=6, tiles='cartodbpositron')

    # Add choropleth layer to the map
    folium.Choropleth(
        geo_data=spain_geojson,
        data=df,
        columns=['NAME_1', 'PointCount'],
        key_on='feature.properties.NAME_1',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Trial Count',
    ).add_to(m)

    # Add labels
    x = folium.GeoJson(
        spain_geojson.merge(df, on='NAME_1'),
        name='Clinical Trials in Spain',
        style_function=lambda x: {
            'fillColor': 'lightblue',
            'color': None,
            'weight': 1,
            'fillOpacity': 0
        },
        highlight_function=None,
    ).add_to(m)
    
    # Add GeoJsonTooltip for labels
    x.add_child(folium.features.GeoJsonTooltip(['NAME_1', 'PointCount'], labels=False))
    folium.LayerControl().add_to(m)
    
    return m

def create_geopandas_dataframe(df2):
    gdf_points = gpd.GeoDataFrame(
        df2,
        geometry='coords',
        crs='EPSG:4326'
    )
    return gdf_points
