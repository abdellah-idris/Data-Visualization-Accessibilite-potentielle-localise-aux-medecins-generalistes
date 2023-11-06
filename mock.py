import pandas as pd
import geopandas as gpd


def read_apl_csv(year):
    apl = pd.read_excel(r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\apl.xlsx', sheet_name='APL_' + str(year), skiprows=8)
    apl = apl.drop(0)
    apl['Code commune INSEE'] = pd.to_numeric(apl['Code commune INSEE'], errors='coerce')
    return apl

apl_2015=read_apl_csv(2015)
apl_2016=read_apl_csv(2016)
apl_2017=read_apl_csv(2017)
apl_2018=read_apl_csv(2018)
apl_2019=read_apl_csv(2019)
apl_2021=read_apl_csv(2021)

cdp = pd.read_csv(r'C:\Users\idris\OneDrive\Documents\Study\M2\data vis\communes-departement-region.csv')
cdp = cdp.rename(columns={'code_commune_INSEE': 'Code commune INSEE'})
cdp['Code commune INSEE'] = pd.to_numeric(cdp['Code commune INSEE'], errors='coerce')

def merge_apl_cdp(apl):
    return pd.merge(apl, cdp, on='Code commune INSEE')
# join
apl_2015 = merge_apl_cdp(apl_2015)
apl_2016 = merge_apl_cdp(apl_2016)
apl_2017 = merge_apl_cdp(apl_2017)
apl_2018 = merge_apl_cdp(apl_2018)
apl_2019 = merge_apl_cdp(apl_2019)
apl_2021 = merge_apl_cdp(apl_2021)


def group_by_departement(apl, year):
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

grouped_apl_2015 = group_by_departement(apl_2015, '2013')
grouped_apl_2016 = group_by_departement(apl_2016, '2014')
grouped_apl_2017 = group_by_departement(apl_2017, '2015')
grouped_apl_2018 = group_by_departement(apl_2018, '2016')
grouped_apl_2019 = group_by_departement(apl_2019, '2017')
grouped_apl_2021 = group_by_departement(apl_2021, '2019')


# Load the GeoJSON file with France's regions
france_regions = gpd.read_file("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/france.geojson")
france_regions = france_regions.rename(columns={'nom': 'nom_departement'})

def merge_to_get_cordinate(apl):
    return france_regions.merge(apl, on='nom_departement')

departement_apl_2015 = merge_to_get_cordinate(grouped_apl_2015)
departement_apl_2016 = merge_to_get_cordinate(grouped_apl_2016)
departement_apl_2017 = merge_to_get_cordinate(grouped_apl_2017)
departement_apl_2018 = merge_to_get_cordinate(grouped_apl_2018)
departement_apl_2019 = merge_to_get_cordinate(grouped_apl_2019)
departement_apl_2021 = merge_to_get_cordinate(grouped_apl_2021)

