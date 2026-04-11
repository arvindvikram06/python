from fastapi import FastAPI ,Request 
from fastapi.responses import Response

from router import get_target_service

from services.proxy import forward_request

from rate_limiter import rate_limiter

app = FastAPI()

@app.api_route("/api/{fullpath:path}",methods=["GET","POST","PUT","DELETE"])

async def gateway(request:Request,fullpath:str):

    api_key = request.headers.get("x-api-key")
    
    if not api_key:
        return Response(content="Missing API Key", status_code=401)
    
    if not rate_limiter.is_allowed(api_key):
        return Response(
            content="Rate limit exceeded",
            status_code=429
        )

    target_url = get_target_service("/api/" + fullpath)

    if not target_url:
        return Response(content = "Service not found" , status_code = 404)

    body = await request.body()

    response = await forward_request(
        method = request.method,
        url = target_url,
        headers = dict(request.headers),
        body=body
    )

    return Response(
        content = response.content,
        status_code = response.status_code,
        headers=dict(response.headers)

    )