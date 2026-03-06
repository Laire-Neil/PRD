from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class PrintingPrices:
    """Fixed pricing structure for printing services"""
    BLACK_AND_WHITE = 2.00  # PHP per page
    COLORED = 5.00  # PHP per page
    PHOTO_PAPER = 20.00  # PHP per page


class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    customer_name: str = Field(..., min_length=1, description="Name of the customer")
    paper_type: Literal["black_and_white", "colored", "photo_paper"] = Field(
        ..., description="Type of paper/printing"
    )
    pages: int = Field(..., gt=0, description="Number of pages to print")
    notes: str | None = Field(None, description="Optional notes for the order")


class Order(BaseModel):
    """Complete order schema with computed fields"""
    order_id: str
    customer_name: str
    paper_type: Literal["black_and_white", "colored", "photo_paper"]
    pages: int
    price_per_page: float
    total_cost: float
    notes: str | None = None
    created_at: datetime
    status: Literal["pending", "completed", "cancelled"] = "pending"


class OrderResponse(BaseModel):
    """Response schema for order operations"""
    success: bool
    message: str
    order: Order | None = None


class OrderListResponse(BaseModel):
    """Response schema for listing all orders"""
    success: bool
    total_orders: int
    total_revenue: float
    orders: list[Order]
