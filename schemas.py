from marshmallow import Schema, fields

# Define the schema for Items
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)  # Used only when serializing output
    name = fields.Str(required=True)  # Mandatory in JSON payload
    price = fields.Float(required=True)  # Mandatory and must be a float
    store_id = fields.Str(required=True)  # Corrected: Uppercase 'Str'

# Schema for Item updates (partial updates)
class ItemUpdateSchema(Schema):
    name = fields.Str()  # Optional field for name
    price = fields.Float()  # Optional field for price

# Define the schema for Stores
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)  # Only for response
    name = fields.Str(required=True)  # Required during creation
