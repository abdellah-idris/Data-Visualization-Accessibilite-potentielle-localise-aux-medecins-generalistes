from flask import Flask, render_template, request
import branca.colormap as cm
from mock import departement_apl_2015, departement_apl_2016, departement_apl_2017, departement_apl_2018

app = Flask(__name__)


# Define a color scale for the choropleth using a LinearColormap
color_scale = cm.LinearColormap(['yellow', 'red'], vmin=0, vmax=1)

@app.route('/')
def index():
    # Load the default map
    year = "2018"

    apl = departement_apl_2018
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
                'Population standardisée '+ str(int(year)-2) + ' pour la médecine générale': row[
                    'Population standardisée '+ str(int(year)-2) + ' pour la médecine générale'],
                'Weighted Average APL': row['Weighted Average APL'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)
    # print(apl_dict.keys())
    # print(apl_dict.items())
    return render_template('map.html', default_year=year, apl=apl_dict)

@app.route('/get_map', methods=['POST'])
def get_map():
    year = request.form['year']

    # Load the map based on the selected year
    if year == '2015':
        apl = departement_apl_2015
    elif year == '2016':
        apl = departement_apl_2016
    elif year == '2017':
        apl = departement_apl_2017
    elif year == '2018':
        apl = departement_apl_2018
    else:
        return "Year not found"

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
                'Population standardisée '+ str(int(year)-2) + ' pour la médecine générale': row['Population standardisée '+ str(int(year)-2) + ' pour la médecine générale'],
                'Weighted Average APL': row['Weighted Average APL'],
            },
            'geometry': row['geometry'].__geo_interface__
        }
        apl_dict['features'].append(feature)

    return render_template('map.html', default_year=year, apl=apl_dict)

if __name__ == '__main__':
    app.run(debug=True)
