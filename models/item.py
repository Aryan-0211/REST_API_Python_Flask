from db import db


class ItemModel(db.Model):
    __tablename__ = "items"  # Define the table name

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for unique item identification
    name = db.Column(db.String(80), unique=True, nullable=False)  # Item name must be unique and non-nullable
    price = db.Column(db.Float(precision=2), nullable=False)  # Price field, non-nullable with 2 decimal precision
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("stores.id"),  # Foreign key linking to the `stores` table
        nullable=False
    )

    # Define relationship with StoreModel
    store = db.relationship(
        "StoreModel",
        back_populates="items"  # Matches the `items` attribute in the `StoreModel`
    )
