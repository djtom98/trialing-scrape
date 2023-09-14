# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: thesis
#     language: python
#     name: python3
# ---

# main.py
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
from extract import scrape_hospital_data, extract_hospital_info
from viz import create_folium_map

# Extract data
hospital_data = scrape_hospital_data()
hospital_info = [extract_hospital_info(hsp) for hsp in hospital_data]
df = pd.DataFrame(hospital_info)

# Data cleaning and processing
df.drop_duplicates(subset=['id'], keep='first', inplace=True)
df['coords'] = df['Website'].str.extract(r'(?:@)(.*)(?:,17z)')
df[['Addressline', 'City', 'Region']] = df[['Hospital Name', 'Address', 'Website']]['Address'].str.replace('Address:', '').str.split('|', expand=True)
#split region into country and region
df[[ 'Region','Country']] = df['Region'].str.split(',', expand=True)
#clean phone number
df['Phone Number'] = df['Phone Number'].str.replace('Phone:', '')

#Preparing csv for export

exportdf=df[['Hospital Name', 'Addressline', 'City', 'Region','Country','Phone Number']]
exportdf.columns=['name','address','city', 'region','country','contact data']
exportdf[['latitude','longitude']]=df['coords'].str.split(',',expand=True)
exportdf.to_csv('extract_data.csv',index=False)



spain_geojson = gpd.read_file('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/spain/spain-comunidad-with-canary-islands.json')
spain_geojson.crs = "EPSG:4326"
trialdata=pd.read_csv('hospital_trials.csv',sep=';')

#dropping trials without corresponding hospital on merge
df2=pd.merge(trialdata,df,how='inner',left_on='hospital_id',right_on='id')
df2['coords'] = df2['coords'].str.split(',').apply(lambda x: Point(float(x[1]), float(x[0])))

gdf_points = gpd.GeoDataFrame(
    df2,
    geometry='coords',
    crs='EPSG:4326' 
)

# Perform a spatial join to count points within each polygon
points_in_polygons = gpd.sjoin(gdf_points, spain_geojson, how='left', op='within')
polygon_counts = points_in_polygons.groupby('NAME_1').size().reset_index(name='PointCount')

# Visualization
m = create_folium_map(polygon_counts, spain_geojson)

# %%
# Print or display map
m.save('clinical_trials_map.html')  # Uncomment to save the map as an HTML file

