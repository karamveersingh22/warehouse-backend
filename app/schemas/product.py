from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


ALLOWED_SIZES = {"S", "M", "L", "XL", "2XL", "3XL", "4XL"}


def _validate_sizes(sizes: dict[str, int]) -> dict[str, int]:
    if not sizes:
        raise ValueError("At least one size must be provided")

    invalid_keys = [key for key in sizes.keys() if key not in ALLOWED_SIZES]
    if invalid_keys:
        invalid_display = ", ".join(sorted(invalid_keys))
        allowed_display = ", ".join(["S", "M", "L", "XL", "2XL", "3XL", "4XL"])
        raise ValueError(f"Invalid size key(s): {invalid_display}. Allowed sizes: {allowed_display}")

    for size, qty in sizes.items():
        if isinstance(qty, bool) or not isinstance(qty, int):
            raise ValueError(f"Quantity for size '{size}' must be a non-negative integer")
        if qty < 0:
            raise ValueError(f"Quantity for size '{size}' must be a non-negative integer")

    return sizes


class ProductCreate(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    sizes: dict[str, int]

    @field_validator("sizes")
    @classmethod
    def sizes_valid(cls, v: dict[str, int]):
        return _validate_sizes(v)

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
    sizes: dict[str, int]

    @field_validator("sizes")
    @classmethod
    def sizes_valid(cls, v: dict[str, int]):
        return _validate_sizes(v)


class ProductResponse(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    sizes: dict[str, int]
    total_inventory: int
    latest_updated_date: datetime
