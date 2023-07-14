# imports
import requests
import os
import datetime

# Documentation for open-meteo api
# link: https://open-meteo.com/en/docs#hourly=temperature_2m,rain,showers,weathercode

# TODO: retrieve weather information for current date
API_endpoint = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": "51.961563",
    "longitude": "7.628202",
    "hourly": ["temperature_2m", "rain", "showers", "weathercode"]
}

response = requests.get(API_endpoint, params=weather_params)

# url = "https://api.open-meteo.com/v1/forecast?latitude=51.961563&longitude=7.628202&hourly=temperature_2m,rain,showers,weathercode"
# response = requests.get(url)
response.raise_for_status()
weather_data = response.json()
print(weather_data)

# TODO: retrieve time data for current timepoint
today = datetime.datetime.now()

print(today)
year = today.year
month = today.month
day = today.day
weekday = today.weekday()
hour = today.hour
print(year)
print(weekday)
print(month)
print(hour)

today_weather_format = f"{year}-{month}-{day}T{hour}:00"
print(today_weather_format)

weather = weather_data["hourly"]["weathercode"][hour]
weather_minus1 = weather_data["hourly"]["weathercode"][hour-1]
# or turn weather into list?
# TODO: check for data at midnight (00-1)
print(weather)

ww_freezing = [56, 57, 66, 67, 71, 73, 75, 77, 85, 86]
ww_wet = [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]
flag_freezing = False
flag_wet = False
flag_weather_cond = 0
if weather in ww_freezing:
    flag_freezing = True
    flag_weather_cond = 0
if weather in ww_wet:
    flag_wet = True
    flag_weather_cond = 0


### extend request for additional data
# could extend weather_params to retrieve additional data
# "hourly": ["temperature_2m", "rain", "showers", "weathercode"]
# retrieve information from additional data
# print(weather_data["hourly"]["showers"])
# temperature = weather_data["hourly"]["temperature_2m"][hour]
# rain = weather_data["hourly"]["rain"][hour + 1]
# showers = weather_data["hourly"]["showers"][hour + 1]

# TODO: filter weather data for relevant time frames

# TODO: convert weather data to format used in dataframe


#
