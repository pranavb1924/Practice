import requests
import json
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import random


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

API_KEY = "bd5e378503939ddaee76f12ad7a97608" 

def get_weather(city_name):

    url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city_name,     
        'appid': API_KEY,    
        'units': 'metric'    
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:

            data = response.json()
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed']
            }
            
            return weather_info
        else:
            return {'error': 'City not found'}
            
    except Exception as e:
        return {'error': str(e)}

@app.route('/weather/<city>')
def weather_api(city):

    weather_data = get_weather(city)
    return jsonify(weather_data)

def get_weather_multiple_cities():
    from concurrent.futures import ThreadPoolExecutor
    import time
    
    cities = ["London", "Paris", "New York", "Tokyo", "Sydney"]
    
    print("Getting weather for multiple cities...")
    print("-" * 40)
    
    start_time = time.time()
    results_sequential = []
    for city in cities:
        results_sequential.append(get_weather(city))
    sequential_time = time.time() - start_time
    
    print(f"Sequential processing took: {sequential_time:.2f} seconds")
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results_parallel = list(executor.map(get_weather, cities))
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing took: {parallel_time:.2f} seconds")
    print(f"Speed improvement: {sequential_time/parallel_time:.1f}x faster!")
    
    # Print results
    print("\nWeather Results:")
    print("-" * 40)
    for weather in results_parallel:
        if 'error' not in weather:
            print(f"{weather['city']}: {weather['temperature']}°C - {weather['description']}")


if __name__ == "__main__":
    print("Starting weather API server...")
    print("Open weather.html in your browser to use the frontend")
    print("API endpoint: http://localhost:5008/weather/<city_name>")
    print("-" * 40)
    app.run(debug=True, port=5008)