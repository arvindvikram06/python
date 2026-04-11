from fastapi import FastAPI, Request
from fastapi.responses import Response

from router import get_target_service
from services.proxy import forward_request

from rate_limiter import rate_limiter
from cache import cache
from circuit_breaker import circuit_manager

app = FastAPI()


@app.api_route("/api/{fullpath:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, fullpath: str):

    
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return Response(content="Missing API Key", status_code=401)

    
    if not rate_limiter.is_allowed(api_key):
        return Response(content="Rate limit exceeded", status_code=429)

    
    cache_key = f"{api_key}:{request.url.path}"

    
    if request.method == "GET":
        cached = await cache.get(cache_key)
        if cached:
            print("CACHE HIT")
            return Response(
                content=cached["body"],
                status_code=cached["status"],
                headers=cached["headers"]
            )

    
    target_url = get_target_service("/api/" + fullpath)
    if not target_url:
        return Response(content="Service not found", status_code=404)

   
    service_name = fullpath.split("/")[0]
    breaker = circuit_manager.get_breaker(service_name)

   
    if not breaker.can_request():
        return Response(
            content="Service temporarily unavailable (circuit open)",
            status_code=503
        )

    
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    
    try:
        response = await forward_request(
            method=request.method,
            url=target_url,
            headers=headers,
            body=body
        )

       
        if response.status_code < 500:
            breaker.record_success()
        else:
            breaker.record_failure()

    except Exception:
        breaker.record_failure()
        return Response(
            content="Downstream service error",
            status_code=503
        )

   
    if request.method == "GET" and response.status_code == 200:
        print("CACHE MISS (storing)")
        await cache.set(
            cache_key,
            {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response.text
            },
            ttl=60
        )

    
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )