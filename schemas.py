"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# 3D Musical Band app schemas

class BandMember(BaseModel):
    """
    Band members collection
    Collection name: "bandmember"
    """
    name: str = Field(..., description="Member full name")
    role: str = Field(..., description="Primary role (e.g., Vocals, Guitar)")
    instrument: Optional[str] = Field(None, description="Main instrument")
    bio: Optional[str] = Field(None, description="Short biography")
    photo_url: Optional[HttpUrl] = Field(None, description="Profile photo URL")

class Song(BaseModel):
    """
    Songs collection
    Collection name: "song"
    """
    title: str
    duration_sec: Optional[int] = Field(None, ge=0)
    album_id: Optional[str] = Field(None, description="Related album ID as string")
    stream_url: Optional[HttpUrl] = Field(None, description="Public streamable MP3 URL")

class Album(BaseModel):
    """
    Albums collection
    Collection name: "album"
    """
    title: str
    year: Optional[int] = Field(None, ge=1900, le=2100)
    cover_url: Optional[HttpUrl] = None
    tracks: Optional[List[str]] = Field(default=None, description="List of song IDs as strings")

class BookingRequest(BaseModel):
    """
    Booking requests collection
    Collection name: "bookingrequest"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=2000)
    event_date: Optional[str] = Field(None, description="Requested event date (ISO string)")
    event_location: Optional[str] = None
