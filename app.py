from fastapi import FastAPI

app = FastAPI(title="Kamal K8s Demo API")

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}! This is running in Kubernetes soon."}
