import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

# Blueprint for item operations
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        """
        Retrieve an item by its ID.
        """
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        """
        Delete an item by its ID.
        """
        try:
            del items[item_id]
            return {"message": "Item Deleted"}
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        """
        Update an item's data by its ID.
        """
        item_data = request.get_json()

        # Validate input data
        if "price" not in item_data or "name" not in item_data:
            abort(
                400, 
                message="Bad request. Ensure 'price' and 'name' are included in JSON payload."
            )
        try:
            # Update existing item
            item = items[item_id]
            item |= item_data  # Use the update operator (Python 3.9+)
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        """
        Retrieve all items.
        """
        return {"items": list(items.values())}

    def post(self):
        """
        Create a new item.
        """
        item_data = request.get_json()

        # Validate input data
        if (
            "name" not in item_data
            or "price" not in item_data
            or "store_id" not in item_data
        ):
            abort(400, message="Item name, price, and store ID are required")

        # Check for duplicate item in the same store
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
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
