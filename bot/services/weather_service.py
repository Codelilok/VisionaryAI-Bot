
import aiohttp
import json
from config import logger, WEATHER_API_KEY, WEATHER_API_URL

async def get_weather(location: str) -> str:
    """Get current weather for a location"""
    try:
        if not location:
            return "Please provide a location to check the weather."
        
        # Make API request
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL, params=params) as response:
                if response.status != 200:
                    return f"Sorry, I couldn't find weather data for {location}. Please check the spelling and try again."
                
                data = await response.json()
                
                # Extract relevant weather information
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                
                # Format weather information
                weather_info = (
                    f"🌍 <b>Weather for {data['name']}, {data.get('sys', {}).get('country', '')}</b>\n\n"
                    f"🌤 <b>Condition:</b> {weather_description.capitalize()}\n"
                    f"🌡 <b>Temperature:</b> {temperature}°C\n"
                    f"🌡 <b>Feels like:</b> {feels_like}°C\n"
                    f"💧 <b>Humidity:</b> {humidity}%\n"
                    f"💨 <b>Wind speed:</b> {wind_speed} m/s"
                )
                
                return weather_info
                
    except Exception as e:
        logger.error(f"Error getting weather: {str(e)}")
        return "Sorry, I couldn't get the weather information. Please try again later."
