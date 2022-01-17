import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import haversine as hs
import requests
import json
import googlemaps
from datetime import datetime
from API import K

def find_nearest_parking(latlon, expected_arrival=datetime.now()):
    """Function to find the nearest parkingplace in Munich given a latitude, 
    longtitude or address and a dataframe with parkings that contains for each entry \
    at least a lon and lat column and optionally an expected arrival time."""
    
    df=pd.read_excel('Data/P_R_Datenbank_2019_ohne.xlsx')
    #create new columns to fill later
    df['bird_dist'] = 0
    
    df['est_time_walking'] = 0
    df['est_time_bicycling'] = 0
    df['est_time_transit'] = 0
    
    df['est_dist_walking'] = 0
    df['est_dist_bicycling'] = 0
    df['est_dist_transit'] = 0
    
    #combine lat and lon in one column
    df['lat_lon']=list(zip(df.lat, df.lon))
    
    #calculate distance as the crow flies from dest to all parkings
    df['bird_dist'] = df.lat_lon.apply(lambda p: hs.haversine((lat_r,lon_r),p))
    
    #sort values based on bird_dist, reset index
    df.sort_values(by='bird_dist',inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    #calculate travel times to final dest for 5 parkings that are the nearest as the crow flies and add them to df
    for i in range (5):
        for j in ['walking','bicycling','transit']:
            #run google api and unpack relevant variables
            if type(latlon) is tuple:
                r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={df.lat[i]},{df.lon[i]}&destination={latlon[0]},{latlon[1]}&mode={j}&key={K}")
            else:
                r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={df.lat[i]},{df.lon[i]}&destination={latlon}&mode={j}&key={K}")
            #unpack
            results = json.loads(r.content)
            legs = results.get("routes").pop(0).get("legs")
            dur_dist=(legs[0].get("duration"), legs[0].get("distance"))
            #save data in previously assigned columns
            df['est_time_'+str(j)][i] = dur_dist[0]['text']
            df['est_dist_'+str(j)][i] = dur_dist[1]['text']
    
    #only first 5 are interesting, drop irrelevant columns
    df=df[:5].drop(columns=['Bahnhof','BahnhofID','GlobaleID', 'Name','Niveau,N,10,0','bird_dist','P+R','MVTT_x','MVTT_y', "Georeferenz", "Name DIVA", "lat_lon"])
    df.rename(columns={"Alternative_name": "Name"}, inplace=True)
    
    #subset availability
    availability = df.filter(regex='OCC_')
    availability = availability.join(df.loc[:,'Name'], lsuffix='_caller', rsuffix='_other')
    availability.set_index('Name', drop=True, inplace=True)
    
    #remove from other dataframe
    df.drop(list(df.filter(regex = 'OCC_')), axis = 1, inplace = True)
    return(df, availability)

def vis_occ(df1):
    a=results[1]

    #Delete parkings of which we don't have the occupancy
    a.dropna(how="all", axis=1, inplace=True)

    #Give columns plottable name
    a.columns=list(np.arange(5,23,1))

    #setup grid
    fig,ax=plt.subplots(1,1,dpi=100, figsize=(8,5))
    tcks=[]
    locs=[]
    for i in range(5,23,3):
        tcks.append(str(i)+"h")
        locs.append(i)
    plt.xticks(locs, tcks)

    #plot vertical line at current time if 
    if 5<datetime.now().hour<22:
        plt.axvline(x=(datetime.now().hour+(datetime.now().minute/60)), linestyle="--", alpha=0.5, color='r', label='Current_time')
    ax.set_xlabel('Time of day')
    ax.set_ylabel('Expected occupancy [%]')
    ax.set_title('Expected occupancy during the day')

    for i,j in enumerate(a.index):
        print()
        ax=a.iloc[i].plot(alpha=0.5)

    # legend = plt.legend(loc="lower left", edgecolor="black", fontsize=8, framealpha=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=5)
    return(fig,ax)
