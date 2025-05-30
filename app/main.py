import uvicorn

from api.load_app import app

if __name__ == "__main__":
    uvicorn.run(app, port=5000)