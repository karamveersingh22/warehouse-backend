from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductInDB(BaseModel):
    sku_code: str
    product_name: Optional[str] = None
    category: str
    inventory: int
    latest_updated_date: datetime
