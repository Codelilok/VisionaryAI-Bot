import aiohttp
from config import NEWSAPI_KEY, NEWSAPI_URL

async def get_news(topic: str) -> str:
    async with aiohttp.ClientSession() as session:
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": topic,
            "language": "en",
            "pageSize": 5
        }
        
        async with session.get(f"{NEWSAPI_URL}everything", params=params) as response:
            if response.status != 200:
                raise Exception("Failed to fetch news")
            
            data = await response.json()
            
            if data["status"] != "ok":
                raise Exception("News API error")
            
            articles = data["articles"]
            
            news_text = f"📰 Latest news about {topic}:\n\n"
            for i, article in enumerate(articles, 1):
                news_text += (
                    f"{i}. <b>{article['title']}</b>\n"
                    f"<i>{article['description']}</i>\n"
                    f"<a href='{article['url']}'>Read more</a>\n\n"
                )
            
            return news_text
