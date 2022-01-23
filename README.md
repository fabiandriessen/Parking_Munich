### API to promote off-street parking munich
Important note
----------------------------------------------------------------------------------------------------------------------------	
An activated google API key named k in a file named API.py must be added to the folder. This key is not provided, because this key must be linked to you bank account. However, usage is initially free of charge (e.g. if the 200 euro free credit budget is not exceeded). The API uses the google API multiple times, though all testing and development required not more than 6 euros of credits.
----------------------------------------------------------------------------------------------------------------------------	

## Project description

API to find the nearest off-parking in Munich, given the origin (anywhere, also outside of Munich), destination and parking time (stay duration). The API will return a selection of the five nearest parkings, the traveltime by car to the given destination, to the parking and traveltimes by foot, bike or public transport from the parking garage to the given destination. Moreover, the application also returns costs of street-parking and the planned street-parking costs if these are available and relevant. In this manner, the application enables consumers to make a adequate decision and stimulates off-street parking and alternative means of last-mile transport.

Currently only P+R locations that are regulated by the MVV are in the dataset. However, any commercially or publicly operated parking in Munich may be added to the dataset \Parking_Munich\Data\P_R_Datenbank_2019_ohne.xlsx with at least a name, lat and lon, for the application to calculate traveltimes and compare it with the street-parking alternative in the region of the destination.

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

2. Application Programming Interface (API)
		
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

flask
pandas
numpy
matplotlib.pyplot
haversine
requests
json
googlemaps
datetime
any excel reader

To run all of the other jupyter notebooks the following other packages may be needed:

osmnx
pyrosm
ast
 
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

2. Travelling from Freising to Hohenschwangaustraße,17, planning to stay 6 hours and 30 minutes and interested in all other available information

http://127.0.0.1:5000/giveindestination?origin=Freising,Germany&destination=Hohenschwangaustraße,17,Munich,Germany&parkingtime=6,30&woman=True&invalid=True&family=True&display_dist=True

3. Travelling from Vaterstetten to Marienplatz, planning to stay 10 hours and interested in all other available information

http://127.0.0.1:5000/giveindestination?origin=vaterstetten,Germany&destination=marienplatz1,Munich,Germany&parkingtime=10,%200&woman=True&invalid=True&family=True&display_dist=True

