from fastapi import FastAPI


app = FastAPI(title="Hello API")


@app.get("/")
async def hello() -> dict[str, str]:
    """Return a simple greeting."""
    return {"message": "Hello"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Report whether the API service is healthy."""
    return {"status": "ok"}
