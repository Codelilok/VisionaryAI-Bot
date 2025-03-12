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
import aiohttp
from config import NEWSAPI_KEY, NEWSAPI_URL, logger
from bot.utils import sanitize_message

async def get_news(topic: str) -> str:
    """Get latest news on a specific topic"""
    async with aiohttp.ClientSession() as session:
        params = {
            'q': topic,
            'apiKey': NEWSAPI_KEY,
            'language': 'en',
            'pageSize': 5
        }
        
        try:
            logger.info(f"Fetching news about: {topic}")
            async with session.get(
                f"{NEWSAPI_URL}everything", 
                params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"News API request failed: {error_text}")
                    raise Exception("Failed to fetch news")
                
                data = await response.json()
                
                if data.get('status') != 'ok':
                    logger.error(f"News API returned error: {data.get('message')}")
                    raise Exception(f"News API error: {data.get('message')}")
                
                articles = data.get('articles', [])
                
                if not articles:
                    return f"No news found for '{topic}'. Try another topic?"
                
                news_text = f"<b>Latest news about '{sanitize_message(topic)}':</b>\n\n"
                
                for i, article in enumerate(articles[:5], 1):
                    title = sanitize_message(article.get('title', 'No title'))
                    source = sanitize_message(article.get('source', {}).get('name', 'Unknown source'))
                    url = article.get('url', '')
                    
                    news_text += f"{i}. <a href='{url}'>{title}</a> - {source}\n\n"
                
                return news_text
                
        except Exception as e:
            logger.error(f"Error in get_news: {str(e)}")
            raise Exception(f"Failed to fetch news: {str(e)}")
