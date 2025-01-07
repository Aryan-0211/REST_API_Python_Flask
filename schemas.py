from marshmallow import Schema, fields

# Define the schema for Items
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)  # Used only when serializing output
    name = fields.Str(required=True)  # Mandatory in JSON payload
    price = fields.Float(required=True)  # Mandatory and must be a float


# Define the schema for Stores
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)  # Only for response
    name = fields.Str(required=True)  # Required during creation

class PlainTagSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
# Schema for Item updates (partial updates)
class ItemUpdateSchema(Schema):
    name = fields.Str()  # Optional field for name
    price = fields.Float()  # Optional field for price
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id =fields.Int(required = True, load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only =True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)
    
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only = True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only = True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)   