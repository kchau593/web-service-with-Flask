#Empower Web Service Coding Challenge
#Kevin Chau

#imports
from flask import Flask, request
import requests, time

#create the web app
app = Flask(__name__)

#URL related
azure_map_key = "key for azure api"
get_driver_URL = "URL with code to get the driver locations"


@app.route('/')
def index():
    """
    Home Page

    Returns:
       Text letting user know that service is running
    """
    return "This is dispatch closest driver web service"


@app.route('/api/dispatch-closest-driver',methods = ['POST'])
def dispatch_closest_driver():
    """
    Displatch closest driver route
    Finds the closest available driver using a query string that contains longitude/latitude and returns their information

    Returns:
       dict: returns id of driverId and their distance from the inputted lon/lat
    """
    #get lon and lat from query string
    args = request.args
    lon = args.get('lon')
    lat = args.get('lat')

    if not lon or not lat:
        return "Incorrect query string received. A lon and lat must be passed", 200
    else:
        #
        return  getClosestDriver(lon,lat)


def getClosestDriver(lon:float, lat:float) -> dict:
    """
    Gets the closest driver to the origin longitude and latitude via distance

    Args:
        lon (float): longitude of the origin
        lat (float): latitude of the origin

    Returns:
        dict: driverId and the distance between the driver and origin
    """
    global azure_map_key, get_driver_URL

    #Get drivers and convert them into a dictionary/map with id being key and lon/lat being the value
    response = requests.get(get_driver_URL)
    # drivers = {}
    closest_driverid = ''
    closest_dist = float('inf')


    # start_time = time.time() #used to keep track of performance

    #get the shortest distance between the origin and each driver
    for driver in response.json(): #make sure you add ".json() to get the correct format"
        driver_dist = getShortestRoute(lon, lat,driver['lon'],driver['lat'])

        #update the clostest driver to the origin based on distance
        if driver_dist < closest_dist:
            closest_dist = driver_dist
            closest_driverid = driver['id']

    #check performance time ~ 40 sec
    # print("--- %s seconds ---" % (time.time() - start_time))

    return {'driverId':closest_driverid,'distance':closest_dist}


def getShortestRoute(orig_lon:float, orig_lat:float,dest_lon:float,dest_lat:float)->int:
    """[summary]

    Args:
        orig_lon (float): longitude of origin
        orig_lat (float): latitude of origin
        dest_lon (float): longitude of destination
        dest_lat (float): latitude of destination

    Returns:
        int: shortest distance between origin and destination
    """

    # sample.. format is {orig-lat}, {orig-lon}:{dest-lat},{dest-lon} -> '52.50931,13.42936:52.50274,13.43872'
    get_route_url = 'https://atlas.microsoft.com/route/directions/json?subscription-key={}&api-version=1.0&query={},{}:{},{}'.format(\
        azure_map_key,str(orig_lat),str(orig_lon),str(dest_lat),str(dest_lon))
    route_response_summary = requests.get(get_route_url).json()

    shortest_dist = float('inf') #initialized to high dist

    #get the shortest dist out of all of the listed routes
    if 'routes' in route_response_summary: #check if there exists a route
        for route in route_response_summary['routes']:
            shortest_dist = min(route['summary']['lengthInMeters'], shortest_dist)

    return shortest_dist


#starts the app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0') #run the app
    