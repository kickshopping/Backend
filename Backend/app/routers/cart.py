from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.CartItemOut])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

@router.post("/", response_model=schemas.CartItemOut)
def add_to_cart(item: schemas.CartItemCreate, user_id: int, db: Session = Depends(get_db)):
    db_item = models.CartItem(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
