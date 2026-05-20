from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductInDB(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    sizes: dict[str, int]
    latest_updated_date: datetime

    @property
    def total_inventory(self) -> int:
        return sum(self.sizes.values())
