from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"  # Define the table name

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for unique store identification
    name = db.Column(db.String(80), unique=True, nullable=False)  # Store name must be unique and non-nullable

    # Define relationship with ItemModel
    items = db.relationship(
        "ItemModel",
        back_populates="store",  # Matches the `store` attribute in the `ItemModel`
        lazy="dynamic",          # Enables dynamic query building for related items
        cascade="all, delete",   # Automatically handle deletion of related items when a store is deleted
    )

    tags = db.relationship(
        "TagModel",
        back_populates = "store",
        lazy = "dynamic"
    )