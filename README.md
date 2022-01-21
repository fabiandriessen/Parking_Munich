-----------------------------------------------------------------	
-----------------------------------------------------------------	
1. Project title :API to promote off-street parking munich
-----------------------------------------------------------------	
-----------------------------------------------------------------	

-----------------------------------------------------------------	
-----------------------------------------------------------------	
2. Project description
-----------------------------------------------------------------	
-----------------------------------------------------------------	

API to find the nearest off-parking in Munich, given the origin (anywhere, also outside of Munich), destination and parking time (stay duration). The API will return a selection of the five nearest parkings, the traveltime by car to the given destination, to the parking and traveltimes by foot, bike or public transport from the parking garage to the given destination. 

Moreover, the application also returns costs of street-parking and the planned street-parking costs if these are available and relevant. In this manner, the application enables consumers to make a adequate decision and stimulates off-street parking and alternative means of last-mile transport.

Currently only P+R locations that are regulated by the MVV are in the dataset. However, any commercially or publicly operated parking in Munich may be added to the dataset \Parking_Munich\Data\P_R_Datenbank_2019_ohne.xlsx with at least a name, lat and lon, for the application to calculate traveltimes and compare it with the street-parking alternative in the region of the destination.

-----------------------------------------------------------------	
-----------------------------------------------------------------	
3. ProjectOutline
-----------------------------------------------------------------	
-----------------------------------------------------------------	

-----------------------------------------------------------------	
File						Description
-----------------------------------------------------------------	
1. Databases				Currently only the first 								database is used in the API, 
						the other datafiles may be 								appended after thorough cleaning
-----------------------------------------------------------------	

Parking_Munich\Data\			MVV P+R database edited for 
P_R_Datenbank_2019_ohne.xlsx	specific API use								
Parking_Munich\Data\Parkings	Partly cleaned OSM parking data 
_in_and_near.xlsx			Munich Area

Parking_Munich\Data\Parkings	Partly cleaned OSM parking data,
_in_only			 		subset of places within Munich

Parking_Munich\Data\Only_in_	Partly cleaned OSM parking data, 
and_with_cap				subset of places within Munich 
						and only with known capacity

Parking_Munich\Data\Muenchen.	Open Street Maps file for Munich
osm.pbf					area
-----------------------------------------------------------------	

2. Application Programming 		Used to make Python functions 
Interface (API)				requestable via the internet
-----------------------------------------------------------------									
Parking_Munich\parking_api.py	Actual API, uses static, 								template and Data folders
-----------------------------------------------------------------	

3. Jupyter Notebooks			Used to analyse datasets and to 							prove concepts
-----------------------------------------------------------------	
Parking_Munich\parking_applic	Jupyter Notebook with two 
ation_clean.ipynb			functions written to use in the 							API, may be used for testing

Parking_Munich\Charging.ipynb	Jupyter lab to subset OSM data 							on charging stations in Munich

Parking_Munich\Munich_dataset	Jupyter lab to analyse and 
_analysis					extract and the OSM data 
						to create the three non-MVV 							datasets
4. Screenshots				Screenshots of the API to 								illustarate the functionalities 							of the API
-----------------------------------------------------------------	
Parking_Munich\screenshots		jpg files


-----------------------------------------------------------------	
-----------------------------------------------------------------	
4. How to Install and Run the Project
-----------------------------------------------------------------	
-----------------------------------------------------------------	
This is a python based project, developed using Python 3.8, running the api requires the following packages, that may all be installed using pip install ... in anaconda prompt

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
 
-----------------------------------------------------------------	
-----------------------------------------------------------------	
Important note!!
-----------------------------------------------------------------	
-----------------------------------------------------------------	
Lastly, also an activated google API key named k in a file named API.py must be added to the folder. This key is not provided, because this key must be linked to you bank account. However, usage is initially free of charge (e.g. if the 200 euro free credit budget is not exceeded). The API uses the google API multiple times, though all testing and development required not more than 6 euros of credits.

-----------------------------------------------------------------	
-----------------------------------------------------------------	
5. How to use the project
-----------------------------------------------------------------	
-----------------------------------------------------------------	
To use the project, open a CMD through which you can execute python statements. 

Run the following statements:
-----------------------------------------------------------------	
1. cd *path to folder*
2. activate *specific environment*
3. python parking_api.py
-----------------------------------------------------------------	

This will start a local host, go there to try out the following functionalities:
-----------------------------------------------------------------	
1. Find the best parking given a origin, destination (in Munich) and parkingtime.
-----------------------------------------------------------------	

/giveindestination?/origin=*address1*+destination=*adress2*+parkingtime=*hours, minutes*

address 1 and 2 must be given in like this: 
-----------------------------------------------------------------	
street,streetnumber,country. 
-----------------------------------------------------------------	
Other forms may also work depending on the google API but might fail.

parking time must be given in like this the first number being the amount of hours and the second number the amount of minutes:
-----------------------------------------------------------------	
7, 10
-----------------------------------------------------------------	

Lastly some extra functions are available, add the following to the link to see the following extra information:

+invalid=True	available parkings for disabled
+woman=True	available womens parkings
+family=True	available familiy parkings
+display_dist	also show actual distances to destination from 				parking destination for three individual forms of 			transport

-----------------------------------------------------------------	
-----------------------------------------------------------------	
6. Example queries
-----------------------------------------------------------------	
-----------------------------------------------------------------	



