import os
from datetime import datetime, timedelta
import requests
import pandas as pd


def get_data(file, df):
    global today
    if(os.path.exists(file)):
        original_countries = pd.read_csv('positiveCases.csv')
        current_df = pd.read_csv(file)
        current_df[today] = pd.DataFrame(columns=[today])
        today_data = []
        yesterday = str((datetime.strptime(today,"%m-%d-%y") -timedelta(
                days=1)).strftime("%m-%d-%y"))
        for country in original_countries.iloc[:, 0]:
            if (country in list(df.loc[:, 'Country'])):
                today_data.append(int(df[df['Country'] == country][today]))
            else:
                today_data.append(current_df.loc[current_df['Country'] == country][yesterday].item())
        current_df[today] = pd.Series(today_data)
        current_df.to_csv(file, index=False)
    else:
        countries = requests.get("https://api.covid19api.com/countries").json()
        countries = sorted([i['Country'] for i in countries])
        country_df = pd.DataFrame(data=countries, columns=['Country'])
        country_df[today] = df[today]
        country_df.to_csv(file, index=False)


data = requests.get("https://api.covid19api.com/summary").json()
today = str(datetime.strptime(data['Countries'][0]['Date'][:10], "%Y-%m-%d").strftime("%m-%d-%y"))

global_data = data["Global"]
print(f"\nGlobal statistics as of {today}")
print(f"Total cases: {global_data['TotalConfirmed']}")
print(f"New cases since yesterday: {global_data['NewConfirmed']}")
print(f"Total deaths: {global_data['TotalDeaths']}")
print(f"New deaths since yesterday: {global_data['NewDeaths']}")
print(f"Total recovered: {global_data['TotalRecovered']}")
print(f"New recovered since yesterday: {global_data['NewRecovered']}")

country_df_positiveCases = pd.DataFrame(columns=['Country', today])
country_df_deaths = pd.DataFrame(columns=['Country', today])
country_df_recovered = pd.DataFrame(columns=['Country', today])

for country in data["Countries"]:
    country_df_positiveCases = country_df_positiveCases.append(
        {'Country': country['Country'], today: country['TotalConfirmed']}, ignore_index=True)
    country_df_deaths = country_df_deaths.append(
        {'Country': country['Country'], today: country['TotalDeaths']}, ignore_index=True)
    country_df_recovered = country_df_recovered.append(
        {'Country': country['Country'], today: country['TotalRecovered']}, ignore_index=True)

get_data('positiveCases.csv', country_df_positiveCases)
get_data('deaths.csv', country_df_deaths)
get_data('recovered.csv', country_df_recovered)

positiveCases_df = pd.read_csv('positiveCases.csv')
confirmed_df = positiveCases_df.sort_values(by=today, ascending=False)
countries = [positiveCases_df.iloc[i]['Country'] for i in range(5)]
recovered_df = pd.read_csv('recovered.csv')
deaths_df = pd.read_csv('deaths.csv')
