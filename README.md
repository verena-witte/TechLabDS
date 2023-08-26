# Bike accidents map

A visualization tool to map and analyze bike accidents in Münster. The project provides an interactive map with filters to understand accident trends based on different factors such as the day of the week, hour of the day, type of vehicle involved, and road conditions

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Using command line on your computer:

1. Ensure you have Python 3.x installed.
2. Install the required libraries: pip install pandas folium ipywidgets
3. Clone this repository or download the project files.
4. Place the Unfallorte_Muenster_comb.csv file in the same directory as the script.

Using Anaconda / Jupyter Notbook:

1. If you haven't already, install Anaconda for your OS.
2. Open Anaconda Navigator.
3. Launch Jupyter Notebook:
4. Open the tab "Files"
5. Click "New" in the up right corner
6. Choose Python 3 (ipykernel) notebook from the dropdown menu.
7. Copy-paste the code from Visualisierung_map.py into the notebook.
8. Replace the directory in the function "# CSV-Datei einlesen
    df = pd.read_csv('Unfallorte_Muenster_comb.csv')" with the correct directory from your computer.
9. Execute the code by clicking the "Run" button of the Jupyter notebook. 
10. Manipulate the headmap to your liking by adjusting the parameter widgets. 


## Usage

Run the Visualisierung_map.py script: python Visualisierung_map.py

An interactive map will be displayed with the available filters. Adjust the filters as needed to view specific accident trends.

Additionally, the Visuals_manual.xlsx file provides statistics on the number of bicycle accidents by month for each year from 2019 to 2022. This can be used for further analysis and comparisons

## Features

- Interactive Heat Map: Visualize the locations of bike accidents in Münster using a heatmap
- Accident Statistics: View the number of accidents by month for each year from 2019 to 2022
- Filters:
    1. Day of the week
    2. Hour of the day
    3. Type of vehicle involved
    4. Road conditions


## Contributing

Contributions to the project are welcome. If you have a feature request, bug report, or want to improve the codebase:

Fork the repository.
Create a new branch.
Implement your changes or fixes.
Submit a pull request for review.
Ensure that your code follows the project's coding standards and that any new features or changes are well-documented.

