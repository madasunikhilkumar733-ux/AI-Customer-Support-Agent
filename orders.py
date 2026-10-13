orders = {
    "TS1001": {
        "status": "Shipped",
        "product": "Laptop",
        "delivery": "Expected tomorrow"
    },

    "TS1002": {
        "status": "Processing",
        "product": "Headphones",
        "delivery": "Expected in 3 days"
    },

    "TS1003": {
        "status": "Delivered",
        "product": "Smartphone",
        "delivery": "Delivered yesterday"
    }
}


def check_order(order_id):
    """check the status of an order  based on the order ID"""
    order=orders.get(order_id)
    if order is None:
        return f"the order ID {order_id} is not found. "
    return(
        f"Order ID: {order_id}\n"
        f"Product: {order['product']}\n"
        f"Status: {order['status']}\n"
        f"Delivery: {order['delivery']}"
    )
print(check_order("TS1001"))