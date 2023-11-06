from mock import departement_apl_2018

import folium
import branca.colormap as cm
import json

def one_html_map(apl):
    # Create a folium map centered at a specific location
    m = folium.Map(location=[48, 2], zoom_start=6, tiles="OpenStreetMap")

    # Define a color scale for the choropleth using a LinearColormap
    color_scale = cm.LinearColormap(['yellow', 'red'], vmin=apl['Weighted Average APL'].min(), vmax=apl['Weighted Average APL'].max())

    def get_color(feature):
        # Map feature properties to color using the colormap
        return color_scale(feature['properties']['Weighted Average APL'])

    # Convert GeoDataFrame to a GeoJSON feature collection
    geojson_data = json.loads(apl.to_json())

    # Add a GeoJson layer to the map using the custom color scale function
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': get_color(feature),
            'color': 'transparent',
            'fillOpacity': 0.6,
        },
        highlight_function=lambda x: {'weight': 1, 'color': 'blue'},
        tooltip=folium.GeoJsonTooltip(fields=['nom_departement', 'Weighted Average APL'], labels=True, sticky=True),
    ).add_to(m)


    # Save the map to an HTML file
    m.save("./2018.html")


one_html_map(departement_apl_2018)

