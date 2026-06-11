from fastapi import FastAPI

from app.routes import router


app = FastAPI(title="Interactive Mailing System")
app.include_router(router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
