import aiohttp
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from app.configs.config import settings


async def fetch_news_rss(topic: str, max_items: int = 5):
    url = settings.NEWS_RSS_BASE + quote_plus(topic)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=20) as resp:
            text = await resp.text()

    root = ET.fromstring(text)
    items = []
    for item in root.findall('.//item')[:max_items]:
        title = item.find('title').text if item.find('title') is not None else ''
        desc = item.find('description').text if item.find('description') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        pub = item.find('pubDate').text if item.find('pubDate') is not None else ''
        items.append({"title": title, "summary": desc, "link": link, "published": pub})
    return items