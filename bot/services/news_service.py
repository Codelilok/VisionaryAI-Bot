import aiohttp
from config import NEWSAPI_KEY, NEWSAPI_URL, logger
import html

async def get_news(topic: str = "technology") -> str:
    """
    Fetch news articles based on a topic

    Args:
        topic: The news topic to search for

    Returns:
        A formatted string with news headlines and links
    """
    logger.info(f"Fetching news about {topic}")

    async with aiohttp.ClientSession() as session:
        params = {
            "q": topic,
            "apiKey": NEWSAPI_KEY,
            "language": "en",
            "pageSize": 5
        }

        async with session.get(f"{NEWSAPI_URL}everything", params=params) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"News API error: {error_text}")
                raise Exception(f"Failed to fetch news: {response.status}")

            data = await response.json()

            if data.get("status") != "ok" or not data.get("articles"):
                logger.warning(f"No news found for topic: {topic}")
                return f"I couldn't find any news about {topic}. Try a different topic?"

            articles = data["articles"]

            # Format the news results
            result = f"📰 <b>Latest news about {html.escape(topic)}</b>\n\n"

            for i, article in enumerate(articles[:5], 1):
                title = html.escape(article["title"])
                url = article["url"]
                source = html.escape(article["source"]["name"])

                result += f"{i}. <b>{title}</b>\n"
                result += f"   Source: {source}\n"
                result += f"   <a href='{url}'>Read more</a>\n\n"

            return result