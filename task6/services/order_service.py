from fastapi import FastAPI

app = FastAPI()


@app.get("/{order_id}")
async def get_order(order_id: int):
    return {
        "service": "order-service",
        "order_id": order_id,
        "amount": 250
    }


@app.get("/health")
async def health():
    return {"status": "order-service healthy"}