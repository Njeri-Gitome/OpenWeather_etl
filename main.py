import json
from datetime import datetime
import pandas as pd
import requests

city_name = 'Nyeri'
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

with open("credentials.txt",'r') as f: #opening the credentials.txt file in read mode
    api_key = f.read()
    
    
# url to obtail weather data
full_url = base_url + city_name + "&appid=" + api_key

#convert temperature from kelvin to celsius
def kelvin_to_celsius(temp_in_kelvin):
    temp_in_celsius = temp_in_kelvin - 273
    return temp_in_celsius
    

#fetching data from api
def etl_weather_data(url):    
    r = requests.get(url)
    data = r.json()

    # Features in the weather data
    city = data['name']
    weather_description = data['weather'][0]['description']
    temp= kelvin_to_celsius(data['main']['temp'])
    feels_like = kelvin_to_celsius (data['main']['feels_like'])
    min_temp = kelvin_to_celsius (data['main']['temp_min'])
    max_temp = kelvin_to_celsius (data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone']) # convert a Unix timestamp into a UTC datetime object
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])


    # data in dictionary 
    transformed_data = {
        "City": city,
        "Description":weather_description,
        "Temperature (C)":temp,
        "Feels Like": feels_like,
        "Minimum Temp (C)": min_temp,
        "Maximum Temp (C)": max_temp,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Time_of_Record": time_of_record,
        "Sunrise": sunrise_time,
        "Sunset": sunset_time
        
    }

    # Convert dict into list then to dataframe
    transformed_data_list =[transformed_data]
    df_data = pd.DataFrame(transformed_data_list)
    print(df_data)

    #Save the data in a csv file
    df_data.to_csv('current_weather_data_nyeri.csv', index = False)
    
# Function call 
if __name__ == "__main__":
    etl_weather_data(full_url)