from fastapi import Body, FastAPI,status,HTTPException,Response, Depends

app=FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
