from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Product
from schemas import ProductCreate, ProductUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {'mesg':'API is running'}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.post("/createProduct")
def create_products(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name = product.name,
        price = product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.put('/updateProduct/{product_id}')
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.price = product_data.price

    db.commit()
    db.refresh(product)

    return product

@app.delete("/deleteProduct/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code = 404,
            detail = "Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        'message':'Product deleted'
    }