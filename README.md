# Campus Printing Shop API

A simple backend API for managing printing orders at a campus printing shop. This system helps digitally record printing orders and automatically computes total costs.

## Features

- Accept printing orders
- Compute total cost automatically
- View all orders with total revenue
- Retrieve a specific order by ID
- Update order status (`pending`, `completed`, `cancelled`)
- Delete an order by ID
- In-memory storage only (no database)
- Fixed pricing structure

## Pricing Structure

| Paper Type | Price per Page |
|------------|---------------|
| Black & White | PHP 2.00 |
| Colored | PHP 5.00 |
| Photo Paper | PHP 20.00 |

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### 3. Access API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Get Pricing Information
```
GET /pricing
```

### Create New Order
```
POST /orders
```

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "paper_type": "black_and_white",
  "pages": 10,
  "notes": "Urgent"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order created successfully. Total: PHP 20.00",
  "order": {
    "order_id": "a1b2c3d4",
    "customer_name": "John Doe",
    "paper_type": "black_and_white",
    "pages": 10,
    "price_per_page": 2.0,
    "total_cost": 20.0,
    "notes": "Urgent",
    "created_at": "2026-03-03T10:30:00",
    "status": "pending"
  }
}
```

### Get All Orders
```
GET /orders
```

### Get Specific Order
```
GET /orders/{order_id}
```

### Update Order Status
```
PUT /orders/{order_id}/status?status=completed
```

Status options: `pending`, `completed`, `cancelled`

### Delete Order
```
DELETE /orders/{order_id}
```

## Usage Examples

### Using cURL

**Create an order:**
```bash
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Content-Type: application/json" \
  -d "{\"customer_name\":\"Jane Smith\",\"paper_type\":\"colored\",\"pages\":5,\"notes\":\"Double-sided\"}"
```

**Get all orders:**
```bash
curl http://127.0.0.1:8000/orders
```

**Get specific order:**
```bash
curl http://127.0.0.1:8000/orders/a1b2c3d4
```

### Using Python

```python
import requests

# Create order
order_data = {
    "customer_name": "Jane Smith",
    "paper_type": "colored",
    "pages": 5,
    "notes": "Double-sided"
}

response = requests.post("http://127.0.0.1:8000/orders", json=order_data)
print(response.json())

# Get all orders
response = requests.get("http://127.0.0.1:8000/orders")
print(response.json())
```

## Paper Type Options

- `black_and_white` - Black & White printing
- `colored` - Colored printing
- `photo_paper` - Photo paper printing

## Features Solving Client Problems

| Problem | Solution |
|---------|----------|
| Orders are lost | All orders stored digitally in memory with unique IDs |
| Orders are duplicated | Each order gets a unique identifier |
| Wrong computation | Automatic calculation based on fixed pricing |
| Hard to track daily orders | View all orders endpoint with total revenue |

## Notes

- This is an in-memory application - data is lost when the server restarts
- Designed for local use only
- No authentication implemented (can be added if needed)
- No database required - perfect for simple use cases

## MVP Scope

- Backend API only
- Local use only
- No database
- No authentication

## Future Enhancements (Optional)

- Add persistence with JSON/CSV file storage
- Add date filtering for daily/weekly reports
- Add customer history tracking
- Export orders to PDF/Excel
