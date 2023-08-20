# imports
import os

import requests
import datetime
import pandas as pd


# Documentation for open-meteo api
# link: https://open-meteo.com/en/docs#hourly=temperature_2m,rain,showers,weathercode

# retrieve weather information for current date
def get_weather_data() -> int:
    # Documentation for open-meteo api
    # link: https://open-meteo.com/en/docs#hourly=temperature_2m,rain,showers,weathercode

    api_endpoint = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": "51.961563",
        "longitude": "7.628202",
        "hourly": ["weathercode"]
    }

    response = requests.get(api_endpoint, params=weather_params)

    response.raise_for_status()
    weather_data = response.json()

    hour = datetime.datetime.now().hour  # get current time and day
    weather = set([])  # create set to call set.intersection(set) later on

    # TODO: remove line below, just for testing
    hour = 0

    weather.add(weather_data["hourly"]["weathercode"][hour])

    if hour == 0:
        print("midnight")
        # get yesterday's date for new request yesterday = datetime.datetime.now() - datetime.timedelta(1)  #
        # alternative version for timespan. Will be useful for the historical weather mapping

        yesterday = datetime.date.today() - datetime.timedelta(
            1)  # use datetime.date object to evade the problem with leading zeros in
        # integers
        print(yesterday)
        # get new request for yesterday's weather
        api_endpoint_yesterday = "https://archive-api.open-meteo.com/v1/archive"
        weather_params_yesterday = {
            "latitude": "51.961563",
            "longitude": "7.628202",
            "start_date": yesterday,
            "end_date": yesterday,
            "hourly": ["weathercode"]
        }

        response_yesterday = requests.get(api_endpoint_yesterday, params=weather_params_yesterday)

        response_yesterday.raise_for_status()
        weather_data_yesterday = response_yesterday.json()

        # TODO: check why the weather data of yesterday just returns "None"
        print(weather_data_yesterday)

        weather.add(weather_data_yesterday["hourly"]["weathercode"][
                        hour - 1])
    else:
        weather.add(weather_data["hourly"]["weathercode"][hour - 1])

    # requires data from the day before
    print(weather)
    # TODO: filter weather data for relevant time frames

    # create sets of weather codes which respond to wet or freezing condition
    ww_freezing = {56, 57, 66, 67, 71, 73, 75, 77, 85, 86}
    ww_wet = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}

    # set weather_cond for wet or freezing for later filtering the df
    # CAVE: the condition of freezing gets prioritized over wet right now
    # TODO: check priorization of freezing over wet
    weather_cond = 0
    if weather.intersection(ww_wet):
        weather_cond = 1
    if weather.intersection(ww_freezing):
        weather_cond = 2

    return weather_cond


def filter_by_weather(df_raw: pd.DataFrame, path_base, weather_cond: int):
    filt_weather = (df_raw["ustrzustand"] == weather_cond)  # create filter for weather conditions
    df_weather = df_raw.loc[filt_weather]  # apply filter
    df_weather.to_csv(os.path.join(path_base, f"Unfallorte_Muenster_Wetter_{weather_cond}.csv"), index=False)


def filter_by_time(df: pd.DataFrame, path_base, time_unit_list: list):
    # get time units (month, hour, e.g.)
    today = datetime.datetime.now()
    month = today.month
    day = today.day  # no use for this since the data contains no int for day
    hour = today.hour

    weekday = today.weekday()
    # map weekdays to standard of Unfallatlas since they start with 1 on sunday opposite to open-meteo 0 on monday
    weekday_dict = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}
    weekday = weekday_dict[weekday]

    time_unit_dict = {"ustunde": hour, "uwochentag": weekday, "umonat": month}  # mapped column name
    # of dict to variable
    time_unit_dict_main = {k: time_unit_dict[k] for k in time_unit_list}  # create subset of time_unit_dict of
    # required time units (month, hour, e.g.) based on time_unit_list

    for key in time_unit_dict_main.keys():
        filt_time = (df[key] == time_unit_dict_main[key])
        df = df.loc[filt_time]  # apply filter

    df.to_csv(os.path.join(path_base, "Unfallorte_Muenster_Zeit.csv"), index=False)
    print()


def main(time_unit_list: list, path_base=os.getcwd(), ):
    df_raw = pd.read_csv(os.path.join(path_base, "Unfallorte_Muenster_comb.csv"))

    weather_condition = get_weather_data()
    filter_by_weather(df_raw, path_base, weather_condition)

    filter_by_time(df_raw, path_base, time_unit_list)


path_base = "/home/ubuntu/TechLabs_23/Unfallorte"
path_base = "D:\\Jo_local\\Techlabs_23\\Unfallorte"
time_unit_list = ["umonat"]  # change this for your time-criteria you wish to filter for

main(time_unit_list, path_base)
