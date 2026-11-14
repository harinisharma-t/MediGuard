from fastapi import FastAPI


app = FastAPI(
    title="MediGuard API",
    description=(
        "An educational medication interaction "
        "and allergy checking API."
    ),
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to MediGuard API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "MediGuard",
    }