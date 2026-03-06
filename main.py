from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Dict
import uuid

from models import (
    OrderCreate,
    Order,
    OrderResponse,
    OrderListResponse,
    PrintingPrices
)

# Initialize FastAPI app
app = FastAPI(
    title="Campus Printing Shop API",
    description="A simple backend API for managing printing orders",
    version="1.0.0"
)

# In-memory storage for orders (dictionary with order_id as key)
orders_db: Dict[str, Order] = {}


def compute_total_cost(paper_type: str, pages: int) -> tuple[float, float]:
    """
    Compute the total cost based on paper type and number of pages
    
    Returns:
        tuple: (price_per_page, total_cost)
    """
    price_map = {
        "black_and_white": PrintingPrices.BLACK_AND_WHITE,
        "colored": PrintingPrices.COLORED,
        "photo_paper": PrintingPrices.PHOTO_PAPER
    }
    
    price_per_page = price_map.get(paper_type, 0)
    total_cost = price_per_page * pages
    
    return price_per_page, total_cost


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Campus Printing Shop API",
        "endpoints": {
            "create_order": "POST /orders",
            "get_all_orders": "GET /orders",
            "get_order": "GET /orders/{order_id}",
            "update_order_status": "PUT /orders/{order_id}/status",
            "delete_order": "DELETE /orders/{order_id}",
            "pricing": "GET /pricing"
        }
    }


@app.get("/pricing")
def get_pricing():
    """Get the current pricing structure"""
    return {
        "currency": "PHP",
        "prices": {
            "black_and_white": {
                "price_per_page": PrintingPrices.BLACK_AND_WHITE,
                "description": "Black & White printing"
            },
            "colored": {
                "price_per_page": PrintingPrices.COLORED,
                "description": "Colored printing"
            },
            "photo_paper": {
                "price_per_page": PrintingPrices.PHOTO_PAPER,
                "description": "Photo paper printing"
            }
        }
    }


@app.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate):
    """
    Create a new printing order
    
    Automatically computes the total cost based on paper type and pages
    """
    # Generate unique order ID
    order_id = str(uuid.uuid4())[:8]
    
    # Compute pricing
    price_per_page, total_cost = compute_total_cost(
        order_data.paper_type, 
        order_data.pages
    )
    
    # Create order object
    new_order = Order(
        order_id=order_id,
        customer_name=order_data.customer_name,
        paper_type=order_data.paper_type,
        pages=order_data.pages,
        price_per_page=price_per_page,
        total_cost=total_cost,
        notes=order_data.notes,
        created_at=datetime.now(),
        status="pending"
    )
    
    # Store in memory
    orders_db[order_id] = new_order
    
    return OrderResponse(
        success=True,
        message=f"Order created successfully. Total: PHP {total_cost:.2f}",
        order=new_order
    )


@app.get("/orders", response_model=OrderListResponse)
def get_all_orders():
    """
    Retrieve all orders
    
    Useful for tracking daily orders and computing total revenue
    """
    all_orders = list(orders_db.values())
    total_revenue = sum(order.total_cost for order in all_orders)
    
    return OrderListResponse(
        success=True,
        total_orders=len(all_orders),
        total_revenue=total_revenue,
        orders=all_orders
    )


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    """
    Retrieve a specific order by ID
    """
    order = orders_db.get(order_id)
    
    if not order:
        raise HTTPException(
            status_code=404, 
            detail=f"Order {order_id} not found"
        )
    
    return OrderResponse(
        success=True,
        message="Order retrieved successfully",
        order=order
    )


@app.put("/orders/{order_id}/status")
def update_order_status(
    order_id: str, 
    status: str
):
    """
    Update the status of an order (pending, completed, cancelled)
    """
    if status not in ["pending", "completed", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be one of: pending, completed, cancelled"
        )
    
    order = orders_db.get(order_id)
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found"
        )
    
    # Update status
    order.status = status
    orders_db[order_id] = order
    
    return OrderResponse(
        success=True,
        message=f"Order status updated to {status}",
        order=order
    )


@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    """
    Delete an order (in case of mistakes)
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found"
        )
    
    deleted_order = orders_db.pop(order_id)
    
    return {
        "success": True,
        "message": f"Order {order_id} deleted successfully",
        "deleted_order": deleted_order
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
