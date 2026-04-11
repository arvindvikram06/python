from fastapi import FastAPI ,Request 
from fastapi.responses import Response

from router import get_target_service

from services.proxy import forward_request

app = FastAPI()

@app.api_route("/api/{fullpath:path}",methods=["GET","POST","PUT","DELETE"])

async def gateway(request:Request,fullpath:str):

    target_url = get_target_service("/api/" + fullpath)

    if not target_url:
        return Response(content = "Service not found" , statusch_code = 404)

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