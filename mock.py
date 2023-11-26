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
    apl = apl.groupby('arrondissement').agg({
        'Weighted APL': 'sum',
        'Population standardisée ' + year + ' pour la médecine générale': 'sum'
    }).reset_index()

    apl['Weighted Average APL'] = apl['Weighted APL'] / apl[
        'Population standardisée ' + year + ' pour la médecine générale']
    return apl


def merge_to_get_coordinate(apl):
    return france_regions.merge(apl, on='nom_departement')


def merge_paris_geo(geo, paris_data):
    return pd.merge(paris_data, geo, on='Code commune INSEE')


def get_cdp():
    cdp = pd.read_csv(r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project'
                      r'\ressources\communes-departement-region_geo.csv')
    cdp = cdp.rename(columns={'code_commune_INSEE': 'Code commune INSEE'})
    cdp['Code commune INSEE'] = pd.to_numeric(cdp['Code commune INSEE'], errors='coerce')
    return cdp


def get_paris_data(apl):
    return apl[(apl['Code commune INSEE'] > 75000) & (apl['Code commune INSEE'] < 76000)]


def get_yveline_data(apl, year):
    apl = apl[(apl['nom_departement'] == 'Yvelines')]
    # Calculate the weighted APL for each commune
    apl['Weighted APL'] = apl['APL aux médecins généralistes'] * apl[
        'Population standardisée ' + year + ' pour la médecine générale']

    # Group by department and calculate the weighted average APL
    apl = apl.groupby('nom_commune').agg({
        'Weighted APL': 'sum',
        'Population standardisée ' + year + ' pour la médecine générale': 'sum'
    }).reset_index()

    apl['Weighted Average APL'] = apl['Weighted APL'] / apl[
        'Population standardisée ' + year + ' pour la médecine générale']

    return apl


def get_departement_nord_data(apl, year):
    apl = apl[(apl['nom_departement'] == 'Nord')]
    # Calculate the weighted APL for each commune
    # apl['Weighted APL'] = apl['APL aux médecins généralistes'] * apl[
    #     'Population standardisée ' + year + ' pour la médecine générale']
    # print(apl.shape)
    #
    # # Group by department and calculate the weighted average APL
    # apl = apl.groupby('nom_departement').agg({
    #     'Weighted APL': 'sum',
    #     'Population standardisée ' + year + ' pour la médecine générale': 'sum'
    # }).reset_index()
    #
    # apl['Weighted Average APL'] = apl['Weighted APL'] / apl[
    #     'Population standardisée ' + year + ' pour la médecine générale']
    #
    # print(apl.shape)

    return apl


def get_arrondissement():
    arrondissement = pd.read_csv(
        r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\project\ressources\arrondissement_2022.csv')
    arrondissement = arrondissement[['DEP', 'ARR', 'NCCENR']]
    arrondissement = arrondissement.rename(columns={'ARR': 'insee'})
    arrondissement['insee'] = pd.to_numeric(arrondissement['insee'], errors='coerce')

    arrondissement = arrondissement.rename(columns={'NCCENR': 'arrondissement'})

    return arrondissement


arrondissement_df = get_arrondissement()
print(arrondissement_df.shape)

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

# merge with arrondissement
apl_2015 = merge_arrondissement(apl_2015, arrondissement_df)
apl_2016 = merge_arrondissement(apl_2016, arrondissement_df)
apl_2017 = merge_arrondissement(apl_2017, arrondissement_df)
apl_2018 = merge_arrondissement(apl_2018, arrondissement_df)
apl_2019 = merge_arrondissement(apl_2019, arrondissement_df)
apl_2021 = merge_arrondissement(apl_2021, arrondissement_df)

paris_df_2015 = get_paris_data(apl_2015)
paris_df_2016 = get_paris_data(apl_2016)
paris_df_2017 = get_paris_data(apl_2017)
paris_df_2018 = get_paris_data(apl_2018)
paris_df_2019 = get_paris_data(apl_2019)
paris_df_2021 = get_paris_data(apl_2021)

# todo : get the department data before merging
yveline_df_2015 = get_yveline_data(apl_2015, '2013')

nord_df_2015 = get_departement_nord_data(apl_2015, '2013')


arrondissement_apl_2015 = group_by_arrondissement(apl_2015, '2013')
arrondissement_apl_2016 = group_by_arrondissement(apl_2016, '2014')
arrondissement_apl_2017 = group_by_arrondissement(apl_2017, '2015')
arrondissement_apl_2018 = group_by_arrondissement(apl_2018, '2016')
arrondissement_apl_2019 = group_by_arrondissement(apl_2019, '2017')
arrondissement_apl_2021 = group_by_arrondissement(apl_2021, '2019')

print(arrondissement_apl_2019.shape)
print(arrondissement_apl_2019.head())
print(arrondissement_apl_2019.tail())


exit(1)


grouped_apl_2015 = group_by_department(apl_2015, '2013')
grouped_apl_2016 = group_by_department(apl_2016, '2014')
grouped_apl_2017 = group_by_department(apl_2017, '2015')
grouped_apl_2018 = group_by_department(apl_2018, '2016')
grouped_apl_2019 = group_by_department(apl_2019, '2017')
grouped_apl_2021 = group_by_department(apl_2021, '2019')

# Load the GeoJSON file with France's regions
france_regions = gpd.read_file(
    "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/france.geojson")
france_regions = france_regions.rename(columns={'nom': 'nom_departement'})
# print("france region")
# print(france_regions.columns)
# print(france_regions.head())


# Load the GeoJSON file with France's regions
paris_gpd = gpd.read_file(r"C:\Users\idris\OneDrive\Documents\Study\M2\data "
                          r"vis\project\ressources\paris-arrondissements.geojson")
paris_gpd = paris_gpd.rename(columns={'c_arinsee': 'Code commune INSEE'})
columns_to_keep = ['Code commune INSEE', 'geometry']
paris_gpd = paris_gpd[columns_to_keep]

# print('PARIS GPD')
# print(paris_gpd.columns)
# print(paris_gpd.head())

department_apl_2015 = merge_to_get_coordinate(grouped_apl_2015)
department_apl_2016 = merge_to_get_coordinate(grouped_apl_2016)
department_apl_2017 = merge_to_get_coordinate(grouped_apl_2017)
department_apl_2018 = merge_to_get_coordinate(grouped_apl_2018)
department_apl_2019 = merge_to_get_coordinate(grouped_apl_2019)
department_apl_2021 = merge_to_get_coordinate(grouped_apl_2021)

# print("department apl")
# print(department_apl_2021.columns)
# print(department_apl_2021.head())


paris_geo_2015 = merge_paris_geo(paris_gpd, paris_df_2015)
paris_geo_2016 = merge_paris_geo(paris_gpd, paris_df_2016)
paris_geo_2017 = merge_paris_geo(paris_gpd, paris_df_2017)
paris_geo_2018 = merge_paris_geo(paris_gpd, paris_df_2018)
paris_geo_2019 = merge_paris_geo(paris_gpd, paris_df_2019)
paris_geo_2021 = merge_paris_geo(paris_gpd, paris_df_2021)

# print("PARIS GEO")
# print(paris_geo_2021.columns)
# print(paris_geo_2021.head())
