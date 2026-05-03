# Async API Gateway

A lightweight **asynchronous API Gateway** built using **FastAPI** that routes client requests to downstream microservices while providing essential infrastructure features.

---

## Features

- **Dynamic Reverse Proxying**
  - Routes requests to multiple downstream services based on URL patterns.
  
- **Token-Bucket Rate Limiting**
  - Prevents abuse by limiting the number of requests per API key.

- **Distributed Caching**
  - Integrated with **Redis** to cache responses and reduce downstream load.
  - Configurable TTL (Time-to-Live) for cached data.

- **Circuit Breaker Pattern**
  - Automatically detects service failures and "opens" the circuit to prevent cascading failures.
  - Implements a recovery mechanism to "close" the circuit once services are healthy.

- **Middleware-based Architecture**
  - Clean separation of concerns using FastAPI middleware for cross-cutting interests.

---

## Tech Stack

- **Python 3**
- **FastAPI**
- **httpx** (Asynchronous HTTP client)
- **Redis**
- **Asyncio**

---

## Project Workflow

1. **Client Request**: A client sends a request to the Gateway.
2. **Rate Limiter**: The Gateway checks if the client has exceeded their request quota.
3. **Cache Lookup**: If allowed, the Gateway checks Redis for a cached version of the response.
4. **Circuit Breaker**: If no cache is found, the system checks the health of the downstream service.
5. **Proxy Execution**: If healthy, the request is proxied to the microservice using `httpx`.
6. **Response Processing**: The response is optionally cached in Redis and returned to the client.

---

## Gateway Logic

- **Circuit Breaker**: Tracks error rates over time. If a threshold is met, it stops forwarding requests to that service for a cooling-off period.
- **Reverse Proxy**: Uses `httpx.AsyncClient` to maintain connection pools and handle streaming responses.

---

## Installation

```bash
# Ensure Redis is running
redis-server

# Install dependencies
pip install fastapi uvicorn httpx redis

# Start the gateway
uvicorn main:app --reload
```
