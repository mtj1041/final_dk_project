from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from geopy.geocoders import GeocoderDotUS

locations = {'ATL': [33.45, -84.23],
'BOS' : [	42.21, -71.5],
'BRKLYN' : [40.69 -73.99],
'CHA' : [35.14, -80.50],
'CHI' : [41.50, -87.37],
'CLE' : [41.28, -81.37],
'DAL' : [32.46, -96.46],
'DEN' : [39.45, -105.0],
'DET' : [42.20, -83.3],
'GS' : [37.48, -122.16],
'HOU' : [29.45, -95.21],
'IND' : [39.46, -86.10],
'LAC' : [34.3, -118.15],
'LAL' : [34.3, -118.15],
'MEM' : [35.9, -90.3],
'MIA' : [25.46, -80.12],
'MIL' : [43.2, -87.55],
'MIN' : [44.59, -93.14],
'NO' : [29.57, -90.4],
'NY' : [40.47, -73.58],
'OKC' : [35.26, -97.28],
'ORL' : [28.41, -81.30],
'PHI' : [39.57, -75.10],
'PHO' : [33.29, -112.4],
'POR' : [43.40, -70.15],
'SAC' : [38.35, -121.30],
'SA' : [29.23, -98.33],
'TOR' : [43.40, -79.24],
'UTAH' : [40.46, -111.54],
'WSH' : [38.53, -77.02]}

def calculateDistance(Team1, Team2):
	
	return (great_circle(locations[Team1], locations[Team2]).miles)
