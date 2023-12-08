from math import sin, cos, asin, sqrt, radians
from json import loads
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool

graphhopper_host = 'host_of_server.com'
# pool = HTTPSConnectionPool(graphhopper_host, maxsize=1, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
pool = HTTPSConnectionPool(graphhopper_host, maxsize=1)

def distanceCrow(lat1, lon1, lat2, lon2):
    return 6372.8 * 2 * asin(sqrt(sin(radians(lat2 - lat1) / 2)**2 + sin(radians(lon2 - lon1) / 2)**2 * cos(radians(lat1)) * cos(radians(lat2))))

def distanceRoad(lat1, lon1, lat2, lon2):
    r = pool.request('GET', '/route', fields=[
      ('vehicle', 'custom_car'),
      ('calc_points', 'false'),
      ('instructions', 'false'),
      ('point', f'{lat1},{lon1}'),
      ('point', f'{lat2},{lon2}')
    ])
    j = loads(r.data)
    return j['paths'][0]['distance'] / 1000