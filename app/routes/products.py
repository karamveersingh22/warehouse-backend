from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    get_all_products,
    get_product_by_sku,
    create_product,
    update_inventory
)
from app.utils.dependencies import get_current_user, require_manager
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
async def list_products(current_user: dict = Depends(get_current_user)):
    products = await get_all_products()
    return products


@router.get("/{sku_code}", response_model=ProductResponse)
async def get_product(sku_code: str, current_user: dict = Depends(get_current_user)):
    product = await get_product_by_sku(sku_code)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def add_product(data: ProductCreate, current_user: dict = Depends(require_manager)):
    product, error = await create_product(data)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return product


@router.put("/{sku_code}", response_model=ProductResponse)
async def update_product_inventory(
    sku_code: str,
    data: ProductUpdate,
    current_user: dict = Depends(require_manager)
):
    product, error = await update_inventory(sku_code, data)
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    return product
