from fastapi import Request, Response
from cache import cache

async def cache_middleware(request: Request, call_next):

    if request.method != "GET":
        return await call_next(request)

    api_key = request.state.api_key
    cache_key = f"{api_key}:{request.url.path}"

    cached = await cache.get(cache_key)

    if cached:
        print("CACHE HIT")
        return Response(
            content=cached["body"],
            status_code=cached["status"],
            headers=cached["headers"]
        )

    response = await call_next(request)

    if response.status_code == 200:
        print("CACHE MISS (storing)")
        await cache.set(
            cache_key,
            {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response.body.decode() if response.body else ""
            },
            ttl=60
        )

    return response