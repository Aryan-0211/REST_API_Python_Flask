from db import db 

class ItemTags(db.Model):
    __tablename__ = "item_tags"
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))  

    # Optional: define relationships to make it easier to access related data
    item = db.relationship("ItemModel", backref="item_tags", lazy=True)
    tag = db.relationship("TagModel", backref="item_tags", lazy=True)
