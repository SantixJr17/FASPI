from fastapi import FastAPI
app = FastAPI(title="Mi Primera API", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}

@app.get("/health")
def health_check():
    return {"status": "OK"}