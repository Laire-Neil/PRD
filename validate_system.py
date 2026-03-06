"""
Comprehensive validation tests for Campus Printing Shop API
Tests all functionality including edge cases and error handling
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'reset': '\033[0m'
}


def print_test(name, passed, details=""):
    """Print test result with color"""
    symbol = "✅" if passed else "❌"
    color = COLORS['green'] if passed else COLORS['red']
    print(f"{color}{symbol} {name}{COLORS['reset']}")
    if details:
        print(f"   {details}")


def test_suite():
    """Run all tests"""
    print(f"\n{COLORS['blue']}{'='*70}")
    print("🧪 CAMPUS PRINTING SHOP API - COMPREHENSIVE TESTS")
    print(f"{'='*70}{COLORS['reset']}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    print(f"{COLORS['yellow']}ℹ️ Running tests without clearing existing orders{COLORS['reset']}\n")
    
    # Test 1: Server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_test("Server is running", True)
            tests_passed += 1
        else:
            print_test("Server is running", False)
            tests_failed += 1
    except:
        print_test("Server is running", False, "Cannot connect to server")
        tests_failed += 1
        return
    
    # Test 2: Get pricing
    try:
        response = requests.get(f"{BASE_URL}/pricing")
        data = response.json()
        passed = (response.status_code == 200 and 
                 data['prices']['black_and_white']['price_per_page'] == 2.0 and
                 data['prices']['colored']['price_per_page'] == 5.0 and
                 data['prices']['photo_paper']['price_per_page'] == 20.0)
        print_test("Get pricing", passed, 
                  f"B&W: ₱2.00, Colored: ₱5.00, Photo: ₱20.00")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Get pricing", False, str(e))
        tests_failed += 1
    
    # Test 3: Create order - Black & White
    try:
        order_data = {
            "customer_name": "John Doe",
            "paper_type": "black_and_white",
            "pages": 10,
            "notes": "Test order"
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        data = response.json()
        passed = (response.status_code == 200 and 
                 data['order']['total_cost'] == 20.0 and
                 data['order']['pages'] == 10)
        order_id_1 = data['order']['order_id'] if passed else None
        print_test("Create order (Black & White)", passed, 
                  f"10 pages × ₱2.00 = ₱20.00")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Create order (Black & White)", False, str(e))
        tests_failed += 1
        order_id_1 = None
    
    # Test 4: Create order - Colored
    try:
        order_data = {
            "customer_name": "Jane Smith",
            "paper_type": "colored",
            "pages": 5
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        data = response.json()
        passed = (response.status_code == 200 and 
                 data['order']['total_cost'] == 25.0)
        order_id_2 = data['order']['order_id'] if passed else None
        print_test("Create order (Colored)", passed, 
                  f"5 pages × ₱5.00 = ₱25.00")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Create order (Colored)", False, str(e))
        tests_failed += 1
        order_id_2 = None
    
    # Test 5: Create order - Photo Paper
    try:
        order_data = {
            "customer_name": "Bob Johnson",
            "paper_type": "photo_paper",
            "pages": 3,
            "notes": "ID pictures"
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        data = response.json()
        passed = (response.status_code == 200 and 
                 data['order']['total_cost'] == 60.0)
        print_test("Create order (Photo Paper)", passed, 
                  f"3 pages × ₱20.00 = ₱60.00")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Create order (Photo Paper)", False, str(e))
        tests_failed += 1
    
    # Test 6: Get all orders
    try:
        response = requests.get(f"{BASE_URL}/orders")
        data = response.json()
        passed = (response.status_code == 200 and 
                 data['total_orders'] >= 3 and
                 data['total_revenue'] >= 105.0)
        print_test("Get all orders", passed, 
                  f"Orders: {data['total_orders']}, Total revenue: ₱{data['total_revenue']:.2f}")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Get all orders", False, str(e))
        tests_failed += 1
    
    # Test 7: Get specific order
    if order_id_1:
        try:
            response = requests.get(f"{BASE_URL}/orders/{order_id_1}")
            data = response.json()
            passed = (response.status_code == 200 and 
                     data['order']['order_id'] == order_id_1)
            print_test("Get specific order", passed, 
                      f"Order ID: {order_id_1}")
            if passed:
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print_test("Get specific order", False, str(e))
            tests_failed += 1
    
    # Test 8: Update order status
    if order_id_2:
        try:
            response = requests.put(
                f"{BASE_URL}/orders/{order_id_2}/status",
                params={"status": "completed"}
            )
            data = response.json()
            passed = (response.status_code == 200 and 
                     data['order']['status'] == 'completed')
            print_test("Update order status", passed, 
                      f"Status changed to 'completed'")
            if passed:
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print_test("Update order status", False, str(e))
            tests_failed += 1
    
    # Test 9: Validation - Invalid paper type
    try:
        order_data = {
            "customer_name": "Test User",
            "paper_type": "invalid_type",
            "pages": 5
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        passed = response.status_code == 422  # Should fail validation
        print_test("Validation: Invalid paper type", passed, 
                  "Correctly rejects invalid paper type")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Validation: Invalid paper type", False, str(e))
        tests_failed += 1
    
    # Test 10: Validation - Zero pages
    try:
        order_data = {
            "customer_name": "Test User",
            "paper_type": "black_and_white",
            "pages": 0
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        passed = response.status_code == 422  # Should fail validation
        print_test("Validation: Zero pages", passed, 
                  "Correctly rejects zero pages")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Validation: Zero pages", False, str(e))
        tests_failed += 1
    
    # Test 11: Validation - Negative pages
    try:
        order_data = {
            "customer_name": "Test User",
            "paper_type": "black_and_white",
            "pages": -5
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        passed = response.status_code == 422  # Should fail validation
        print_test("Validation: Negative pages", passed, 
                  "Correctly rejects negative pages")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Validation: Negative pages", False, str(e))
        tests_failed += 1
    
    # Test 12: Validation - Empty customer name
    try:
        order_data = {
            "customer_name": "",
            "paper_type": "black_and_white",
            "pages": 5
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        passed = response.status_code == 422  # Should fail validation
        print_test("Validation: Empty customer name", passed, 
                  "Correctly rejects empty customer name")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Validation: Empty customer name", False, str(e))
        tests_failed += 1
    
    # Test 13: Get non-existent order
    try:
        response = requests.get(f"{BASE_URL}/orders/nonexistent123")
        passed = response.status_code == 404  # Should return 404
        print_test("Get non-existent order", passed, 
                  "Correctly returns 404 for non-existent order")
        if passed:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print_test("Get non-existent order", False, str(e))
        tests_failed += 1
    
    # Test 14: Invalid status update
    if order_id_1:
        try:
            response = requests.put(
                f"{BASE_URL}/orders/{order_id_1}/status",
                params={"status": "invalid_status"}
            )
            passed = response.status_code == 400  # Should return 400
            print_test("Validation: Invalid status", passed, 
                      "Correctly rejects invalid status")
            if passed:
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print_test("Validation: Invalid status", False, str(e))
            tests_failed += 1
    
    # Test 15: Delete specific order
    if order_id_1:
        try:
            response = requests.delete(f"{BASE_URL}/orders/{order_id_1}")
            passed = response.status_code == 200
            print_test("Delete specific order", passed, 
                      f"Successfully deleted order {order_id_1}")
            if passed:
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print_test("Delete specific order", False, str(e))
            tests_failed += 1
    
    # Test 16: Verify order was deleted
    if order_id_1:
        try:
            response = requests.get(f"{BASE_URL}/orders/{order_id_1}")
            passed = response.status_code == 404
            print_test("Verify order deletion", passed, 
                      "Deleted order no longer exists")
            if passed:
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print_test("Verify order deletion", False, str(e))
            tests_failed += 1
    
    # Print summary
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{COLORS['blue']}{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}{COLORS['reset']}")
    print(f"{COLORS['green']}✅ Tests Passed: {tests_passed}{COLORS['reset']}")
    print(f"{COLORS['red']}❌ Tests Failed: {tests_failed}{COLORS['reset']}")
    print(f"📈 Pass Rate: {pass_rate:.1f}%")
    
    if tests_failed == 0:
        print(f"\n{COLORS['green']}🎉 ALL TESTS PASSED! System is fully functional.{COLORS['reset']}")
    else:
        print(f"\n{COLORS['yellow']}⚠️  Some tests failed. Please review the errors above.{COLORS['reset']}")
    
    print(f"{COLORS['blue']}{'='*70}{COLORS['reset']}\n")


if __name__ == "__main__":
    print(f"\n{COLORS['yellow']}⚠️  Make sure the server is running on http://127.0.0.1:8000")
    print(f"   Run: python main.py{COLORS['reset']}\n")
    
    try:
        test_suite()
    except requests.exceptions.ConnectionError:
        print(f"\n{COLORS['red']}❌ Error: Could not connect to the server.")
        print(f"   Make sure the server is running on http://127.0.0.1:8000{COLORS['reset']}\n")
    except Exception as e:
        print(f"\n{COLORS['red']}❌ Error: {e}{COLORS['reset']}\n")
