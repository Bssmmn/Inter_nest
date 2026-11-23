from fastapi import FastAPI

app = FastAPI(title='InterNest API')

@app.get('/health')
def health():
    return {'status':"ok"}