from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def root(request:Request)->dict:
    return {
        "message": "Welcome To FastApi"
    }

if __name__ == "__main__":
    uvicorn.run("root:app", host="0.0.0.0", port=8080, reload=True)