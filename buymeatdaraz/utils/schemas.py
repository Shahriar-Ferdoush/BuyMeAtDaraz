from langchain_core.pydantic_v1 import BaseModel, Field, validator


class DarazProduct(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    discount: float = Field(..., description="Discount percentage")
    rating: float = Field(..., description="Rating of the product")
    sold: int = Field(..., description="Number of items sold")
    image: str = Field(..., description="Image URL of the product")
    url: str = Field(..., description="Product URL")

    @validator("price", "discount", "rating", "sold")
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError("Value must be positive")
        return v

    @validator("image", "url")
    def validate_url(cls, v):
        if not v.startswith("http"):
            raise ValueError("Invalid URL format")
        return v
