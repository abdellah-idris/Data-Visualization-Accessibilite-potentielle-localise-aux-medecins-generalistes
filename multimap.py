from mock import (department_apl_2015, department_apl_2016, department_apl_2017, department_apl_2018, department_apl_2019,
                  department_apl_2021, paris_geo_2015, paris_geo_2016, paris_geo_2017, paris_geo_2018, paris_geo_2019,
                  paris_geo_2021,
                  nord_geo_2015, nord_geo_2016, nord_geo_2017, nord_geo_2018, nord_geo_2019, nord_geo_2021,
                  pdc_geo_2015, pdc_geo_2016, pdc_geo_2017, pdc_geo_2018, pdc_geo_2019, pdc_geo_2021)
from flask import Flask, render_template, request, jsonify
import branca.colormap as cm

app = Flask(__name__)

# https://france-geojson.gregoiredavid.fr/

# Define a color scale for the choropleth using a LinearColormap
color_scale = cm.LinearColormap(['yellow', 'red'], vmin=0, vmax=1)


@app.route('/')
def index():
    # Load the default map for a selected year
    year = "2015"  # Default year
    apl = department_apl_2015  # Default data

    # Prepare the data as a GeoJSON FeatureCollection
    apl_dict = {
        'type': 'FeatureCollection',
        'features': []
    }

    for index, row in apl.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'code': row['code'],
                'nom_departement': row['nom_departement'],
                'Weighted APL': row['Weighted APL'],
                'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale'],
                'Weighted Average APL': row['Weighted Average APL'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return render_template('map.html', selected_year=year, apl_data=jsonify(apl_dict))


@app.route('/get_map', methods=['POST'])
def get_map():
    apl = None
    if request.method == 'POST':
        year = request.form.get('year')
    else:
        year = "2015"  # Default year

    # Load data based on the selected year
    if year == '2015':
        apl = department_apl_2015
    elif year == '2016':
        apl = department_apl_2016
    elif year == '2017':
        apl = department_apl_2017
    elif year == '2018':
        apl = department_apl_2018
    elif year == '2019':
        apl = department_apl_2019
    elif year == '2021':
        apl = department_apl_2021

    apl_dict = {
        'type': 'FeatureCollection',
        'features': []
    }

    for index, row in apl.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'code': row['code'],
                'nom': row['nom_departement'],
                'Weighted APL': row['Weighted APL'],
                'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale'],
                'Weighted Average APL': row['Weighted Average APL'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return jsonify(apl_dict)  # Return JSON data to update the map


@app.route('/get_paris_data', methods=['POST'])
def get_paris_data():
    apl = None
    if request.method == 'POST':
        year = request.form.get('year')
    else:
        year = "2015"  # Default year

    # Load data based on the selected year
    if year == '2015':
        apl = paris_geo_2015
    elif year == '2016':
        apl = paris_geo_2016
    elif year == '2017':
        apl = paris_geo_2017
    elif year == '2018':
        apl = paris_geo_2018
    elif year == '2019':
        apl = paris_geo_2019
    elif year == '2021':
        apl = paris_geo_2021

    apl_dict = {
        'type': 'FeatureCollection',
        'features': []
    }

    for index, row in apl.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'code': row['Code commune INSEE'],
                'nom': row['nom_commune'],
                'Weighted Average APL': row['APL aux médecins généralistes'],
                'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return jsonify(apl_dict)

@app.route('/get_nord_data', methods=['POST'])
def get_nord_data():
    apl = None
    if request.method == 'POST':
        year = request.form.get('year')
    else:
        year = "2015"  # Default year

    # Load data based on the selected year
    if year == '2015':
        apl = nord_geo_2015
    elif year == '2016':
        apl = nord_geo_2016
    elif year == '2017':
        apl = nord_geo_2017
    elif year == '2018':
        apl = nord_geo_2018
    elif year == '2019':
        apl = nord_geo_2019
    elif year == '2021':
        apl = nord_geo_2021

    apl_dict = {
        'type': 'FeatureCollection',
        'features': []
    }

    for index, row in apl.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'code': row['Code commune INSEE'],
                'nom': row['nom_commune'],
                'Weighted Average APL': row['APL aux médecins généralistes'],
                'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return (jsonify(apl_dict))



@app.route('/get_pdc_data', methods=['POST'])
def get_pdc_data():
    apl = None
    if request.method == 'POST':
        year = request.form.get('year')
    else:
        year = "2015"  # Default year

    # Load data based on the selected year
    if year == '2015':
        apl = pdc_geo_2015
    elif year == '2016':
        apl = pdc_geo_2016
    elif year == '2017':
        apl = pdc_geo_2017
    elif year == '2018':
        apl = pdc_geo_2018
    elif year == '2019':
        apl = pdc_geo_2019
    elif year == '2021':
        apl = pdc_geo_2021

    apl_dict = {
        'type': 'FeatureCollection',
        'features': []
    }

    for index, row in apl.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'code': row['Code commune INSEE'],
                'nom': row['nom_commune'],
                'Weighted Average APL': row['APL aux médecins généralistes'],
                'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée ' + str(int(year)-2) + ' pour la médecine générale'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return jsonify(apl_dict)


if __name__ == '__main__':
    app.run(debug=True)
