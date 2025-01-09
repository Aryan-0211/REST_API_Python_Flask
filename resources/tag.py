from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        if not store.tags:
            abort(404, message="No tags found for the given store.")

        return store.tags.all()  # Assumes lazy="dynamic" in StoreModel.tags

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # Check if the store exists
        store = StoreModel.query.get_or_404(store_id)

        # Check for duplicate tag
        if TagModel.query.filter_by(store_id=store_id, name=tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in this store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Tag creation failed due to a data integrity error.")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An unexpected error occurred: {str(e)}")

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        # Check if the tag is already linked
        if tag in item.tags:
            abort(400, message="This tag is already associated with the item.")

        item.tags.append(tag)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while linking the tag: {str(e)}")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        # Ensure the tag is associated with the item
        if tag not in item.tags:
            abort(400, message="The tag is not associated with the specified item.")

        item.tags.remove(tag)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while unlinking the tag: {str(e)}")

        return {"message": "Tag removed from item.", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        # Check if the tag is associated with any items
        if tag.items:
            abort(400, message="Tag cannot be deleted because it is associated with items.")

        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while deleting the tag: {str(e)}")

        return {"message": "Tag deleted."}
