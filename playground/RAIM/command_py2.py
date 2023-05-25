import random
import json

class Command():
    def __init__(self, request=True, id=random.randint(1000,9999), data={}):
        self.request = request
        self.id = id
        self.data = data
    
    def toJson(self):
        j_obj = {"request": self.request, "id": self.id, "data":self.data}
        return json.dumps(j_obj)
    def __str__(self):
        return self.toJson()
    def __repr__(self):
        return self.toJson()
    
    def serialize(self):
        return {"request": self.request, "id": self.id, "data":self.data}
    
    @classmethod
    def fromJson(cls, json_str):
        j_obj = json.loads(json_str)
        return cls(j_obj["request"], j_obj["id"], j_obj["data"])

    def toBytes(self):
        return str(self).encode("utf-8")

    @classmethod
    def fromBytes(cls, bytes):
        json_str = bytes.decode("utf-8")
        return cls.fromJson(json_str)