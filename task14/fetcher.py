 import aiohttp
import time

async def fetch(session, url):
    start = time.time()

    try:
        async with session.get(url, allow_redirects=True, timeout=10) as response:
            html = await response.text()
            end = time.time()

            return {
                "status": response.status,
                "html": html,
                "time": round(end - start, 2),
                "redirects": [str(r.url) for r in response.history],
                "final_url": str(response.url)
            }

    except Exception:
        return {
            "status": None,
            "html": None,
            "time": 0,
            "redirects": [],
            "final_url": url
        }