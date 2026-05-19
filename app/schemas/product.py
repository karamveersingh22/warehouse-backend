from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    inventory: int

    @field_validator("inventory")
    @classmethod
    def inventory_non_negative(cls, v):
        if v < 0:
            raise ValueError("Inventory must be a non-negative integer")
        return v

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Category must not be empty")
        return v

    @field_validator("sku_code")
    @classmethod
    def sku_not_empty(cls, v):
        if not v.strip():
            raise ValueError("SKU code must not be empty")
        return v


class ProductUpdate(BaseModel):
    inventory: int

    @field_validator("inventory")
    @classmethod
    def inventory_non_negative(cls, v):
        if v < 0:
            raise ValueError("Inventory must be a non-negative integer")
        return v


class ProductResponse(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    inventory: int
    latest_updated_date: datetime
