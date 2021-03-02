'''
Created on May 18, 2018; Updated on June 24, made it single-thread again!
In our traffic incident data, there are some redundant events. Redundant events are those which have almost started at the same, 
    at the very same location, and have the exact same type. 
@author: sobhan
'''

import pandas as pd
import time
import math
from datetime import date, datetime, timedelta
import threading

class event:
    eventId = ''
    type = ''
    refinedType = ''
    startTime = '' #UTC 
    endTime = '' #UTC
    locationLat = 0
    locationLng = 0
    distance = 0 #mi
    airportCode = ''
    number = 0
    street = ''
    side = ''
    city = ''
    county = ''
    state = ''
    zipCode = ''
    childs = set()
    parents = set()
    toBeMerged = False
    modified= False
       
    def __init__(self, eventId, type, refinedType, startTime, endTime, locationLat, locationLng, distance, 
                 airportCode, number, street, side, city, county, state, zipCode, childs=set(), parents=set(), toBeMerged = False, modified = False):
        self. eventId = eventId
        self.type = type
        self.refinedType = refinedType
        self.startTime = datetime.strptime(startTime.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.endTime = datetime.strptime(endTime.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.locationLat = locationLat
        self.locationLng = locationLng
        self.distance = distance
        self.airportCode = airportCode
        self.number = number
        self.street = street
        self.side = side
        self.city = city
        self.county = county
        self.state = state
        self.zipCode= zipCode
        self.childs = childs
        self.parents = parents
        self.toBeMerged = toBeMerged
        self.modified = modified
           
def haversineDistance(aLat, aLng, bLat, bLng):
    #From degree to radian
    fLat = math.radians(aLat)
    fLon = math.radians(aLng)
    sLat = math.radians(bLat)
    sLon = math.radians(bLng)
           
    R = 3958.7564 #mi
    #R = 6371000.0 #meters
    #R = 6371.0 #km
    dLon = sLon - fLon
    dLat = sLat - fLat
    a = math.sin(dLat/2.0)**2 + (math.cos(fLat) * math.cos(sLat) * math.pow(math.sin(dLon/2.0), 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
       
    return R * c
   
def loadZipToAirportCode():
    zipToAirpot = {}
       
    with open(path + 'AirportForZipsUSA_Augmented.csv', 'r') as lines:
        header = True
        for r in lines:
            if header:
                header = False
                continue
            r = r.replace('\r', '').replace('\n', '').split(',')
            zipToAirpot[r[0]] = r[1]            
       
    zipToAirpot['N/A'] = 'N/A'
       
    return zipToAirpot
   
def loadEventData():    
    zip_to_traffic_event = {}
    airport_to_weather_event = {}
    #CHUNKSIZE = 1000000
    start = time.time()
    count = 0

    #total_traffic = pd.DataFrame()
    #total_weather = pd.DataFrame()

    events = pd.read_csv(path + 'AllEvents_EntireData.csv', dtype = str) # , chunksize=CHUNKSIZE
    #chunk_list_traffic = []
    #chunk_list_weather = []
    for i, r in events.iterrows():
        #for i in range(0, len(r)):
        events = {}
        if r[1] == 'W':
            if r[12] in airport_to_weather_event:
                events = airport_to_weather_event[r[12]]
            childs = set()
            parents = set()
            refined = ('' if isinstance(r[2], float) else r[2]) + '-' + ('' if isinstance(r[3], float) else r[3])
            e = event(eventId=r[0], type='W', refinedType=refined, startTime=r[6], endTime=r[7], locationLat=0, locationLng=0,  
                        distance=0, airportCode=r[12], number=0, street='NA', side='NA', city='NA', county='NA', state='NA', 
                        zipCode='NA', childs=childs, parents=parents, toBeMerged=False, modified=False)
            events[e.eventId] = e
            airport_to_weather_event[r[12]] = events
        else:
            if isinstance(r[19], float):
                continue
            if r[19] in zip_to_traffic_event:
                events = zip_to_traffic_event[r[19]]
            childs = set()
            parents = set()
            refined = ('' if isinstance(r[2], float) else r[2]) + '-' + ('' if isinstance(r[3], float) else r[3])

            e = event(eventId=r[0], type='T', refinedType=refined, startTime=r[6], endTime=r[7], locationLat=float(r[9]), locationLng=float(r[10]), 
                        distance=float(r[11]), airportCode=r[19], number=(0 if isinstance(r[13], float) else int(r[13])), street=r[14], side=r[15], city=r[16], 
                        county=r[17], state=r[18], zipCode=r[19], childs=childs, parents=parents, toBeMerged=False, modified=False)
            events[e.eventId] = e
            zip_to_traffic_event[r[19]] = events  
            
        count += 1
        if count%10000 == 0: print('processed {} lines from all event data file.'.format(count))
        #chunk_list_traffic.append(zip_to_traffic_event)
        #chunk_list_weather.append(airport_to_weather_event)
    #total_traffic = pd.concat(chunk_list_traffic, ignore_index= True)
    #total_traffic.reset_index(drop = True)    
    #total_weather = pd.concat(chunk_list_weather, ignore_index= True)
    #total_weather.reset_index(drop = True)
    print ('Event data is loaded in: %.1f sec'%(time.time()-start))
    return zip_to_traffic_event, airport_to_weather_event #total_traffic, total_weather

    
def integrateSimilarTrafficIncidents(trTimeThresh = 5, distanceThresh = 0.2): 
    '''Time thresholds are in minutes'''
    start = time.time()
    count = 0
    similarPairsOfEvents = totalPairs = 0
    
    for z in zipToAirport:            
        count += 1
        if count%10 == 0:
            print ('Processed %d zips, progress: %.2f' % (count, float(count)/len(zipToAirport)*100))
        
        incidents = {}            
        if z in zip_to_traffic_event: 
            incidents = zip_to_traffic_event[z]
           
        if len(incidents) == 0:
            continue                
           
        for i1 in incidents:
            if incidents[i1].toBeMerged:
                continue            
            trigger = False
            for i2 in incidents:               
                if trigger:
                    
                    dist = haversineDistance(incidents[i1].locationLat, incidents[i1].locationLng, incidents[i2].locationLat, incidents[i2].locationLng)
                    timeDiff = abs((incidents[i1].startTime - incidents[i2].startTime).total_seconds())
                       
                    '''I need to merge events with the same start location and approximate start time'''
                    if dist < 0.06 and  timeDiff < (trTimeThresh*60) and incidents[i1].refinedType == incidents[i2].refinedType and \
                        'Congestion' in incidents[i1].refinedType and incidents[i1].side == incidents[i2].side and incidents[i1].street == incidents[i2].street:
                           
                        incidents[i1].startTime = min(incidents[i1].startTime, incidents[i2].startTime)
                        incidents[i1].endTime = max(incidents[i1].endTime, incidents[i2].endTime)
                        incidents[i1].distance = max(incidents[i1].distance, incidents[i2].distance)                        
                        incidents[i1].modified = True
                           
                        if not incidents[i2].toBeMerged:
                            similarPairsOfEvents += 1                        
                        incidents[i2].toBeMerged = True   
                    totalPairs += 1 
                elif i1 == i2:
                    trigger = True
           
        zip_to_traffic_event[z] = incidents
       
    print ('Have found {} similar pairs of traffic incidents out of {} pairs, in {:.1f} seconds'.format(similarPairsOfEvents, totalPairs, time.time()-start))
    
       
def integrateSimilarWeatherEvents(): 
    '''Time thresholds are in minutes'''
    start = time.time()
    count = 0
    similarPairsOfEvents = totalPairs = 0
    
    for a in airport_to_weather_event:      
        count += 1
        if count%10 == 0:
            print ('Processed %d Airport Stations, progress: %.2f' % (count, float(count)/len(airport_to_weather_event)*100))
                  
        events = airport_to_weather_event[a]
        if len(events) == 0:
            continue
            
        for i1 in events:
            if events[i1].toBeMerged:
                continue            
            trigger = False
            for i2 in events:               
                if trigger:
                    if events[i1].refinedType == events[i2].refinedType:
                        timeDiff = max((events[i1].startTime - events[i2].endTime).total_seconds(), (events[i2].startTime - events[i1].endTime).total_seconds())     # IS THIS CORRECT??? WHAT ABOUT THE CASE FOR TRAFFIC INCIDENTS?              
                        if 'snow' in events[i1].refinedType: th = wTimeThreshs['snow']
                        elif 'rain' in events[i1].refinedType: th = wTimeThreshs['rain']
                        else: th = wTimeThreshs['default']
                        ''' Those weather events which happened sequentially, with a small gap in time, can be merged '''
                        if timeDiff < (th*60):
                            events[i1].startTime = min(events[i1].startTime, events[i2].startTime)
                            events[i1].endTime = max(events[i1].endTime, events[i2].endTime)                              
                            events[i1].modified = True                       
                               
                            if not events[i2].toBeMerged:
                                similarPairsOfEvents += 1
                            events[i2].toBeMerged = True     
                           
                    totalPairs += 1 
                elif i1 == i2:
                    trigger = True
            
        airport_to_weather_event[a] = events
    
    print ('Have found {} similar pairs of weather events out of {} pairs, in {:.1f} seconds'.format(similarPairsOfEvents, totalPairs, time.time()-start))

    
def writeIntegratedIncidentsAndEvents():
    
    w = open(path + 'AllEvents_Distinct.csv', 'w')    
    start= time.time()
       
    with open(path + 'AllEvents_EntireData.csv', 'r') as f:
        header = True
        for line in f:
            if header:
                w.write('EventId,Type(W/T),RefinedType,StartTime(UTC),EndTime(UTC),LocationLat,LocationLng,Distance(mi),AirportCode,Number,Street,Side,City,County,State,ZipCode\n')
                header = False
                continue
            parts = line.replace('\r', '').replace('\n', '').split(',')
            if parts[1] == 'W':
                events = airport_to_weather_event[parts[12]]
                e = events[parts[0]]
                refined = ('' if isinstance(parts[2], float) else parts[2]) + '-' + ('' if isinstance(parts[3], float) else parts[3])
                if e.toBeMerged == True:
                    continue
                if e.modified == False:
                    w.write(parts[0] + ',' + parts[1] + ',' + refined + ',' + parts[6] + ',' + parts[7] + ',' + 
                    parts[9] + ',' + parts[10] + ',' + parts[11] + ',' + parts[12] + ',' + parts[13] + ',' + parts[14] + ',' + 
                    parts[15] + ',' + parts[16] + ',' + parts[17] + ',' + parts[18] + ',' + parts[19] + '\n')
                else:
                    w.write(parts[0] + ',' + parts[1] + ',' + refined + ',')
                    w.write(e.startTime.strftime('%Y-%m-%d %H:%M:%S') + ',' + e.endTime.strftime('%Y-%m-%d %H:%M:%S'))
                    for i in range(9, len(parts)):
                        w.write(',' + parts[i])
                    w.write('\n')
            elif parts[1] == 'T':
                if parts[19] not in zip_to_traffic_event:
                    continue
                incidents = zip_to_traffic_event[parts[19]]                
                e = incidents[parts[0]]
                refined = ('' if isinstance(parts[2], float) else parts[2]) + '-' + ('' if isinstance(parts[3], float) else parts[3])
                if e.toBeMerged == True:
                    continue
                if e.modified == False:
                    w.write(parts[0] + ',' + parts[1] + ',' + refined + ',' + parts[6] + ',' + parts[7] + ',' + 
                    parts[9] + ',' + parts[10] + ',' + parts[11] + ',' + parts[12] + ',' + parts[13] + ',' + parts[14] + ',' + 
                    parts[15] + ',' + parts[16] + ',' + parts[17] + ',' + parts[18] + ',' + parts[19] + '\n')
                else:
                    w.write(parts[0] + ',' + parts[1] + ',' + refined + ',')
                    w.write(e.startTime.strftime('%Y-%m-%d %H:%M:%S') + ',' + e.endTime.strftime('%Y-%m-%d %H:%M:%S') + ',' +
                            parts[9] + ',' + parts[10] + ',' + str(e.distance))
                    for i in range(12, len(parts)):
                        w.write(',' + parts[i])
                    w.write('\n')
               
    w.close()
    print ('Distinct events/incidents are written in: %.1f sec'%(time.time()-start))
   

if __name__ == "__main__":  
    path = './data/'
    zipToAirport = loadZipToAirportCode()
    zip_to_traffic_event, airport_to_weather_event = loadEventData() 
    
    # Traffic Incident Processing
    integrateSimilarTrafficIncidents()
        
    # Weather Event Processing    
    wTimeThreshs = {'rain':15, 'snow':30, 'default':10}
    integrateSimilarWeatherEvents()
        
    # Writing Filtered Events and Incidents
    writeIntegratedIncidentsAndEvents()
    