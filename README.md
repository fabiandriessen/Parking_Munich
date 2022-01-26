## API to promote off-street parking Munich

**Important note**

_An activated google API key named k in a file named API.py must be added to the folder. This key is not provided, because this key must be linked to your bank account. However, usage is initially free of charge (e.g. if the 200 euro free credit budget is not exceeded). The API uses the google API multiple times, though all testing and development required not more than 6 euros of credits._

## Project description

This project is a Python-based Application Programming Interface (API), that can be seen as a tool to support consumers to find the nearest off-street parking in Munich. The application enables consumers to compare both off-street parking garages with on-street parking near their destination. If applicable the application also calculates and views the costs if new parking tariffs of the City of Munich, that are currently under review, are indeed implemented. These costs are calculated depending on the districts, according to the tariffs on the map below.


![Figure 1-3](static/parking_tariffs.png?raw=True "Parking tariffs Munich")
_[Source (edited by author)](https://www.sueddeutsche.de/muenchen/muenchen-parkgebuehren-anhebung-kritik-1.5504642)_

**Inputs**

As an input it requires an:
- Origin (anywhere, also outside of Munich).
- Destination (inside or around Munich).
- Parking time of max 24 hours. 

**Outputs**

The API will return:
- The travel time by car to the given destination.
- The five nearest parking garages in the dataset, their capacities, and the tariffs that apply there.
- The travel time from the place of origin to each of the parking garages.
- Travel times by foot, bike or public transport from each parking garage to the given final destination.
- Current and planned street parking costs for the total parking time.
- If available and requested: information on present disabled, women or family parking spots.

With this information, the application serves as a decision making tool to help consumers decide which off-street parking lot is the best alternative.

**Relevance**

TThe project addresses a few issues that are of high priority for the City of Munich. Decreasing car traffic, promoting P+R (Park and Ride) locations and reduce on-street parking. Furthermore, this application is also increasingly relevant for consumers because it has the potential to reduce their travel times and parking costs. Currently, the city has proposed to significantly raise on-street parking tariffs for all non-residents and ban street parking on some intersections. One of our core features is to highlight nearby charging facilities which is important due to the emergence of electric vehicles

**Target group**

This application is best suited for both long-term parking consumers (6+ hours a day) who aren’t able to apply for a parking permit or want to park their car in an off-street parking garage. The application helps select the best parking garage. Future updates will include more features for electric vehicle owners and enable users in long-term contracts to sublet their parking spots through our platform

**Incorporated parking garages**

Currently, only P+R locations regulated by the MVV are in the dataset. However, any commercially or publicly operated parking in Munich may be added to the dataset \Parking_Munich\Data\P_R_Datenbank_2019_ohne.xlsx with at least a a name and GPS Coordinates. This information allows the application to calculate travel times to the parking garage versus the nearby street-parking spaces. Parking at P+R locations is limited to a max of 24h, hence the application does currently not support finding parking for more than 24 consecutive hours.

**Challenges and plans for future features**

Additional data on other parking garages and charging stations are planned to be added to the dataset. This data has already been extracted from Open Street Maps (OSM). However, cleaning this data and converting it to the required format was not possible within the timeframe of this project. On this GitHub page, we have included the aforementioned raw data, partially cleaned datasets, and the Jupyter Notebooks used to extract and clean the data.

The goal of this project is to incorporate this database into a consumer smartphone application. Engaging with parking suppliers, we will provide greater value by adding the ability to book long-term parking spots. The goal is to also serve as a booking service for long-term parking, and not just as a decision-making tool. Up until now, a Proto.io application sketch has been made, that is currently being prepared for consumer and expert feedback. 

## Table of contents
1. Databases

_Currently only the first database is used in the API, the other data files may be incorporated after adequate cleaning._

| File path                                     | Description                                                    |
|-----------------------------------------------|----------------------------------------------------------------|
| P_R_Datenbank_2019_ohne.xlsx                  | MVV P+R database edited for specific API use                   |
| Parking_Munich\Data\Muenchenosm.pbf		| Open Street Maps file Munich				 |
| Parking_Munich\Data\Parkings_in_and_near.xlsx | Partly cleaned OSM parking data for greater Munich area                    |
| Parking_Munich\Data\Parkings_in_only          | Subset of the file above with only places within Munich	 |
| Parking_Munich\Data\Only_in_and_with_cap	| Subset of the file above with only places with known capacity	 |

2. API
		
_Used to make Python functions requestable via the internet._

| File path                                     | Description                                                    |
|-----------------------------------------------|----------------------------------------------------------------|
| Parking_Munich\parking_api.py              	| Actual API that uses static, template and Data folders         |
								

3. Jupyter Notebooks
		
_May be used to analyse datasets and recreate datasets in \Data folder out of the OSM file._

| File path                                     	| Description                                                    |
|-----------------------------------------------	|----------------------------------------------------------------|
| Parking_Munich\parking_application_clean.ipynb	| Contains 2 API functions, useful for testing purposes		 |
| Parking_Munich\Charging.ipynb				| Subset OSM charging station data		 		 |
| Parking_Munich\Munich_dataset_analysis		| Analyse and extract the OSM data				 |

4. Screenshots				

| File path                                     	| Description                                                    |
|-----------------------------------------------	|----------------------------------------------------------------|
| Parking_Munich\Screens				| Screenshots of the API to illustrate functionalities		 |

## How to install and run the project

This is a Python based project developed using Python 3.8, 
all listed packages below may all be installed using pip install **package name**.

Running the API requires the following packages:

- flask
- pandas
- numpy
- matplotlib.pyplot
- haversine
- requests
- json
- googlemaps
- datetime
- any excel reader

To run all of the other jupyter notebooks the following other packages may be needed:

- osmnx
- pyrosm
- ast
 
## How to use the project

To use the project, open a CMD that has access to your Python installation. 

1. cd *path to folder*
2. activate *specific environment with all required packages*
3. python parking_api.py

_This will start a local host, go there to try out the following functionalities:_

### 1. Find the best parking given the origin (anywhere), destination (in Munich) and parking time.

**How to use the application**

Navigate to:

http://127.0.0.1:5000/giveindestination?/ origin= *address1* + destination= *adress2* +parkingtime= *hours, minutes*

- Address 1 and 2 provided in this format: *street,streetnumber (both optional), city, country* 

Other forms may also work depending on the google API but might fail. Check the [google directions documentation](https://developers.google.com/maps/documentation/directions/get-directions) to find out all other address forms that are accepted.

- Parking time must be provided in this format: Minutes, Hours (e.g. if you want to park 7 hours and 10 minutes you give in: 7, 10).

Lastly, some extra functions are available, add the following to the link to see the following extra information:
| Argument	| Also show:				|
| --------------|---------------------------------------|
| invalid=True	| Present parking spots for disabled  	|
| woman=True	| Present female-friendly parking spots	|
| family=True	| Present familiy parking spots		|
| display_dist	| Travel distances to destination	|

**How it works**

The API calls the function find_nearest_parkings, this function consists of the following steps:
1. Reading in parking garage data and creating additional columns to fill later on. Also determine latitude, longitude and district with google API (uses google API 1x).
2. Calculates hemispherical distances from the destination to all parking locations in the dataset using a mathematical formula, by using latitudes and longitudes of parking spots and the destination.
3. Calculates travel time (using Google API 1x) and approximated costs (street parking costs based on the district) if they were to drive directly to the destination.
4. Calculate travel times to the final destination for 5 hemispherically nearest parking garages, for 3 forms of transport and travel times from origin to parking (uses Google API 3*5+5 = 15x).
5. Final output data selection and preparation, drop unnecessary columns, partly based on optional function (user) input.

Thus, the Google API is executed 21 times during one cycle. However, the total execution time is only 3.11s and might be optimized by programming some parts of the code a bit more efficiently. E.g. by determining the district in which each parking is, and only searching in nearby districts for a given location. However, this was not feasible during the limited project time frame.

### 2. View expected availability

**How to use the function**

_After a query is executed, a jpg is generated to visualize the availability for the selected parking garages._ 

This figure is available at http://127.0.0.1:5000/check_availability or can be viewed directly from the static folder.

**How it works**

The function vis_occ is automatically called when the find_nearest_parkings function is executed. It takes a data frame with the availability of x amount of parking garages in it and visualizes the parking garages for which there is occupancy data available. Plotting this data happens according to the usual Python procedure, hereafter, a vertical line that visualizes the current time is also plotted. A more detailed description of this process may be found in the comments of the code.

## Example queries

_Below are some sample queries presented. The results of the given queries can be found in the screens folder_

1. Traveling from Augsburg to the Arcisstrasse in Munich, planning to stay 7 hours and 15 minutes and just interested in core information:

http://127.0.0.1:5000/giveindestination?origin=augsburg,germany&destination=arcisstra%C3%9Fe%2023,Munich,Germany&parkingtime=7,%2015

Results in:

![Figure 1-2](Screens/overview_result_query_1_from_readme.jpg?raw=True "Results from query 1: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-3](Screens/Availability_result_query_1_from_readme.jpg?raw=True "Results from query 1: availability")

2. Travelling from Freising to Hohenschwangaustraße,17, planning to stay 6 hours and 30 minutes and interested in all available information

http://127.0.0.1:5000/giveindestination?origin=Freising,Germany&destination=Hohenschwangaustraße,17,Munich,Germany&parkingtime=6,30&woman=True&invalid=True&family=True&display_dist=True

Results in:

![Figure 1-4](Screens/overview_result_query_2_from_readme.jpg?raw=True "Results from query 2: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-5](Screens/Availability_result_query_2_from_readme.jpg?raw=True "Results from query 2: availability")


3. Travelling from Vaterstetten to Marienplatz, planning to stay 10 hours and interested in all available information

http://127.0.0.1:5000/giveindestination?origin=vaterstetten,Germany&destination=marienplatz1,Munich,Germany&parkingtime=10,%200&woman=True&invalid=True&family=True&display_dist=True

Results in:

![Figure 1-6](Screens/overview_result_query_3_from_readme.jpg?raw=True "Results from query 3: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-7](Screens/Availability_result_query_3_from_readme.jpg?raw=True "Results from query 3: availability")
