from fastapi import FastAPI

app = FastAPI(
    title="Volunteer Operations Platform",
    description="Backend API for volunteer workflow automation",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
