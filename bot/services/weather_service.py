
import aiohttp
import html
from config import logger

# OpenWeatherMap API endpoint and key
from config import WEATHER_API_URL, WEATHER_API_KEY

async def get_weather(location: str) -> str:
    """Get current weather for a location"""
    logger.info(f"Getting weather for location: {location}")
    
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "q": location,
                "appid": WEATHER_API_KEY,
                "units": "metric"  # For Celsius
            }
            
            async with session.get(WEATHER_API_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"Weather API error: {response.status}")
                    return "Sorry, I couldn't get the weather information for that location."
                
                data = await response.json()
                
                # Extract relevant weather information
                city = data["name"]
                country = data["sys"]["country"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                
                # Format the response
                weather_info = (
                    f"🌦 <b>Weather for {html.escape(city)}, {html.escape(country)}</b>\n\n"
                    f"🌡 Temperature: {temp}°C\n"
                    f"🤔 Feels like: {feels_like}°C\n"
                    f"☁️ Conditions: {html.escape(description.capitalize())}\n"
                    f"💧 Humidity: {humidity}%\n"
                    f"💨 Wind speed: {wind_speed} m/s"
                )
                
                return weather_info
                
    except Exception as e:
        logger.error(f"Error getting weather: {str(e)}")
        return "Sorry, I couldn't get the weather information. Please try again later."
