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


def cut_to_region(csv_path: str, geo_id_dict: dict, column_dict: dict, path_base=os.getcwd()):
    # filters the dataframe from the submitted file to a region specified by
    # the german AGS ID (amtliche Gemeinde Schlüssel) in the geo_id_dict

    df_raw = pd.read_csv(csv_path, delimiter=";")

    # convert the column names to lowercase letters
    df_raw.rename(columns=str.lower, inplace=True)

    year = df_raw.loc[1, "ujahr"]  # retrieve the year of the data file to later namning

    # rename columns to get a standardized df for every file
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
    df_comb = pd.concat(df_list)  # concatenate the dfs of the different years into one df
    df_comb.to_csv(os.path.join(path_base, f"Unfallorte_Muenster_comb.csv"), index=False)


def main(geo_id_dict: dict, column_dict: dict, path_base=os.getcwd()):
    # controls the whole workflow
    # if path_base is not submitted, the current working directory is used as default

    raw_file_list = get_raw_file_list(path_base)
    print(raw_file_list)

    print(geo_id_dict)
    df_list = []
    for file in raw_file_list:

        print(file)

        try:
            df_bike = cut_to_region(file, geo_id_dict, column_dict, path_base)
        except:
            print(f'Error: file: {file} could not be processed')
        else:
            print(f'file: {file} was successfully processed')
            df_list.append(df_bike)

    conc_dfs(df_list, path_base)


if __name__ == '__main__':
    ### for users:
    # change "path_base" according to your directories containing the "Unfallorte.._LinRef.csv/.txt" files
    # if path_base is not submitted, the current working directory is used as default
    path_base = ".\\Unfallorte"

    geo_id_dict = {"uland": np.int64("05"), "uregbez": np.int64("5"), "ukreis": np.int64("15"),
                   "ugemeinde": np.int64("000")}  # change to filter for another city or region by replacing the
    # numbers according to the german AGS ID (amtliche Gemeinde Schlüssel)

    column_dict = {"istsonstige": "istsonstig", "strzustand": "ustrzustand", "iststrassenzustand": "ustrzustand"}  #
    # this dict is necessary to accommodate for changes in column naming of the submitted files

    main(geo_id_dict, column_dict, path_base)
