# Imports
import numpy as np
import pandas as pd
import os

# Settings frames for df
pd.set_option("display.max_columns", 85)
pd.set_option("display.max_rows", 85)


def get_raw_file_list(path_base=os.getcwd()) -> list:
    # gets all files in subsequent directories that end with LinRef.txt or LinRef.csv
    # and returns the file names as a list
    # default: curent working directory

    raw_file_list = []
    for root, d_list, f_list in os.walk(path_base):
        # print(root, d_list, f_list)
        for file in f_list:
            if file.endswith(("LinRef.txt", "LinRef.csv")):
                raw_file_list.append(os.path.join(root, file))
    return raw_file_list


def cut_to_region(csv_path: str, geo_id_dict: dict, path_base=os.getcwd()):
    # filters the dataframe from the submitted file to a region specified by
    # the german AGS ID (amtliche Gemeinde Schlüssel)

    df_raw = pd.read_csv(csv_path, delimiter=";")

    # convert the column names to lowercase letters
    df_raw.rename(columns=str.lower, inplace=True)

    year = df_raw.loc[1, "ujahr"]  # retrieve the year of the data file to later namning

    # rename columns to get a standardized df for every file
    column_dict = {"istsonstige": "istsonstig", "strzustand": "ustrzustand", "iststrassenzustand": "ustrzustand"}
    df_raw = df_raw.rename(column_dict, axis=1)  # renames if possible

    # filter df to region defined by AGS
    list_locid = list(geo_id_dict.keys())
    filt_location = (df_raw[list_locid[0]] == geo_id_dict[list_locid[0]]) & \
                    (df_raw[list_locid[1]] == geo_id_dict[list_locid[1]]) & \
                    (df_raw[list_locid[2]] == geo_id_dict[list_locid[2]]) & \
                    (df_raw[list_locid[3]] == geo_id_dict[list_locid[3]])

    df_location = df_raw.loc[filt_location]

    # filter df down to necessary columns
    column_list = ["objectid", "ujahr", "umonat", "ustunde", "uwochentag",
                   "ukategorie", "uart", "utyp1", "ulichtverh",
                   "istrad", "istpkw", "istfuss", "istkrad", "istgkfz",
                   "istsonstig", "ustrzustand", "linrefx", "linrefy", "xgcswgs84", "ygcswgs84"]
    df_location = df_location[column_list]

    df_location.to_csv(os.path.join(path_base, f"Unfallorte_{year}_Muenster.csv"), index=False)
    # index parameter defines if the index-column specified in read_csv is written aswell or not
    filt_bikes = (df_location["istrad"] == 1)
    df_bike = df_location.loc[filt_bikes]

    print(year)

    return df_bike


def conc_dfs(df_list: list, path_base=os.getcwd()):
    df_comb = pd.concat(df_list)
    df_comb.to_csv(os.path.join(path_base, f"Unfallorte_Muenster_comb_2.csv"), index=False)
    # df_comb.to_csv(f'/home/ubuntu/TechLabs_23/new_files/Unfallorte_Muenster_comb.csv', index=False)


def main(geo_id_dict: dict, path_base=os.getcwd()):
    # controls the whole workflow
    # if path_base is not submitted, the current working directory is used as default

    raw_file_list = get_raw_file_list(base_path)
    print(raw_file_list)

    print(geo_id_dict)
    df_list = []
    for file in raw_file_list:

        print(file)

        try:
            df_bike = cut_to_region(file, geo_id_dict, path_base)
        except:
            print(f'Error: file: {file} could not be processed')
        else:
            print(f'file: {file} was successfully processed')
            df_list.append(df_bike)

    conc_dfs(df_list, path_base)


### for users:
# change "base_path" for your directories which contains the "Unfallorte.._LinRef.csv/.txt" files
# if path_base is not submitted, the current working directory is used as default
base_path = "/home/ubuntu/TechLabs_23/Unfallorte"
base_path = "D:\\Jo_local\\Techlabs_23\\Unfallorte"

geo_id_dict = {"uland": np.int64("05"), "uregbez": np.int64("5"), "ukreis": np.int64("15"),
               "ugemeinde": np.int64("000")}

main(geo_id_dict, base_path)


def old_stuff():
    # data_dirs = [d for d in os.listdir(path_base)]
    # list_1 = [f for f in data_dirs if os.path.isdir(os.path.join(path_base, f))]
    # print(list_1)
    # print(data_dirs)

    #     # drop UIDENTSTLAE column which occurs the first time in 2021 to bring all dfs to the same dimensions
    #     try:
    #         df_raw = df_raw.drop(["uidentslae"], axis=1)
    #     except:
    #         print("column UIDENTSTLAE (uidentslae) couldn't be dropped")
    #     else:
    #         print("dropped column")

    column_list_original = ["OBJECTID", "ULAND", "UREGBEZ", "UKREIS", "UGEMEINDE",
                            "UJAHR", "UMONAT", "USTUNDE", "UWOCHENTAG",
                            "UKATEGORIE", "UART", "UTYP1", "ULICHTVERH",
                            "IstRad", "IstPKW", "IstFuss", "IstKrad", "IstGkfz",
                            "IstSonstig", "USTRZUSTAND", "LINREFX", "LINREFY", "XGCSWGS84", "YGCSWGS84"]

    # print(df_raw)
    # print(df_raw.info)
    # print(df_raw.dtypes)
    geo_ULAND = np.int64("05")
    geo_UREGBEZ = np.int64("5")
    geo_UKREIS = np.int64("15")
    geo_UGEMEINDE = np.int64("000")

    # geo_ULAND = "05"
    # geo_UREGBEZ = 5
    # geo_UKREIS = 15
    # geo_UGEMEINDE = 000

    list_locid = ["ULAND", "UREGBEZ", "UKREIS", "UGEMEINDE"]
    # df_raw[list_locid] = df_raw[list_locid].astype(str)
    # df_raw = [df_raw[col_name].astype(str) for col_name in df_raw.columns if col_name in list_locid]  # returns list, dict-comprehension?
    # print(df_raw)
    # print(df_raw["ULAND"].astype(str))

    # filter df to region
    filt_location = (df_raw["uland"] == geo_ULAND) & (df_raw["uregbez"] == geo_UREGBEZ) & (
            df_raw["ukreis"] == geo_UKREIS) & (df_raw["ugemeinde"] == geo_UGEMEINDE)

    geo_id_list = [np.int64("05"), np.int64("5"), np.int64("15"), np.int64("000")]

    # print(f'df_raw[list_locid 0] {df_raw[list_locid[0]]}')
    # print(f'list_locid 0 {list_locid[0]}')
    # print(f'geo_dict[list_locid 0] {geo_id_dict[list_locid[0]]}')

    # print(f'filt_location: {filt_location}')
    # print(f'type(filt_location: {type(filt_location)}')
    # filt_location = (df_raw["UKREIS"] == geo_UKREIS)
    df_location = df_raw.loc[filt_location]
    # print(f'df_raw.dtypes:  {df_raw.dtypes}')
    # print(f' df_location:   {df_location}')
    year = df_raw.loc[1, "UJAHR"]

    # save by AGS df_location.to_csv(f'/home/ubuntu/TechLabs_23/Unfallorte_{year}_{geo_ULAND}{geo_UREGBEZ}{
    # geo_UKREIS}{geo_UGEMEINDE}.csv', index=False)
    df_location.to_csv(f'/home/ubuntu/TechLabs_23/new_files/Unfallorte_{year}_Muenster.csv', index=False)
    # index parameter defines if the index-column specified in read_csv is written aswell or not
    filt_bikes = (df_location["istrad"] == 1)
    df_bike = df_location.loc[filt_bikes]
    # print(f'df_bike:    {df_bike}')
    # print(f'columns:    {df_bike.head()}')
    print(year)

    # print(f'df_raw[list_locid 0] {df_raw[list_locid[0]]}')
    # print(f'list_locid 0 {list_locid[0]}')
    # print(f'geo_dict[list_locid 0] {geo_id_dict[list_locid[0]]}')

    # print(f'filt_location: {filt_location}')
    # print(f'type(filt_location: {type(filt_location)}')
    # filt_location = (df_raw["UKREIS"] == geo_UKREIS)
    df_location = df_raw.loc[filt_location]
    # print(f'df_raw.dtypes:  {df_raw.dtypes}')
    # print(f' df_location:   {df_location}')

    # save by AGS df_location.to_csv(f'/home/ubuntu/TechLabs_23/Unfallorte_{year}_{geo_ULAND}{geo_UREGBEZ}{
    # geo_UKREIS}{geo_UGEMEINDE}.csv', index=False)
    # df_location.to_csv(f'/home/ubuntu/TechLabs_23/new_files/Unfallorte_{year}_Muenster.csv', index=False)
    df_location.to_csv(os.path.join(path_base, f"Unfallorte_{year}_Muenster.csv"), index=False)
    # index parameter defines if the index-column specified in read_csv is written aswell or not
    filt_bikes = (df_location["istrad"] == 1)
    df_bike = df_location.loc[filt_bikes]
    # print(f'df_bike:    {df_bike}')
    # print(f'columns:    {df_bike.head()}')
    print(year)

    ##testing

    # calling of cut_to_region() for tests
    # file = "/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2020_EPSG25832_CSV/csv/Unfallorte2020_LinRef.csv"
    #
    # file_list = ['/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2020_EPSG25832_CSV/csv/Unfallorte2020_LinRef.csv',
    #              '/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2017_EPSG25832_CSV/csv/Unfallorte2017_LinRef.txt',
    #              '/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2019_EPSG25832_CSV/csv/Unfallorte2019_LinRef.txt',
    #              '/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2016_EPSG25832_CSV/csv/Unfallorte_2016_LinRef.txt',
    #              '/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2021_EPSG25832_CSV/Unfallorte2021_LinRef.csv',
    #              '/home/ubuntu/TechLabs_23/Unfallorte/Unfallorte2018_EPSG25832_CSV/csv/Unfallorte2018_LinRef.txt']
    # file = file_list[2]
    # problems = ["2017", "1", "2016", "3", "2018", "5"]
    # cut_to_region(file, geo_id_dict, geo_id_list)


def old_stuff_date_states():
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
        hour = 0
        weather.add(weather_data["hourly"]["weathercode"][hour])

        if hour == 0:
            print("midnight")
            # get yesterday's date for new request yesterday = datetime.datetime.now() - datetime.timedelta(1)  #
            # alternative version for timespan. Will be useful for the historical weather mapping

            yesterday = datetime.date.today()  # use datetime.date object to evade the problem with leading zeros in
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
        weather_cond = 0
        if weather.intersection(ww_wet):
            weather_cond = 1
        if weather.intersection(ww_freezing):
            weather_cond = 2

        return weather_cond

    def filter_by_weather(df_raw: pd.DataFrame, weather_cond: int):

        filt_weather = (df_raw["USTRZUSTAND"] == weather_cond)  # filter for weather conditions
        df_weather = df_raw.loc[filt_weather]  # apply filter

        df_weather.to_csv(f'..\\Unfallorte_Muenster_Wetter_{weather_cond}.csv',
                          index=False)  # write fitlered df to new file

    df_raw = pd.read_csv('Unfallorte_Muenster_comb.csv', encoding='ISO-8859-1', delimiter=",")  # get df
    weather_condition = get_weather_data()
    filter_by_weather(df_raw, weather_condition)

    def filter_by_time(df: pd.DataFrame, time_unit_list: list):
        # get time units (month, hour, e.g.)
        today = datetime.datetime.now()
        year = today.year
        month = today.month
        day = today.day  # no use for this
        weekday = today.weekday()
        hour = today.hour

        # map weekdays to standard of Unfallatlas since they start with 1 on sunday opposite to open-meteo 0 on monday
        weekday_dict = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}
        weekday = weekday_dict[weekday]

        time_unit_dict = {"ustunde": hour, "uwochentag": weekday, "umonat": month, "ujahr": year}  # mapped column name
        # of dict to variable
        time_unit_dict_main = {k: time_unit_dict[k] for k in time_unit_list}  # create subset of time_unit_dict of
        # required time units (month, hour, e.g.) based on time_unit_list

        for key in time_unit_dict_main.keys():
            filt_time = (df[key] == time_unit_dict_main[key])
            df = df.loc[filt_time]  # apply filter

        df.to_csv(f'..\\Unfallorte_Muenster_Zeit.csv',
                  index=False)  # write filtered df to new file

    # df_raw = pd.read_csv('Unfallorte_Muenster_comb.csv', encoding='ISO-8859-1', delimiter=",")  # get df
    # time_unit_list = ["UMONAT", "USTUNDE"]
    # filter_by_time(df_raw, time_unit_list)

    ### extend request for additional data
    # could extend weather_params to retrieve additional data
    # "hourly": ["temperature_2m", "rain", "showers", "weathercode"]
    # retrieve information from additional data
    # print(weather_data["hourly"]["showers"])
    # temperature = weather_data["hourly"]["temperature_2m"][hour]
    # rain = weather_data["hourly"]["rain"][hour + 1]
    # showers = weather_data["hourly"]["showers"][hour + 1]
