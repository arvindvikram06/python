import httpx


async def forward_request(method,url,headers,body):
    async with httpx.AsyncClient() as Client:
        response = await Client.request(
            method = method,
            url = url,
            headers = headers,
            content = body
        )
        return response

