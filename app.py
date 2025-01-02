import uuid
from flask_smorest import abort
from flask import Flask, request
from db import items, stores

app = Flask(__name__)

# Endpoint to get all stores
@app.get("/store")
def get_all_stores():
    """
    Retrieve a list of all stores.
    Returns:
        dict: A dictionary containing all stores in the system.
    """
    return {"stores": list(stores.values())}

# Endpoint to create a new store
@app.post("/store")
def create_store():
    """
    Create a new store with the provided data.
    Request Body:
        - name (str): Name of the store (required).
    Returns:
        dict: The newly created store data.
    """
    store_data = request.get_json()

    # Validate input data
    if "name" not in store_data:
        abort(400, message="Store name is required")
    
        for store in store.values():
            if (store_data["name"] == store["name"]):
                abort(400, message="Store already exists.")

    # Generate a unique ID for the store
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201

# Endpoint to get an item by its ID
@app.delete("/store/<string:store_id>")

def delete_store(store_id):
    
    try:
        del stores[store_id]
        return {"message":"Store Deleted"}
    except KeyError:
        abort(404, message="Store not found")

    return stores[store_id]


# Endpoint to get a store by its ID

@app.get("/store/<string:store_id>")
def get_store_by_id(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")
        

# Endpoint to add an item to a specific store
@app.post("/item")
def create_item():
    """
    Add a new item to a specific store.
    Request Body:
        - name (str): Name of the item (required).
        - price (float): Price of the item (required).
        - store_id (str): ID of the store to add the item to (required).
    Returns:
        dict: The newly created item data.
    """
    item_data = request.get_json()

    # Validate input data
    if (
        "name" not in item_data 
        or "price" not in item_data 
        or "store_id" not in item_data
        ):
        abort(400, message="Item name, price, and store ID are required")
        
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item ["store_id"]
        ):
            abort(400, message="Item already exists.")

    # Check if the specified store exists
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    # Generate a unique ID for the item
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


# Endpoint to get an item by its ID
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message = "Item not found")

# Endpoint to get an item by its ID
@app.delete("/item/<string:item_id>")

def delete_item(item_id):
    
    try:
        del items[item_id]
        return {"message":"Item Deleted"}
    except KeyError:
        abort(404, message="Item not found")

    return items[item_id]

# Endpoint to update the item
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message= "Bad request. Ensure 'price', and 'name' are included in JSON payload.")
    try:
        item = items[item_id]
        item |= item_data   # |= new update operator in Dictionary
        
        return item
    except KeyError:
        abort(404,message="Item not found.")

# Endpoint to get all items
@app.get("/item")
def get_all_items():
    """
    Retrieve a list of all items.
    Returns:
        dict: A dictionary containing all items in the system.
    """
    return {"items": list(items.values())}


if __name__ == "__main__":
    # Start the Flask app with debugging enabled for development
    app.run(debug=True, port=5001)  # Use port 5001
