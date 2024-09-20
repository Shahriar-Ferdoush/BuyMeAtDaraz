from pydantic import BaseModel, HttpUrl, Field, field_validator


class DarazProduct(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    discount: float = Field(..., description="Discount percentage")
    rating: float = Field(..., description="Rating of the product")
    sold: int = Field(..., description="Number of items sold")
    image: str | None = Field(..., description="Image URL of the product")
    url: HttpUrl  = Field(..., description="Product URL")
    
    
    # Field validator for the image URL
    @field_validator("image", mode="before")
    def validate_image_url(cls, v):
        if v == "N/A" or not v.startswith("http"):
            # Set to None or a default image URL
            return None  # Or return a default image URL
        return v

    class Config:
        str_strip_whitespace = True  # Renamed config option in Pydantic V2
