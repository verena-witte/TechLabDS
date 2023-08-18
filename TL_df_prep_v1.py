# Imports
import numpy as np
import pandas as pd
import os

# Settings frames for df
pd.set_option("display.max_columns", 85)
pd.set_option("display.max_rows", 85)

path_unfallorte = "/home/ubuntu/TechLabs_23/Unfallorte"


def get_raw_file_list(path_base: str) -> list:
    # gets all files in subsequent directories that end with LinRef.txt or LinRef.csv
    # and returns the file names as a list


    # data_dirs = [d for d in os.listdir(path_base)]
    # list_1 = [f for f in data_dirs if os.path.isdir(os.path.join(path_base, f))]
    # print(list_1)
    # print(data_dirs)
    raw_file_list = []
    for root, d_list, f_list in os.walk(path_base):
        # print(root, d_list, f_list)
        for file in f_list:
            if file.endswith(("LinRef.txt", "LinRef.csv")):
                raw_file_list.append(os.path.join(root, file))
    return raw_file_list


def cut_to_region(csv_path: str, geo_id_dict: dict, geo_id_list: list):
    # filters the dataframe from the submitted file to a region specified by
    # the german AGS ID (amtliche Gemeinde Schlüssel)

    df_raw = pd.read_csv(csv_path, delimiter=";")
    year = df_raw.loc[1, "UJAHR"]  # retrieve the year of the data
    # TODO: change UJAHR above

    # TODO: lower case conversion
    # convert the column names to lowercase letters
    # df_raw.rename(columns=str.lower, inplace=True)

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

    #     # drop UIDENTSTLAE column which occurs the first time in 2021 to bring all dfs to the same dimensions
    #     try:
    #         df_raw = df_raw.drop(["UIDENTSTLAE"], axis=1)
    #     except:
    #         print("column UIDENTSTLAE couldn't be dropped")
    #     else:
    #         print("dropped column")

    # rename columns to get a standardized df for every file
    column_dict = {"IstSonstige": "IstSonstig", "STRZUSTAND": "USTRZUSTAND"}
    df_raw = df_raw.rename(column_dict, axis=1)  # renames if possible

    # filter df down to necessary columns
    column_list = ["OBJECTID", "ULAND", "UREGBEZ", "UKREIS", "UGEMEINDE",
                   "UJAHR", "UMONAT", "USTUNDE", "UWOCHENTAG",
                   "UKATEGORIE", "UART", "UTYP1", "ULICHTVERH",
                   "IstRad", "IstPKW", "IstFuss", "IstKrad", "IstGkfz",
                   "IstSonstig", "USTRZUSTAND", "LINREFX", "LINREFY", "XGCSWGS84", "YGCSWGS84"]
    df_raw = df_raw[column_list]
    # TODO: change col names to lower

    # filter df to region
    filt_location = (df_raw["ULAND"] == geo_ULAND) & (df_raw["UREGBEZ"] == geo_UREGBEZ) & (
            df_raw["UKREIS"] == geo_UKREIS) & (df_raw["UGEMEINDE"] == geo_UGEMEINDE)

    # TODO: generate list_locid from the dict instead of importing it separately
    # list_locid = geo_id_dict.keys()

    # attempts for alternative version where you can use the AGZ as input
    filt_location = (df_raw[list_locid[0]] == geo_id_dict[list_locid[0]]) & \
                    (df_raw[list_locid[1]] == geo_id_dict[list_locid[1]]) & \
                    (df_raw[list_locid[2]] == geo_id_dict[list_locid[2]]) & \
                    (df_raw[list_locid[3]] == geo_id_dict[list_locid[3]])
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
    filt_bikes = (df_location["IstRad"] == 1)
    df_bike = df_location.loc[filt_bikes]
    # print(f'df_bike:    {df_bike}')
    # print(f'columns:    {df_bike.head()}')
    print(year)
    return df_bike


def conc_dfs(df_list: list):
    df_comb = pd.concat(df_list)
    df_comb.to_csv(f'/home/ubuntu/TechLabs_23/new_files/Unfallorte_Muenster_comb.csv', index=False)


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

raw_file_list = get_raw_file_list(path_unfallorte)
print(raw_file_list)

geo_id_dict = {"ULAND": np.int64("05"), "UREGBEZ": np.int64("5"), "UKREIS": np.int64("15"),
               "UGEMEINDE": np.int64("000")}
geo_id_list = [np.int64("05"), np.int64("5"), np.int64("15"), np.int64("000")]

print(geo_id_dict)
df_list = []
for file in raw_file_list:
    try:
        df_bike = cut_to_region(file, geo_id_dict, geo_id_list)
    except:
        print(f'Error: file: {file} could not be processed')
    else:
        print(f'file: {file} was successfully processed')
        df_list.append(df_bike)

conc_dfs(df_list)
