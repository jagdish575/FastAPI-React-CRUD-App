from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database_models import get_db, Product
from pydantic_model import ProductCreate, ProductResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace 3000 with your React app's port
    "http://localhost:8000",
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,  # Allows cookies and credentials
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def greet():
    return "Hellow world"


@app.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@app.get("/product/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/product", response_model=ProductResponse, status_code=201)  # 201 Created
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product_data.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.put("/product/{id}", response_model=ProductResponse)
def update_product(id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_data.name
    product.price = product_data.price

    db.commit()
    db.refresh(product)

    return product


@app.delete("/product/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

    return {"detail": "Product successfully deleted"}
