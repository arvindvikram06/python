from fastapi import FastAPI, Request
from fastapi.responses import Response

from router import get_target_service
from services.proxy import forward_request

from middlewares.rate_limit import rate_limit_middleware
from middlewares.cache import cache_middleware
from middlewares.circuit import circuit_middleware

app = FastAPI()

app.middleware("http")(rate_limit_middleware)
app.middleware("http")(cache_middleware)
app.middleware("http")(circuit_middleware)


@app.api_route("/api/{fullpath:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, fullpath: str):

    target_url = get_target_service("/api/" + fullpath)

    if not target_url:
        return Response(content="Service not found", status_code=404)

    body = await request.body()

    headers = dict(request.headers)
    headers.pop("host", None)

    response = await forward_request(
        method=request.method,
        url=target_url,
        headers=headers,
        body=body
    )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )