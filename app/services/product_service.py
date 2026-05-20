from datetime import datetime
from app.database.mongodb import get_db
from app.schemas.product import ProductCreate, ProductUpdate


_ALLOWED_SIZES = {"S", "M", "L", "XL", "2XL", "3XL", "4XL"}


def _normalize_sizes(product: dict) -> dict[str, int]:
    sizes = product.get("sizes")
    if isinstance(sizes, dict):
        normalized: dict[str, int] = {}
        for key, value in sizes.items():
            if key not in _ALLOWED_SIZES:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                continue
            if value < 0:
                continue
            normalized[key] = value
        return normalized

    legacy_inventory = product.get("inventory")
    if isinstance(legacy_inventory, bool) or not isinstance(legacy_inventory, int):
        return {}
    if legacy_inventory < 0:
        return {}

    # Backward-compat: older documents stored a single flat inventory.
    # Treat it as size "M" so responses keep a consistent shape.
    return {"M": legacy_inventory}


def _with_total_inventory(product: dict) -> dict:
    sizes = _normalize_sizes(product)
    product["sizes"] = sizes
    product["total_inventory"] = sum(sizes.values())
    product.pop("inventory", None)
    return product


async def get_all_products():
    db = get_db()
    products = []
    async for product in db.products.find({}, {"_id": 0}):
        products.append(_with_total_inventory(product))
    return products


async def get_product_by_sku(sku_code: str):
    db = get_db()
    product = await db.products.find_one({"sku_code": sku_code}, {"_id": 0})
    if not product:
        return None
    return _with_total_inventory(product)


async def create_product(data: ProductCreate):
    db = get_db()

    existing = await db.products.find_one({"sku_code": data.sku_code})
    if existing:
        return None, "SKU code already exists"

    product_doc = {
        "sku_code": data.sku_code,
        "product_name": data.product_name,
        "category": data.category,
        "sizes": data.sizes,
        "latest_updated_date": datetime.utcnow()
    }

    await db.products.insert_one(product_doc)
    product_doc.pop("_id", None)
    return _with_total_inventory(product_doc), None


async def update_inventory(sku_code: str, data: ProductUpdate):
    db = get_db()

    existing = await db.products.find_one({"sku_code": sku_code})
    if not existing:
        return None, "Product not found"

    updated_date = datetime.utcnow()
    await db.products.update_one(
        {"sku_code": sku_code},
        {
            "$set": {"sizes": data.sizes, "latest_updated_date": updated_date},
            "$unset": {"inventory": ""},
        }
    )

    updated_product = await db.products.find_one({"sku_code": sku_code}, {"_id": 0})
    return _with_total_inventory(updated_product), None
