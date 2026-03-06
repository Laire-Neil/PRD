"""
Test script for the Campus Printing Shop API
Run this after starting the server to verify everything works
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def print_response(title, response):
    """Helper function to print responses nicely"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, default=str))


def test_api():
    """Test all API endpoints"""
    
    # 1. Test root endpoint
    print("\n🔍 Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    
    # 2. Test pricing endpoint
    print("\n💰 Testing Pricing Endpoint...")
    response = requests.get(f"{BASE_URL}/pricing")
    print_response("GET /pricing", response)
    
    # 3. Create first order (Black & White)
    print("\n📝 Creating Order 1 (Black & White)...")
    order1 = {
        "customer_name": "John Doe",
        "paper_type": "black_and_white",
        "pages": 10,
        "notes": "Thesis - Chapter 1"
    }
    response = requests.post(f"{BASE_URL}/orders", json=order1)
    print_response("POST /orders (Black & White)", response)
    order1_id = response.json()["order"]["order_id"]
    
    # 4. Create second order (Colored)
    print("\n📝 Creating Order 2 (Colored)...")
    order2 = {
        "customer_name": "Jane Smith",
        "paper_type": "colored",
        "pages": 5,
        "notes": "Presentation slides"
    }
    response = requests.post(f"{BASE_URL}/orders", json=order2)
    print_response("POST /orders (Colored)", response)
    order2_id = response.json()["order"]["order_id"]
    
    # 5. Create third order (Photo Paper)
    print("\n📝 Creating Order 3 (Photo Paper)...")
    order3 = {
        "customer_name": "Bob Johnson",
        "paper_type": "photo_paper",
        "pages": 3,
        "notes": "ID pictures"
    }
    response = requests.post(f"{BASE_URL}/orders", json=order3)
    print_response("POST /orders (Photo Paper)", response)
    
    # 6. Get all orders
    print("\n📋 Getting All Orders...")
    response = requests.get(f"{BASE_URL}/orders")
    print_response("GET /orders", response)
    
    # 7. Get specific order
    print(f"\n🔍 Getting Specific Order (ID: {order1_id})...")
    response = requests.get(f"{BASE_URL}/orders/{order1_id}")
    print_response(f"GET /orders/{order1_id}", response)
    
    # 8. Update order status
    print(f"\n✏️ Updating Order Status (ID: {order2_id})...")
    response = requests.put(
        f"{BASE_URL}/orders/{order2_id}/status",
        params={"status": "completed"}
    )
    print_response(f"PUT /orders/{order2_id}/status", response)
    
    # 9. Get all orders again to see the update
    print("\n📋 Getting All Orders (After Update)...")
    response = requests.get(f"{BASE_URL}/orders")
    data = response.json()
    print_response("GET /orders (Updated)", response)
    
    # Print summary
    print("\n" + "="*60)
    print("✅ TEST SUMMARY")
    print("="*60)
    print(f"Total Orders: {data['total_orders']}")
    print(f"Total Revenue: PHP {data['total_revenue']:.2f}")
    print("\nOrders:")
    for order in data['orders']:
        print(f"  - {order['customer_name']}: {order['pages']} pages "
              f"({order['paper_type']}) = PHP {order['total_cost']:.2f} "
              f"[{order['status']}]")
    print("="*60)


if __name__ == "__main__":
    print("🚀 Starting API Tests...")
    print(f"Testing server at: {BASE_URL}")
    print("\n⚠️  Make sure the server is running first!")
    print("   Run: python main.py")
    
    try:
        test_api()
        print("\n✅ All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("   Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
