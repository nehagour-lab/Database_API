from itertools import product

from fastapi import FastAPI, Depends, HTTPException
import database_models
from model import Product
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, name="Product A", price=10.99),
    Product(id=2, name="Product B", price=19.99),
    Product(id=3, name="Product C", price=5.99),
]

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database with sample products
def db_init(db: Session = Depends(get_db)):
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

# Call THE HOME function 
@app.get("/")
def read_root():
    return {"message": "Welcome to the Product API!"}

# list all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # Here you would typically query the database for products
    return db.query(database_models.Product).all()

# Get a product by ID
@app.get('/products/{product_id}')
def get_product_by_id (product_id: int, db: Session = Depends(get_db)):
    # Here you would typically query the database for a product by its ID
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post('/products')
def create_product(item: Product, db: Session = Depends(get_db)):
    db_item = database_models.Product(**item.model_dump())
    if db.query(database_models.Product).filter(database_models.Product.id == db_item.id).first():
        raise HTTPException(status_code=400, detail=f"Product with ID {db_item.id} already exists")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    raise  HTTPException(status_code=201, detail=f"Product with ID {db_item.id} created successfully")


@app.put('/products')
def update_products(id: int, item: Product, db: Session = Depends(get_db)):
    db_item = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")
    db_item.name = item.name
    db_item.price = item.price
    db.commit()
    raise HTTPException(status_code=200, detail=f" ID {id} updated successfully")


@app.delete('/products/{product_id}')
def delete_product(id: int, db: Session = Depends(get_db)):
    db_item = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_item)
    db.commit()
    raise HTTPException(status_code=200, detail=f" ID {id} deleted successfully")

   















