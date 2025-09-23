from fastapi import FastAPI

app = FastAPI(title="CRUD API")

@app.get("/")
def root():
    return {"message": "API is running"}
