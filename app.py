from flask import Flask, request

app = Flask(__name__)

# Data structure to hold stores and their items
stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

# Endpoint to get all stores
@app.get("/store")
def get_all_stores():
    """
    Retrieve all stores with their items.
    Example: GET http://127.0.0.1:5001/store
    """
    return {"stores": stores}

# Endpoint to create a new store
@app.post("/store")
def create_store():
    """
    Create a new store with an empty list of items.
    Example: POST http://127.0.0.1:5001/store
    Body: { "name": "New Store" }
    """
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

# Endpoint to add an item to a specific store
@app.post("/store/<string:name>/item")
def add_item_to_store(name):
    """
    Add an item to a store.
    Example: POST http://127.0.0.1:5001/store/My%20Store/item
    Body: { "name": "Table", "price": 45.99 }
    """
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404

# Endpoint to get a store by its name
@app.get("/store/<string:name>")
def get_store_by_name(name):
    """
    Retrieve a store by its name.
    Example: GET http://127.0.0.1:5001/store/My%20Store
    """
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

# Endpoint to get all items in a specific store
@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    """
    Retrieve all items in a store.
    Example: GET http://127.0.0.1:5001/store/My%20Store/item
    """
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404

if __name__ == "__main__":
    # Start the Flask app with debugging enabled
    app.run(debug=True, port=5001)  # Use port 5001
