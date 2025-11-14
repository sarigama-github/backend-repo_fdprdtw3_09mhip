import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import BandMember, Song, Album, BookingRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "3D Musical Band API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the 3D Musical Band backend!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Public content endpoints
@app.get("/api/band/members")
def list_band_members(limit: int = 50):
    docs = get_documents("bandmember", limit=limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return {"items": docs}

@app.get("/api/music/albums")
def list_albums(limit: int = 50):
    docs = get_documents("album", limit=limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return {"items": docs}

@app.get("/api/music/songs")
def list_songs(limit: int = 100, album_id: Optional[str] = None):
    filt = {}
    if album_id:
        filt["album_id"] = album_id
    docs = get_documents("song", filter_dict=filt, limit=limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return {"items": docs}

# Booking endpoint
@app.post("/api/booking")
def create_booking(req: BookingRequest):
    inserted_id = create_document("bookingrequest", req)
    return {"status": "ok", "id": inserted_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
