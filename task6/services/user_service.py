from fastapi import FastAPI

app = FastAPI()


@app.get("/{item_id}")
async def get_user(item_id: int):
    return {
        "service": "user-service",
        "user_id": item_id,
        "name": "Arvind"
    }


@app.get("/health")
async def health():
    return {"status": "user-service healthy"}