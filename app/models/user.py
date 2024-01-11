from mongoengine import Document, EmailField, StringField, BooleanField

class User(Document):
    email = EmailField(required=True, unique=True)
    ordered = BooleanField(required=False)
    
    @classmethod
    def from_mongo(cls, data: dict, id_str=False):
        if not data:
            return data
        id = data.pop("_id", None) if not id_str else str(data.pop("_id", None))
        if "_cls" in data:
            data.pop("_cls", None)
        return cls(**dict(data, id=id))

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    meta = {
        "collection": "Users",
        "indexes": ["email"],
        "allow_inheritance": True,
        "index_cls": False,
    }