from datetime import datetime, timedelta, timezone
import geocoder
import requests
import json


token = '7513f858e4b4774d2ea0a9b495d6d3ec'


def get_current_location_info():
    result = dict()
    try:
        gc = geocoder.ip("me")
        result["country"]   = gc.country
        result["city"]      = gc.city
        result["lat"]       = gc.latlng[0]
        result["lon"]       = gc.latlng[1]
        result["success"]   = True
        result["status"]    = 'Success'
    except:
        result["success"] = False;
        result["status"] = f'Error! Unable to get current location info'
    return result

def get_location_info(name : str):
    result = dict();
    
    # request location data from openweathermap server
    try:
        request_url = f'http://api.openweathermap.org/geo/1.0/direct?q={name}&limit={1}&appid={token}'
        timeout_sec = 5
        response: requests.Response = requests.get(request_url, timeout=timeout_sec)
    except requests.Timeout:
        result["success"] = False;
        result["status"] = f'Error! Timeout of {timeout_sec} exceeded'
        return result

    try:
        if response.status_code != 200:
            result["success"] = False;
            result["status"] = f'Server error! Server answered with code {response.status_code}'
            return result
        body = json.loads(response.content)
        if len(body) == 0:
            result["success"] = False;
            result["status"] = f'Query error! Unknow city name: "{name}"'
            return result

        body = body[0]
        result["country"]   = body["country"]
        result["city"]      = body["name"]
        result["lat"]       = body["lat"]
        result["lon"]       = body["lon"]
        result["success"]   = True
        result["status"]    = 'Success'
        
    except:
        result["success"] = False;
        result["status"] = f'Internal Error when detecting city!'
    
    return result



def get_weather(location_info):
    lat = location_info["lat"]
    lon = location_info["lon"]
    city_name = location_info["city"]
    country = location_info["country"]
    result = dict();
    
    # request weather data from openweathermap server
    try:
        units = 'metric'
        request_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units={units}'
        timeout_sec = 5
        response: requests.Response = requests.get(request_url, timeout=timeout_sec)
    except requests.Timeout:
        result["success"] = False;
        result["status"] = f'Error! Timeout of {timeout_sec} exceeded'
        return result

    # parse response
    try:
        if response.status_code != 200:
            result["success"] = False;
            result["status"] = f'Server error! Server answered with code {response.status_code}'
            return result
        
        body = json.loads(response.content)
        weather = dict()
        weather["main"]        = body["weather"][0]["main"]
        weather["description"] = body["weather"][0]["description"]
        weather["temp_actual"] = body["main"]["temp"]
        weather["temp_feels"]  = body["main"]["feels_like"]
        weather["wind_speed"]  = body["wind"]["speed"]
        
        result["weather"]   = weather
        result["timestamp"] = body["dt"]
        result["timezone"]  = body["timezone"]
        result["city"]      = f'{city_name}, {country}'
        result["date"]      = response.headers["Date"]
        result["success"]   = True
        result["status"]    = 'Success'
        
    except:
        result["success"] = False;
        result["status"] = f'Internal Error when parsing weather!'

    return result


def get_weather_result(result):
    local_delta = timedelta(seconds=result["timezone"])
    local_tz = timezone(local_delta)
    local_dt = datetime.fromtimestamp(result["timestamp"], tz=local_tz)
    lines = [
        f'* Local time:   {local_dt.strftime("%d-%m-%Y %H:%M:%S %Z")}',
        f'* City:         {result["city"]}',
        f'* Weather:      {result["weather"]["main"]} ({result["weather"]["description"]})',
        f'* Temperature: {result["weather"]["temp_actual"] : .0f}°C',
        f'* Feels like   {result["weather"]["temp_feels"] : .0f}°C',
        f'* Wind speed:   {result["weather"]["wind_speed"]} m/sec'
    ]
    message = '\n'.join(lines)
    return message

