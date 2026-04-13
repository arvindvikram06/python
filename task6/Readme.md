#  Async API Gateway

## Description
A lightweight **asynchronous API Gateway** built using FastAPI that routes client requests to downstream microservices.  
It includes core production-grade features such as **rate limiting**, **Redis-based caching**, and **circuit breaker** for fault tolerance.

This project demonstrates how real-world gateways manage traffic, improve performance, and handle service failures gracefully.

---

##  Tech Stack
- **FastAPI** — Web framework  
- **httpx** — Async HTTP client (reverse proxy)  
- **Redis (redis.asyncio)** — Distributed caching  
- **Python asyncio** — Non-blocking concurrency  
- **Custom Middleware** — Rate limiting, caching, circuit breaker  

---

## 🔄 Request Flow
Client Request
↓
[ Rate Limiter ]
↓
[ Cache (Redis) ]
↓
[ Circuit Breaker ]
↓
[ Reverse Proxy ]
↓
Microservices


##  Features
-  Dynamic routing (`/api/users`, `/api/orders`, etc.)
-  Token-bucket rate limiting (per API key)
-  Redis caching with TTL
-  Circuit breaker for failure handling
-  Middleware-based architecture

