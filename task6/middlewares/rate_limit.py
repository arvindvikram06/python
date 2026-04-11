from fastapi import Request, Response
from rate_limiter import rate_limiter

async def rate_limit_middleware(request: Request, call_next):

    api_key = request.headers.get("x-api-key")

    if not api_key:
        return Response(content="Missing API Key", status_code=401)

    if not rate_limiter.is_allowed(api_key):
        return Response(content="Rate limit exceeded", status_code=429)

    request.state.api_key = api_key

    return await call_next(request)