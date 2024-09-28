# main.py

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from routes.daraz import daraz_router

# Load environment variables from a .env file
load_dotenv()

# Set the API key in the environment if it's not already set
api_key = os.getenv("GOOGLE_API_TOKEN")
if api_key and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log", mode="a")],
)

logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()
app.include_router(daraz_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the pxlGPT API!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")
