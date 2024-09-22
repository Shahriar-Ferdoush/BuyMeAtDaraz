from pydantic import BaseModel, Field, HttpUrl, field_validator


class DarazProduct(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    discount: float = Field(..., description="Discount percentage")
    rating: float = Field(..., description="Rating of the product")
    sold: int = Field(..., description="Number of items sold")
    url: str = Field(..., description="Product URL")

    @field_validator("url", mode="before")
    def validate_url(cls, v):
        if not v.startswith("http"):
            raise ValueError("URL must start with 'http'")
        return v

    class Config:
        str_strip_whitespace = True  # Renamed config option in Pydantic V2
