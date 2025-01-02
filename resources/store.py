import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

# Blueprint for store operations
blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        """
        Retrieve a store by its ID.
        """
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        """
        Delete a store by its ID.
        """
        try:
            del stores[store_id]
            return {"message": "Store Deleted"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        """
        Retrieve all stores.
        """
        return {"stores": list(stores.values())}

    def post(self):
        """
        Create a new store.
        """
        store_data = request.get_json()

        # Validate input data
        if "name" not in store_data:
            abort(400, message="Store name is required")

        # Check for duplicate store names
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")

        # Generate a unique ID for the store
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store, 201
