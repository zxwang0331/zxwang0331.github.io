from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace with your Tomorrow.io API key
TOMORROW_IO_API_KEY = 'iyFuaKiIYstyKXalAHEUeB14GwWNV83c'


@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude parameters'}), 400

    # 构建 Tomorrow.io API 的 URL
    # url = f'https: // api.tomorrow.io/v4/timelines?\
    #        location={lat}, {lon} &\
    #        fields=temperature, temperatureApparent, temperatureMin,\
    #        temperatureMax, windSpeed, windDirection,\
    #        humidity, pressureSeaLevel, uvIndex,\
    #        weatherCode, precipitationProbability, precipitationType,\
    #        sunriseTime, sunsetTime, visibility, moonPhase, cloudCover &\
    #        timesteps=current &\
    #        timezone=America/Los_Angeles &\
    #        units=imperial &\
    #        apikey={TOMORROW_IO_API_KEY}'
    # sunriseTime,sunsetTime,visibility,moonPhase,cloudCover
    cur_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,temperatureApparent,temperatureMin,temperatureMax,windSpeed,windDirection,humidity,pressureSeaLevel,uvIndex,weatherCode,precipitationProbability,precipitationType,visibility,cloudCover&timesteps=current&timezone=America/Los_Angeles&units=imperial&apikey={TOMORROW_IO_API_KEY}'

    days_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,temperatureApparent,temperatureMin,temperatureMax,windSpeed,windDirection,humidity,pressureSeaLevel,uvIndex,weatherCode,precipitationProbability,precipitationType,visibility,cloudCover&timesteps=1d&timezone=America/Los_Angeles&units=imperial&apikey={TOMORROW_IO_API_KEY}'

    hourly_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,temperatureApparent,temperatureMin,temperatureMax,windSpeed,windDirection,humidity,pressureSeaLevel,uvIndex,weatherCode,precipitationProbability,precipitationType,visibility,cloudCover&timesteps=1h&timezone=America/Los_Angeles&units=imperial&apikey={TOMORROW_IO_API_KEY}'

    try:
        cur_response = requests.get(cur_url)
        cur_response.raise_for_status()
        cur_weather_data = cur_response.json()

        days_response = requests.get(days_url)
        days_response.raise_for_status()
        days_weather_data = days_response.json()

        hourly_response = requests.get(hourly_url)
        hourly_response.raise_for_status()
        hourly_weather_data = hourly_response.json()

        weather_data = {
            'cur_weather_data': cur_weather_data,
            'days_weather_data': days_weather_data,
            'hourly_weather_data': hourly_weather_data
        }

        return jsonify(weather_data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_weather_detail', methods=['GET'])
def get_weather_detail():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude parameters'}), 400

    days_url = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,temperatureApparent,temperatureMin,temperatureMax,windSpeed,windDirection,humidity,pressureSeaLevel,uvIndex,weatherCode,precipitationProbability,precipitationType,visibility,cloudCover,sunriseTime,sunsetTime&timesteps=1d&timezone=America/Los_Angeles&units=imperial&apikey={TOMORROW_IO_API_KEY}'

    try:

        days_response = requests.get(days_url)
        days_response.raise_for_status()
        days_weather_data = days_response.json()

        return jsonify(days_weather_data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def home():
    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True)
