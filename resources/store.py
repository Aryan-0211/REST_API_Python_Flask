from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import StoreModel
from schemas import StoreSchema

# Blueprint for store operations
blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # Retrieve store by ID or raise 404
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    def delete(self, store_id):
        # Retrieve and delete store by ID or raise 404
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully"}, 200


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """
        Retrieve all stores.
        """
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # Create a new store
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            # Handle uniqueness constraint violation (e.g., store name already exists)
            abort(400, message="A store with this name already exists.")
        except SQLAlchemyError:
            # Handle other SQLAlchemy errors
            abort(500, message="An error occurred while inserting the store.")

        return store, 201
