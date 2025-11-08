from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = MongoClient(os.getenv("MONGO_URL"))
db = client.my_library
collection = db.books

class Book(BaseModel):
    title: str
    author: str
    year: int
    genre: str

@app.get("/books")
def get_books():
    return list(collection.find({}, {"_id": 1, "title": 1, "author": 1, "year": 1, "genre": 1}))

@app.post("/books")
def add_book(book: Book):
    result = collection.insert_one(book.dict())
    return {"id": str(result.inserted_id)}