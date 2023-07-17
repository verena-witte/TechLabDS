# imports
import requests
import datetime
import pandas as pd


# Documentation for open-meteo api
# link: https://open-meteo.com/en/docs#hourly=temperature_2m,rain,showers,weathercode

# retrieve weather information for current date
def get_weather_data() -> int:
    # Documentation for open-meteo api
    # link: https://open-meteo.com/en/docs#hourly=temperature_2m,rain,showers,weathercode

    API_endpoint = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": "51.961563",
        "longitude": "7.628202",
        "hourly": ["weathercode"]
    }

    response = requests.get(API_endpoint, params=weather_params)

    response.raise_for_status()
    weather_data = response.json()

    hour = datetime.datetime.now().hour  # get current time and day
    weather = set([])  # create set to call set.intersection(set) later on

    weather.add(weather_data["hourly"]["weathercode"][hour])
    weather.add(weather_data["hourly"]["weathercode"][
                    hour - 1])  # CAVE: what happens if this function is called at midnight 00:00?
    # TODO: check for data at midnight (00-1)
    # requires data from the day before

    # TODO: filter weather data for relevant time frames

    # create sets of weather codes which respond to wet or freezing condition
    ww_freezing = {56, 57, 66, 67, 71, 73, 75, 77, 85, 86}
    ww_wet = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}

    # set weather_cond for wet or freezing for later filtering the df
    weather_cond = 0
    if weather.intersection(ww_wet):
        weather_cond = 1
    if weather.intersection(ww_freezing):
        weather_cond = 2

    return weather_cond


def filter_by_weather(weather_cond: int):
    df_raw = pd.read_csv('Unfallorte_Muenster_comb.csv', encoding='ISO-8859-1', delimiter=",")  # get df

    filt_weather = (df_raw["USTRZUSTAND"] == weather_cond)  # filter for weather conditions
    df_weather = df_raw.loc[filt_weather]  # apply filter

    df_weather.to_csv(f'..\\Unfallorte_Muenster_Wetter_{weather_cond}.csv',
                      index=False)  # write fitlered df to new file


weather_condition = get_weather_data()
filter_by_weather(weather_condition)


def filter_by_time(df_raw: pd.DataFrame, time_unit_list: list):
    today = datetime.datetime.now()
    print(today)
    year = today.year
    month = today.month
    day = today.day
    weekday = today.weekday()
    hour = today.hour
    print(year)
    print(f' weekday: {weekday}')
    print(month)
    print(hour)

    # map weekdays to standard of Unfallatlas since they start with 1 on sunday opposite to open-meteo 0 on monday
    weekday_dict = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}
    weekday = weekday_dict[weekday]
    print(f' weekday: {weekday}')

    today_weather_format = f"{year}-{month}-{day}T{hour}:00"
    print(today_weather_format)

    for time_unit in time_unit_list:
        if time_unit == "hour":
            filt_time = (df_raw["USTUNDE"] == hour)
            df_time = df_raw.loc[filt_time]  # apply filter
        if time_unit == "weekday":
            filt_time = (df_raw["UWOCHENTAG"] == weekday)
            df_time = df_raw.loc[filt_time]  # apply filter
        if time_unit == "month":
            filt_time = (df_raw["UMONAT"] == month)
            df_time = df_raw.loc[filt_time]  # apply filter
        if time_unit == "year":
            filt_time = (df_raw["UJAHR"] == year)
            df_time = df_raw.loc[filt_time]  # apply filter

    # or solve this via a dict?
    # TODO: check where to get the actual time values (in the dict as keys) from
    time_unit_dict = {hour: "USTUNDE", weekday: "UWOCHENTAG", month: "UMONAT", year: "UJAHR"}
    time_unit_dict_main = {k: time_unit_dict[k] for k in time_unit_list}
    for key in time_unit_dict_main.keys():
        filt_time = (df_raw[time_unit_dict_main[key]] == key)
        df_time = df_raw.loc[filt_time]  # apply filter

### extend request for additional data
# could extend weather_params to retrieve additional data
# "hourly": ["temperature_2m", "rain", "showers", "weathercode"]
# retrieve information from additional data
# print(weather_data["hourly"]["showers"])
# temperature = weather_data["hourly"]["temperature_2m"][hour]
# rain = weather_data["hourly"]["rain"][hour + 1]
# showers = weather_data["hourly"]["showers"][hour + 1]
