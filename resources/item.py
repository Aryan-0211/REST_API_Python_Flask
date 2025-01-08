from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# Blueprint for item operations
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Fetch the item by ID
        item = ItemModel.query.get_or_404(item_id)
        return item  # Return the item serialized using the ItemSchema

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message = "Admin privilege required")
        # Fetch and delete the item
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # Fetch the item by ID or create a new one if it doesn't exist
        item = ItemModel.query.get(item_id)
        if item:
            # Update the existing item's attributes
            item.name = item_data.get("name", item.name)
            item.price = item_data.get("price", item.price)
        else:
            # Create a new item if it doesn't exist
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Item with the same name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))  # Returns a list of items
    def get(self):
        # Fetch and return all items
        return ItemModel.query.all()


    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # Create a new item
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An item with the same name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item, 201
