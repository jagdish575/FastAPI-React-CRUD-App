from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True
