import pygeoip
import os
import json
from flask import make_response
import requests
import random


def generate_code():
    k = ""
    while len(k) < 6:
        k += random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I",
                            "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                            "S", "T", "U", "Y", "V", "X", "W", "Z", "0",
                            "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    return k.upper()


def root_dir():
    """ Returns root directory for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/.'))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


def geo_locate(ip):
    if ip in ["0.0.0.0", "127.0.0.1"]:
        response = requests.get("https://ipapi.co/json/")
        data = response.json()
    else:
        g = pygeoip.GeoIP('GeoLiteCity.dat')
        data = g.record_by_addr(ip) or {}

    city = data.get("city")
    region_code = data.get("region_code")
    country = data.get("country_code")
    country_name = data.get("country_name")
    region = data.get("region")
    lon = data.get("longitude", 0)
    lat = data.get("latitude", 0)
    timezone = data.get("timezone")

    region_data = {"code": region_code, "name": region, "country": {
        "code": country, "name": country_name}}
    city_data = {"code": city, "name": city, "state": region_data,
                 "region": region_data}
    timezone_data = {"code": timezone, "name": timezone,
                     "dstOffset": 3600000,
                     "offset": -21600000}
    coordinate_data = {"latitude": float(lat),
                       "longitude": float(lon)}
    location_data = {"city": city_data, "coordinate": coordinate_data,
                     "timezone": timezone_data}
    return location_data


def location_dict(city="", region_code="", country_code="",
             country_name="", region="", longitude=0, latitude=0,
             timezone=""):
    region_data = {"code": region_code, "name": region,
                        "country": {
                            "code": country_code,
                            "name": country_name}}
    city_data = {"code": city, "name": city,
                      "state": region_data,
                      "region": region_data}
    timezone_data = {"code": timezone, "name": timezone,
                          "dstOffset": 3600000,
                          "offset": -21600000}
    coordinate_data = {"latitude": float(latitude),
                            "longitude": float(longitude)}
    return {"city": city_data,
                          "coordinate": coordinate_data,
                          "timezone": timezone_data}
