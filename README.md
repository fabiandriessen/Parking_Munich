## API to promote off-street parking munich

**Important note**

_An activated google API key named k in a file named API.py must be added to the folder. This key is not provided, because this key must be linked to you bank account. However, usage is initially free of charge (e.g. if the 200 euro free credit budget is not exceeded). The API uses the google API multiple times, though all testing and development required not more than 6 euros of credits._

## Project description

This project is a Python based Application Programming Interface (API), that can be seen as a tool to support consumers to find the nearest off-street parking in Munich. Moreover, the application enables consumers to compare these off-street parking with on-street parking near their destination. If applicable the application also calculates and views the costs if new parking tariffs of the City of Munich, that are currently under review, are indeed implemented. These costs are calculated depending on the city part, according to the tariffs on the map below.


![Figure 1-3](static/parking_tariffs.png?raw=True "Parking tariffs Munich")
_Source (edited): https://www.sueddeutsche.de/muenchen/muenchen-parkgebuehren-anhebung-kritik-1.5504642_

**Inputs**

As an input it requires an:
- Origin (anywhere, also outside of Munich).
- Destination (inside or around Munich).
- Parking time of max 24 hours. 

**Outputs**

The API will return:
- The traveltime by car to the given destination.
- The five nearest parkings in the dataset, their capacities, and the tariffs that apply there.
- The traveltime from the place of origin to each of the parkings.
- Traveltimes by foot, bike or public transport from each parking garage to the given final destination.
- Current and planned street parking costs given the parking time.
- Optionally: information on present disabled, women or family parkingspots.

In this manner, the application enables consumers to make an adequate decision, and stimulates off-street parking and alternative means of last-mile transport.

**Relevance**

The reason for this project is the wish of the municipality of Munich to decrease car traffic in general, promote P+R locations and reduce on-street parking. Furthermore this application is also increasingly relevant for consumers because it has the potential to reduce their travel times and parking costs. Adittionally, proposed plans to significantly rise on-street parking tariffs for all non-residents and ban street parking in at a growing degree and the emergence of electric vehicles are expected to make this application even more relevant in the near future.

**Target group**

This application is relevant for regular middle long-term or long-term parking consumers in the city of Munich who cannot apply for a resident permit, or residents that want to park their car in an off-street parking garage. The application may help them to select the best parking, future extensions aim to focus on users with an electric car, enable users to book parkings by engaging in long-term contracts and facilitate sublenting parkings by consumers via the platform.

**Incorporated parkings**

Currently only P+R locations that are regulated by the MVV are in the dataset. However, any commercially or publicly operated parking in Munich may be added to the dataset \Parking_Munich\Data\P_R_Datenbank_2019_ohne.xlsx with at least a name, lat and lon, for the application to calculate traveltimes and compare it with the street-parking alternative in the region of the destinations. Parking at P+R locations is limited to max 24h. 

**Challenges and plans for future features**

The data on other parkings and charging stations is planned to be implemented. This data has been extracted from Open Street Maps (OSM), but cleaning this data and converging it to the required format was not possible within the time of this project. However, the raw data, some partly cleaned datasets, and the Jupyter Notebooks that are used to extract and clean the data are also provided at this GitHub page.

Besides this, the plan is to develop an smartphone application for end-users and to engage in contracts with parking suppliers. The goal is also serve as a booking service for long-term parking, and not just as a decison-making tool. Up untill now a proto.io application has been made that is currently being prepared for consumer and expert feedback. 

## Table of contents
1. Databases

_Currently only the first database is used in the API, the other datafiles may be appended after adequate cleaning._

| File path                                     | Description                                                    |
|-----------------------------------------------|----------------------------------------------------------------|
| P_R_Datenbank_2019_ohne.xlsx                  | MVV P+R database edited for specific API use                   |
| Parking_Munich\Data\Muenchenosm.pbf		| Open Street Maps file for Munich				 |
| Parking_Munich\Data\Parkings_in_and_near.xlsx | Partly cleaned OSM parking data Munich area                    |
| Parking_Munich\Data\Parkings_in_only          | Subset of file above with only places within Munich		 |
| Parking_Munich\Data\Only_in_and_with_cap	| Subset of file above with only parkings with known capacity	 |

2. API
		
_Used to make Python functions requestable via the internet._

| File path                                     | Description                                                    |
|-----------------------------------------------|----------------------------------------------------------------|
| Parking_Munich\parking_api.py              	| Actual API, uses static, template and Data folders             |
								

3. Jupyter Notebooks
		
_May be used to analyse datasets and recreate datasets in \Data folder out of the OSM file._

| File path                                     	| Description                                                    |
|-----------------------------------------------	|----------------------------------------------------------------|
| Parking_Munich\parking_application_clean.ipynb	| Contains 2 API functions, useful for testing purposes		 |
| Parking_Munich\Charging.ipynb				| Subset OSM charging station data		 		 |
| Parking_Munich\Munich_dataset_analysis		| Analyse and extract and the OSM data				 |

4. Screenshots				

| File path                                     	| Description                                                    |
|-----------------------------------------------	|----------------------------------------------------------------|
| Parking_Munich\Screens				| Screenshots of the API to illustarate functionalities		 |

## How to install and run the project

This is a python based project developed using Python 3.8, 
all listed packes below may all be installed using pip install ... in anaconda prompt.

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

To use the project, open a CMD that has access your Python installation. 

1. cd *path to folder*
2. activate *specific environment with all required packages*
3. python parking_api.py

_This will start a local host, go there to try out the following functionalities:_

1. Find the best parking given a origin, destination (in Munich) and parkingtime.

Navigate to:

http://127.0.0.1:5000/giveindestination?/ origin= *address1* + destination= *adress2* +parkingtime= *hours, minutes*

- Address 1 and 2 must be given in like this: *street,streetnumber (both optional), city, country* 

Other forms may also work depending on the google API, but might fail. Check the google directions documentation too find out all other adress forms that are accepted.

- Parking time must be given in like this the first number being the amount of hours and the second number the amount of minutes: *7, 10*

Lastly some extra functions are available, add the following to the link to see the following extra information:
| Argument	| Also show:				|
| --------------|---------------------------------------|
| invalid=True	| Present parkings for disabled	  	|
| woman=True	| Present womens parkings		|
| family=True	| Present familiy parkings		|
| display_dist	| Travel distances to destination	|

2. View expected availability

_After a query is excuted a jpg is generated to visualize the availability for the found parkings._ 

This figure is available at http://127.0.0.1:5000/check_availability or can be viewed directly from the static folder.


## Example queries

_Below some example queries are presented, the results of these give queries can be found in the screens folder_

1. Traveling from augsburg to the arcisstrasse in Munich, planning to stay 7 hours and 15 miutes and just interested in core information:

http://127.0.0.1:5000/giveindestination?origin=augsburg,germany&destination=arcisstra%C3%9Fe%2023,Munich,Germany&parkingtime=7,%2015

Results in:

![Figure 1-2](Screens/overview_result_query_1_from_readme.jpg?raw=True "Results from query 1: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-3](Screens/Availability_result_query_1_from_readme.jpg?raw=True "Results from query 1: availability")

2. Travelling from Freising to Hohenschwangaustraße,17, planning to stay 6 hours and 30 minutes and interested in all other available information

http://127.0.0.1:5000/giveindestination?origin=Freising,Germany&destination=Hohenschwangaustraße,17,Munich,Germany&parkingtime=6,30&woman=True&invalid=True&family=True&display_dist=True

Results in:

![Figure 1-4](Screens/overview_result_query_2_from_readme.jpg?raw=True "Results from query 2: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-5](Screens/Availability_result_query_2_from_readme.jpg?raw=True "Results from query 2: availability")


3. Travelling from Vaterstetten to Marienplatz, planning to stay 10 hours and interested in all other available information

http://127.0.0.1:5000/giveindestination?origin=vaterstetten,Germany&destination=marienplatz1,Munich,Germany&parkingtime=10,%200&woman=True&invalid=True&family=True&display_dist=True

Results in:

![Figure 1-6](Screens/overview_result_query_3_from_readme.jpg?raw=True "Results from query 3: overview")

Navigating to http://127.0.0.1:5000/check_availability afterwards gives:

![Figure 1-7](Screens/Availability_result_query_3_from_readme.jpg?raw=True "Results from query 3: availability")
