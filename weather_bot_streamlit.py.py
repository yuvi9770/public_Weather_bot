import streamlit as st
import requests

API_KEY = "c98e5ca2351846e8b9e150154231109"

class WeatherBot:
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
    
    def get_current_weather(self, city):
        endpoint = f"/current.json?key={API_KEY}&q={city}&aqi=no"
        data = self.make_request(endpoint)
        if isinstance(data, str):
            return data

        temperature_celsius = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data['current']['humidity']
        return f"Current temperature in {city}: {temperature_celsius}°C, Condition: {condition}, Humidity: {humidity}%."

    def get_14_day_forecast(self, city):
        endpoint = f"/forecast.json?key={API_KEY}&q={city}&days=14&aqi=no"
        data = self.make_request(endpoint)
        if isinstance(data, str):
            return data

        forecast_data = data["forecast"]["forecastday"]
        forecast_text = ""
        for day in forecast_data:
            date = day["date"]
            max_temp_celsius = day["day"]["maxtemp_c"]
            min_temp_celsius = day["day"]["mintemp_c"]
            condition = day["day"]["condition"]["text"]
            forecast_text += f"Date: {date}, Max Temp: {max_temp_celsius}°C, Min Temp: {min_temp_celsius}°C, Condition: {condition}\n"
        return forecast_text

    def get_time_zone(self, city):
        endpoint = f"/timezone.json?key={API_KEY}&q={city}"
        data = self.make_request(endpoint)
        if isinstance(data, str):
            return data

        time_zone_data = data["location"]["tz_id"]
        return f"Time zone for {city}: {time_zone_data}"

    def get_location_data(self, city):
        endpoint = f"/search.json?key={API_KEY}&q={city}"
        data = self.make_request(endpoint)
        if isinstance(data, str):
            return data

        location_data = data[0] 
        if not location_data:
            return f"No location data available for {city}."

        location_text = "Location Data:\n"
        location_name = location_data.get("name", "N/A")
        location_country = location_data.get("country", "N/A")
        location_region = location_data.get("region", "N/A")
        location_latitude = location_data.get("lat", "N/A")
        location_longitude = location_data.get("lon", "N/A")
        location_text += f"Name: {location_name}\nCountry: {location_country}\nRegion: {location_region}\nLatitude: {location_latitude}\nLongitude: {location_longitude}"
        return location_text

    def get_air_quality_data(self, city):
        endpoint = f"/current.json?key={API_KEY}&q={city}&aqi=yes"
        data = self.make_request(endpoint)
        if isinstance(data, str):
            return data

        air_quality_data = data.get("current", {}).get("air_quality", {})
        if not air_quality_data:
            return f"No air quality data available for {city}."

        air_quality_text = "Air Quality Data:\n"
        air_quality_text += f"CO: {air_quality_data.get('co', 'N/A')} µg/m³\n"
        air_quality_text += f"NO2: {air_quality_data.get('no2', 'N/A')} µg/m³\n"
        air_quality_text += f"O3: {air_quality_data.get('o3', 'N/A')} µg/m³\n"
        air_quality_text += f"SO2: {air_quality_data.get('so2', 'N/A')} µg/m³\n"
        air_quality_text += f"PM2.5: {air_quality_data.get('pm2_5', 'N/A')} µg/m³\n"
        air_quality_text += f"PM10: {air_quality_data.get('pm10', 'N/A')} µg/m³\n"
        air_quality_text += f"us-epa-index: {air_quality_data.get('us-epa-index', 'N/A')}\n"
        air_quality_text += f"GB DEFRA Index: {air_quality_data.get('gb-defra-index', 'N/A')}\n"
        return air_quality_text

    def make_request(self, endpoint):
        full_url = self.base_url + endpoint
        response = requests.get(full_url)
        data = response.json()
        if 'error' in data:
            return f"Sorry, I couldn't retrieve the information. Error: {data['error']['message']}"
        return data

# Streamlit UI
def main():
    st.title("WeatherBot")

    city = st.text_input("Enter city:")
    choice = st.selectbox("Choose an option:", ["Current Weather", "14-Day Weather Forecast", "Time Zone", "Location Data", "Air Quality Data"])

    weather_bot = WeatherBot()
    if st.button("Get Data"):
        if choice == "Current Weather":
            result = weather_bot.get_current_weather(city)
        elif choice == "14-Day Weather Forecast":
            result = weather_bot.get_14_day_forecast(city)
        elif choice == "Time Zone":
            result = weather_bot.get_time_zone(city)
        elif choice == "Location Data":
            result = weather_bot.get_location_data(city)
        elif choice == "Air Quality Data":
            result = weather_bot.get_air_quality_data(city)
        else:
            result = "Invalid choice"
        st.text(result)

    if st.button("Clear"):
        city = ""
        st.text("")

    if st.button("About WeatherBot"):
        st.info("WeatherBot GUI\nVersion 1.0\nCreated by Yuvraj")

if __name__ == "__main__":
    main()