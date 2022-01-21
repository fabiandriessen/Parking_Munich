import flask
from flask import request, jsonify, Response, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import haversine as hs
import requests
import json
import googlemaps
from datetime import datetime
from API import K
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def find_nearest_parking(origin, destination, parking_time, display_dist=False, disabled=False, woman=False, family=False, expected_arrival=datetime.now()):
    """Function to serve as a decision making tool to find the nearest parkingplace in Munich given a address,
    and a dataframe with parkings that contains for each entry at least a lon and lat column 
    and optionally an expected arrival time (by default set to datetime.now()"""
    ############################################################################################
    ##step1: reading in data and preparing data    
    ############################################################################################
    #readin dataframe
    df=pd.read_excel('Data/P_R_Datenbank_2019_ohne.xlsx')
    #create needed lat and lon if normal address is input
    r= requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key={K}")
    #unpack
    results = json.loads(r.content)
    #save lat, lon (to calculate bird_dist) and district (to calculate street parking tariffs)
    district = results['results'][0]['address_components'][2]['long_name']
    lat_r = results['results'][0]['geometry']['location']['lat']
    lon_r = results['results'][0]['geometry']['location']['lng']
    
    parking_time=tuple(map(int, parking_time.split(', ')))

    #create new columns to fill later
    df['bird_dist'] = 0
    df['Driving to parking'] = 0
    
    df['est_time_walking'] = 0
    df['est_time_bicycling'] = 0
    df['est_time_transit'] = 0
    
    if display_dist:
        df['est_dist_walking'] = 0
        df['est_dist_bicycling'] = 0
        df['est_dist_transit'] = 0
    
    #combine lat and lon in one column
    df['lat_lon']=list(zip(df.lat, df.lon))
    
    ############################################################################################
    #step 2: calculate distance as the crow flies from dest to all parkings
    ############################################################################################
    
    df['bird_dist'] = df.lat_lon.apply(lambda p: hs.haversine((lat_r,lon_r),p))
    
    #sort values based on bird_dist, reset index
    df.sort_values(by='bird_dist',inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    ############################################################################################
    #step 3:calculate travel time and approx costs if they where to drive directly to dest
    ############################################################################################

    r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=driving&key={K}")
    #unpack
    results = json.loads(r.content)
    legs = results.get("routes").pop(0).get("legs")
    df['Driving to destination'] = legs[0].get("duration")['text']
    
    costsin1 = ['Milbershofen', 'Trudinger-Riem', 'Schwanthalerhöhe', 'Ludwigsvorstadt', 'Isarvorstadt', 'Au', 'Haidhausen',
                'Au-haidhausen', 'Giesing', 'Steinhausen', 'Tivoli', 'Maxvorstadt', "Schwabing-west", "Glockenbach", "Untersendling"]
    costsin2 = ['Moosach', 'Neuhausen', "Sendling-Westpark", "Giesling"]
    
    if ('Altstadt' in district) or ('Lehel' in district):
        df['Current costs streetparking'] = round((parking_time[0]*2.5+(parking_time[1]/60)*2.5),2)
    elif district in costsin1:
        df['Current costs streetparking'] = round(max((parking_time[0]*1+(parking_time[1]/60)*1), 6),2)
        df['Planned costs streetparking'] = round(max((parking_time[0]*1.9+(parking_time[1]/60)*1.9), 12),2)
    elif district in costsin2:
        df['Planned costs streetparking'] = round(max((parking_time[0]*1.9+(parking_time[1]/60)*1.9), 12),2)
    else:
        df['Current costs streetparking'] = 'free'
        
    ############################################################################################
    #step 4:calculate travel times to final dest for 5 nearest parkings for 3 forms of transport
    ############################################################################################
    
    for i in range (5):
        r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={df.lat[i]},{df.lon[i]}&mode=driving&key={K}")
            #unpack
        results = json.loads(r.content)
        legs = results.get("routes").pop(0).get("legs")
        df['Driving to parking'][i] = legs[0].get("duration")['text']
            
        for j in ['walking','bicycling','transit']:
            #run google api and unpack relevant variables
            r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={df.lat[i]},{df.lon[i]}&destination={destination}&mode={j}&key={K}")
            #unpack
            results = json.loads(r.content)
            legs = results.get("routes").pop(0).get("legs")
            dur_dist=(legs[0].get("duration"), legs[0].get("distance"))
            #save data in previously assigned columns
            df['est_time_'+str(j)][i] = dur_dist[0]['text']
            if display_dist:
                df['est_dist_'+str(j)][i] = dur_dist[1]['text']
    
    ############################################################################################
    #step 5: final output data selection and preparation
    ############################################################################################
    
    #only first 5 are interesting, drop irrelevant columns
    df=df[:5].drop(columns=['lat','lon','Bahnhof','BahnhofID','GlobaleID', 'Name','Niveau,N,10,0','bird_dist','MVTT_x','MVTT_y', "Georeferenz", "Name DIVA", "lat_lon",'Entrance'])
    
    df.rename(columns={"Alternative_name": "Name"}, inplace=True)
    
    #subset availability
    availability = df.filter(regex='OCC_')
    availability = availability.join(df.loc[:,'Name'], lsuffix='_caller', rsuffix='_other')
    availability.set_index('Name', drop=True, inplace=True)
    
    to_k =['Name', 'Driving to parking','est_time_walking','est_time_bicycling', 'est_time_transit', 'Day_price',
           'Ticket_for_10', 'Month_ticket', 'Year_ticket','Driving to destination']
    
    if 'Current costs streetparking' in df.columns:
        to_k.append('Current costs streetparking')
    if 'Planned costs streetparking' in df.columns:
        to_k.append('Planned costs streetparking')
        
    if woman:
        to_k.append('P_women')
    if disabled:
        to_k.append('P_invalid')
    if family:
        to_k.append('P_family')
        
    to_k.append('Capacity')
    to_k.append('Link')
    df = df[to_k] #Create new dataframe with columns in the order you want
    
    #remove from other dataframe
    df.drop(list(df.filter(regex = 'OCC_')), axis = 1, inplace = True)
    return(df, availability)


def vis_occ(a):

    #Delete parkings of which we don't have the occupancy
    a.dropna(how="all", axis=1, inplace=True)

    #Give columns plottable name
    a.columns=list(np.arange(5,23,1))

    #setup grid
    fig,ax=plt.subplots(1,1,dpi=200, figsize=(8,5))
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
        ax=a.iloc[i].plot(alpha=0.5)

    # legend = plt.legend(loc="lower left", edgecolor="black", fontsize=8, framealpha=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=3)
    plt.savefig('static\A_fig.jpg', bbox_inches='tight')
    return(fig)



@app.route('/', methods=['PUSH','GET'])
def home():
    return '''<h1>Find the best parking in Munich</h1>
<p>Go to ""/giveindestination to give in an adress or (lat,lon) to get started! </p>'''


@app.route('/giveindestination', methods=['GET'])
def api_all():
    query_parameters = request.args
    origin = query_parameters.get('origin')
    destination = query_parameters.get('destination')
    parktime = query_parameters.get('parkingtime')
    
    woman = False
    family = False
    invalid = False
    display_dist = False
    
    if query_parameters.get('woman'):
        woman = query_parameters.get('woman')
    if query_parameters.get('family'):
        family = query_parameters.get('family')
    if query_parameters.get('invalid'):
        invalid = query_parameters.get('invalid')
    if query_parameters.get('display_dist'):
        display_dist = query_parameters.get('display_dist')
    
    df, availability = find_nearest_parking(origin, destination, parktime, display_dist, invalid, woman, family)
    #now also create figure
    fig = vis_occ(availability)
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
#     left here for testing
#     return jsonify(origin, destination, parktime)

    
@app.route('/check_availability')
def show_index():
    full_filename=r"static\A_fig.jpg"
    return render_template('Index.html', user_image = full_filename)    



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
