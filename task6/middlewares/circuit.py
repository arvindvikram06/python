from fastapi import Request, Response
from circuit_breaker import circuit_manager

async def circuit_middleware(request: Request, call_next):

    path_parts = request.url.path.split("/")

    if len(path_parts) < 3:
        return await call_next(request)

    service_name = path_parts[2]
    breaker = circuit_manager.get_breaker(service_name)

    if not breaker.can_request():
        return Response(
            content="Service temporarily unavailable (circuit open)",
            status_code=503
        )

    try:
        response = await call_next(request)

        if response.status_code < 500:
            breaker.record_success()
        else:
            breaker.record_failure()

        return response

    except Exception:
        breaker.record_failure()
        return Response(
            content="Downstream service error",
            status_code=503
        )