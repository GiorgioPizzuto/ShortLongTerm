'''
Created on May 6, 2018 - Modified on June 4'th 2018 (minor modification)
This script is to combine weather and traffic events data. 
Traffic: EventId, Type(T/W), RefinedType, StartTime(UTC), EndTime(UTC), LocationLat, LocationLng, Distance(mi), AirportCode, ZipCode, Number, Street, County, City, State
Weather: EventId, Type(W/T), RefinedType, StartTime(UTC), EndTime(UTC), AirportCode
@author: moosas1
'''
import random

main_path = './data/'
traffic_path = './data/'
files = ['WeatherEvents_Aug16_June20_Publish', 'TrafficEvents_Aug16_June20_Publish']


writer = open(main_path + 'AllEvents_EntireData.csv', 'w')
writer.write('EventId,Type(W/T),RefinedType,                        StartTime(UTC),         EndTime(UTC),              LocationLat,LocationLng,Distance(mi),AirportCode,Number,Street,Side,City,County,State,ZipCode\n')
#               0        1          2                                     3                     4                            5          6           7           8         9      10    11   12   13     14     15
#             'EventId Source  Type Severity  TMC  Description       StartTime(UTC)         EndTime(UTC)     TimeZone  LocationLat  LocationLng  Distance(mi) AirportCode  Number  Street  Side      City    County State  ZipCode'
##               0       1       2     3       4       5                  6                     7               8          9           10           11           12           13     14     15        16       17     18      19

weatherId = set()
trafficId = set()
noZip = 0

for f in files:
    header= False
    traffic = False
    if 'Weather' in f: path = main_path + f + '.csv'
    else: 
        path = traffic_path + f + '.csv'
        traffic = True
    with open(path, 'r') as lines:
        for r in lines:
            if header is not True:
                header= True
                continue
            parts = r.replace('\r', '').replace('\n', '').split(',')
            
            if traffic:  #this is traffic event file
                rnd = random.random()
                if rnd < 0:
                    continue
                id = len(trafficId) + 1
                if len(parts[25]) == 0:
                    parts[25] = 'N/A'
                else:
                    parts[25] = parts[25].split('-')[0]
                writer.write('T-' + str(id) + ',T,' + parts[1] + '-' + parts[2] + ',' + parts[5] + ',' + parts[6] + ',' + parts[8] + ',' + parts[9] + ',' + parts[10] + ',' + parts[11] +
                             ',' + parts[12] + ',' + parts[13] + ',' + parts[14] + ',' + parts[15] + ',' + parts[16] + ',' + parts[17] + ',' + parts[18] + '\n')
                trafficId.add(id)
                
            else:  #This is weather event file
                rnd = random.random()
                if rnd < 0:
                    continue
                id = len(weatherId) + 1
                writer.write('W-' + str(id) + ',W,' + parts[1] + '-' + parts[2] + ',' + parts[3] + ',' + parts[4] + ',' + parts[6] + ',' + parts[7] + ',N/A,' + parts[8] + ',N/A,N/A,N/A,'
                            + parts[9] + ',' + parts[10] + ',' + parts[11] + ',' + parts[12] + '\n')
                weatherId.add(id)
            
                
    print('Done by "%s"' % (f))
              
writer.close()

print ('Max Weather ID: %s, Max Traffic ID: %s' % (len(weatherId), len(trafficId)))
                