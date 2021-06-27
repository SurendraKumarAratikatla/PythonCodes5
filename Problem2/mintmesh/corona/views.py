from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def json_data():
    # dependencies
    result_dict = {}
    country_dict = {}
    world_status_dict = {}
    url = "https://www.worldometers.info/coronavirus/"
    # here headers providing for avoiding forbidden type of issues
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    # making soup to scrap data
    soup = BeautifulSoup(response.content, 'html.parser')
    # searching for pattern to march tabledata
    soup = re.sub(r'<.*?>', lambda g: g.group(0).upper(), str(soup))
    # creating dataframe by using read_html into df variable
    df = pd.read_html(soup)
    # taking 1st table
    df = df[0]
    # renaming the dataframe columns
    df = df.rename(
        columns={
            'Country,Other': 'CountryName'
        }
    )
    # taking countries data from 7 to 230 row avoiding unnecessary data
    df_country_column = df['CountryName'][7:230]
    # setting indexing and making true to save changes in df
    df.set_index('CountryName', inplace=True)
    # calculating RecoveryRate = TotalRecovered / TotalCases
    df['RecoveryRate'] = df['TotalRecovered'] / df['TotalCases']
    # filling all NaN values with 1
    df.fillna({'Population': 1}, inplace=True)
    # calculating PercentageOfPopulationInfected = TotalCases / Population * 100
    df['PercentageOfPopulationInfected'] = df['TotalCases'] / df['Population'] * 100
    # taking only necessary data
    df1 = df[['TotalCases', 'ActiveCases', 'TotalDeaths', 'RecoveryRate', 'PercentageOfPopulationInfected']][7:230]
    # filling all NaN values with 1
    df1.fillna(0, inplace=True)
    # iterating through over all countries and making final dictionary
    for country in df_country_column:
        temp_dict = {}
        if country == 'World':
            temp_dict['Total Cases'] = int(df1.loc[country].TotalCases)
            temp_dict['Active Cases'] = int(df1.loc[country].ActiveCases)
            temp_dict['Total Deaths'] = int(df1.loc[country].TotalDeaths)
            temp_dict['Recovery Rate'] = df1.loc[country].RecoveryRate
            temp_dict['Percentage of Population Infected'] = df1.loc[country].PercentageOfPopulationInfected
            world_status_dict[country] = temp_dict
        else:
            # temp_dict['Country Name'] = country
            temp_dict['Total Cases'] = int(df1.loc[country].TotalCases)
            temp_dict['Active Cases'] = int(df1.loc[country].ActiveCases)
            temp_dict['Total Deaths'] = int(df1.loc[country].TotalDeaths)
            temp_dict['Recovery Rate'] = df1.loc[country].RecoveryRate
            temp_dict['Percentage of Population Infected'] = df1.loc[country].PercentageOfPopulationInfected
            country_dict[country] = temp_dict

    result_dict["Entire World Status"] = world_status_dict
    result_dict["Individual Country Status"] = country_dict

    return result_dict

# get api view
@api_view(['GET'])
def apiCoronaView(request):
    return Response(json_data())
