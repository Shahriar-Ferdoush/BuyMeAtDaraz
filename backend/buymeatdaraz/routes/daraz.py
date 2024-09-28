from typing import List

from fastapi import APIRouter, HTTPException
from routes import *
from utils.daraz import search_daraz, sync_daraz_scraper
from utils.database.sqlite import save_products_to_db

daraz_router = APIRouter(prefix="/daraz")


@daraz_router.post("/load_search_results")
def load_search_results(query: str):
    search_url = search_daraz(query)
    results = sync_daraz_scraper(search_url)
    
    save_products_to_db(results, "database/daraz.db")
    
    return {"message": "Search results loaded successfully!"}