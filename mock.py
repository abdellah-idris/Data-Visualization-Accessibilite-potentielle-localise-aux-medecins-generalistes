import pandas as pd
import geopandas as gpd


def read_apl_csv(year):
    apl = pd.read_excel(r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\apl.xlsx', sheet_name='APL_' + str(year),
                        skiprows=8)
    apl = apl.drop(0)
    apl['Code commune INSEE'] = pd.to_numeric(apl['Code commune INSEE'], errors='coerce')
    return apl


def merge_apl_cdp(apl, cdp_param):
    apl = pd.merge(apl, cdp_param, on='Code commune INSEE')
    apl['code_departement'] = pd.to_numeric(apl['code_departement'], errors='coerce')
    apl['insee'] = apl['Code commune INSEE'] / 100
    apl['insee'] = pd.to_numeric(apl['insee'], errors='coerce')
    return apl


def merge_arrondissement(apl, arrondissement):
    return pd.merge(apl, arrondissement, on='insee')


def group_by_department(apl, year):
    # Calculate the weighted APL for each commune
    apl['Weighted APL'] = apl['APL aux médecins généralistes'] * apl[
        'Population standardisée ' + year + ' pour la médecine générale']

    # Group by department and calculate the weighted average APL
    apl = apl.groupby('nom_departement').agg({
        'Weighted APL': 'sum',
        'Population standardisée ' + year + ' pour la médecine générale': 'sum'
    }).reset_index()

    apl['Weighted Average APL'] = apl['Weighted APL'] / apl[
        'Population standardisée ' + year + ' pour la médecine générale']
    return apl


def group_by_arrondissement(apl, year):
    # Calculate the weighted APL for each commune
    apl['Weighted APL'] = apl['APL aux médecins généralistes'] * apl[
        'Population standardisée ' + year + ' pour la médecine générale']

    # Group by department and calculate the weighted average APL
    apl = apl.groupby(['nom_departement','arrondissement']).agg({
        'Weighted APL': 'sum',
        'Population standardisée ' + year + ' pour la médecine générale': 'sum',
    }).reset_index()

    apl['Weighted Average APL'] = apl['Weighted APL'] / apl[
        'Population standardisée ' + year + ' pour la médecine générale']
    return apl


def merge_to_get_coordinate(apl):
    # Load the GeoJSON file with France's regions
    france_regions = gpd.read_file(
        "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/france.geojson")
    france_regions = france_regions.rename(columns={'nom': 'nom_departement'})
    return france_regions.merge(apl, on='nom_departement')


def merge_paris_geo(geo, paris_data):
    return pd.merge(paris_data, geo, on='Code commune INSEE')
def merge_geo(geo, data):
    return pd.merge(data, geo, on='Code commune INSEE')


def get_cdp():
    cdp = pd.read_csv(r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project'
                      r'\ressources\communes-departement-region_geo.csv')
    cdp = cdp.rename(columns={'code_commune_INSEE': 'Code commune INSEE'})
    cdp['Code commune INSEE'] = pd.to_numeric(cdp['Code commune INSEE'], errors='coerce')
    return cdp


def get_paris_data(apl):
    return apl[(apl['Code commune INSEE'] > 75000) & (apl['Code commune INSEE'] < 76000)]


def get_departement_data(apl, year, departement):
    apl = apl[(apl['nom_departement'] == departement)]

    return apl


def get_arrondissement():
    arrondissement = pd.read_csv(
        r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project\ressources\arrondissement_2022.csv')
    arrondissement = arrondissement[['DEP', 'ARR', 'NCCENR']]
    arrondissement = arrondissement.rename(columns={'ARR': 'insee'})
    arrondissement['insee'] = pd.to_numeric(arrondissement['insee'], errors='coerce')

    arrondissement = arrondissement.rename(columns={'NCCENR': 'arrondissement'})

    return arrondissement

def get_paris_gpd():
    # Load the GeoJSON file with France's regions
    paris_gpd = gpd.read_file(r"C:\Users\idris\OneDrive\Documents\Study\M2\data "
                              r"vis\project\ressources\paris-arrondissements.geojson")
    paris_gpd = paris_gpd.rename(columns={'c_arinsee': 'Code commune INSEE'})
    columns_to_keep = ['Code commune INSEE', 'geometry']
    paris_gpd = paris_gpd[columns_to_keep]
    return paris_gpd

def get_geo(file_name):
        # Load the GeoJSON file with France's regions
        geo_coordinate = gpd.read_file(file_name)
        print(f"geo coordinate columns {geo_coordinate.columns}")
        geo_coordinate = geo_coordinate.rename(columns={'code': 'Code commune INSEE'})
        columns_to_keep = ['Code commune INSEE', 'geometry']
        geo_coordinate = geo_coordinate[columns_to_keep]
        geo_coordinate['Code commune INSEE'] = pd.to_numeric(geo_coordinate['Code commune INSEE'], errors='coerce')

        return geo_coordinate

apl_2015 = read_apl_csv(2015)
apl_2016 = read_apl_csv(2016)
apl_2017 = read_apl_csv(2017)
apl_2018 = read_apl_csv(2018)
apl_2019 = read_apl_csv(2019)
apl_2021 = read_apl_csv(2021)

# commune, departement, region
cdp = get_cdp()

# join
apl_2015 = merge_apl_cdp(apl_2015, cdp)
apl_2016 = merge_apl_cdp(apl_2016, cdp)
apl_2017 = merge_apl_cdp(apl_2017, cdp)
apl_2018 = merge_apl_cdp(apl_2018, cdp)
apl_2019 = merge_apl_cdp(apl_2019, cdp)
apl_2021 = merge_apl_cdp(apl_2021, cdp)


# Paris
paris_df_2015 = get_paris_data(apl_2015)
paris_df_2016 = get_paris_data(apl_2016)
paris_df_2017 = get_paris_data(apl_2017)
paris_df_2018 = get_paris_data(apl_2018)
paris_df_2019 = get_paris_data(apl_2019)
paris_df_2021 = get_paris_data(apl_2021)
paris_gpd = get_paris_gpd()
paris_geo_2015 = merge_paris_geo(paris_gpd, paris_df_2015)
paris_geo_2016 = merge_paris_geo(paris_gpd, paris_df_2016)
paris_geo_2017 = merge_paris_geo(paris_gpd, paris_df_2017)
paris_geo_2018 = merge_paris_geo(paris_gpd, paris_df_2018)
paris_geo_2019 = merge_paris_geo(paris_gpd, paris_df_2019)
paris_geo_2021 = merge_paris_geo(paris_gpd, paris_df_2021)


# Nord
nord_df_2015 = get_departement_data(apl_2015, '2013', 'Nord')
nord_df_2016 = get_departement_data(apl_2016, '2014', 'Nord')
nord_df_2017 = get_departement_data(apl_2017, '2015', 'Nord')
nord_df_2018 = get_departement_data(apl_2018, '2016', 'Nord')
nord_df_2019 = get_departement_data(apl_2019, '2017', 'Nord')
nord_df_2021 = get_departement_data(apl_2021, '2019', 'Nord')
print(f"nord columns {nord_df_2021.columns}")
nord_geo = get_geo(r"C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project\ressources\nord.geojson")
print("geo columns" + nord_geo.columns)
nord_geo_2015 = merge_geo(nord_geo, nord_df_2015)
nord_geo_2016 = merge_geo(nord_geo, nord_df_2016)
nord_geo_2017 = merge_geo(nord_geo, nord_df_2017)
nord_geo_2018 = merge_geo(nord_geo, nord_df_2018)
nord_geo_2019 = merge_geo(nord_geo, nord_df_2019)
nord_geo_2021 = merge_geo(nord_geo, nord_df_2021)

# Pas-de-Calais
pdc_df_2015 = get_departement_data(apl_2015, '2013', 'Pas-de-Calais')
pdc_df_2016 = get_departement_data(apl_2016, '2014', 'Pas-de-Calais')
pdc_df_2017 = get_departement_data(apl_2017, '2015', 'Pas-de-Calais')
pdc_df_2018 = get_departement_data(apl_2018, '2016', 'Pas-de-Calais')
pdc_df_2019 = get_departement_data(apl_2019, '2017', 'Pas-de-Calais')
pdc_df_2021 = get_departement_data(apl_2021, '2019', 'Pas-de-Calais')
pdc_geo = get_geo(r"C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project\ressources\Pas-de-Calais.geojson")
pdc_geo_2015 = merge_geo(pdc_geo, pdc_df_2015)
pdc_geo_2016 = merge_geo(pdc_geo, pdc_df_2016)
pdc_geo_2017 = merge_geo(pdc_geo, pdc_df_2017)
pdc_geo_2018 = merge_geo(pdc_geo, pdc_df_2018)
pdc_geo_2019 = merge_geo(pdc_geo, pdc_df_2019)
pdc_geo_2021 = merge_geo(pdc_geo, pdc_df_2021)

# group by departement
grouped_apl_2015 = group_by_department(apl_2015, '2013')
grouped_apl_2016 = group_by_department(apl_2016, '2014')
grouped_apl_2017 = group_by_department(apl_2017, '2015')
grouped_apl_2018 = group_by_department(apl_2018, '2016')
grouped_apl_2019 = group_by_department(apl_2019, '2017')
grouped_apl_2021 = group_by_department(apl_2021, '2019')

# merge departement geo
department_apl_2015 = merge_to_get_coordinate(grouped_apl_2015)
department_apl_2016 = merge_to_get_coordinate(grouped_apl_2016)
department_apl_2017 = merge_to_get_coordinate(grouped_apl_2017)
department_apl_2018 = merge_to_get_coordinate(grouped_apl_2018)
department_apl_2019 = merge_to_get_coordinate(grouped_apl_2019)
department_apl_2021 = merge_to_get_coordinate(grouped_apl_2021)
