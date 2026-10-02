from pydantic import BaseModel, Field

class CartItem(BaseModel):
    product_id: str | None = None
    quantity: int = Field(gt=0)
    name: str | None = None
    unit_price: float | None = Field(default=None, gt=0)

class CreateSale(BaseModel):
    items: list[CartItem]
    customer_phone: str | None = None
    customer_name: str | None = None
    payment_method: str = "upi"

class StockChange(BaseModel):
    quantity: int = Field(gt=0)

class ProductCreate(BaseModel):
    barcode: str = Field(min_length=3)
    name: str = Field(min_length=2)
    category: str = "General"
    price: float = Field(gt=0)
    unit: str = "unit"
    initial_stock: int = Field(ge=0)

class ContactRequest(BaseModel):
    note: str = "Interested in discussing this stock opportunity."

class CustomerCreate(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    name: str = Field(min_length=2)

class Repayment(BaseModel):
    amount: float = Field(gt=0)
