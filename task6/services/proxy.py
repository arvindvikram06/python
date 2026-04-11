import httpx


async def forward_request(method,url,headers,body):
    async with httpx.AsyncClient() as Client:
        response = await Client.reques(
            method = method,
            url = url,
            headers = headers,
            body = body
        )
        return response

