from fastapi import FastAPI

app = FastAPI(
    title="3D Model Generator API",
    description="Backend для построения 3D-моделей по фотографиям",
    version="1.0.0"
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }