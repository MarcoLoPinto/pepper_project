import random
import json

class Command():
    def __init__(self, request=True, to_client_id="0", from_client_id="", data={}):
        self.request = request
        self.to_client_id = to_client_id
        self.from_client_id = from_client_id
        self.data = data
    
    def serialize(self):
        return {"request": self.request, "to_client_id": self.to_client_id, "from_client_id": self.from_client_id, "data":self.data}
    
    def toJson(self):
        j_obj = self.serialize()
        return json.dumps(j_obj)
    def __str__(self):
        return self.toJson()
    def __repr__(self):
        return self.toJson()
    
    @classmethod
    def fromJson(cls, json_str):
        j_obj = json.loads(json_str)
        return cls(request=j_obj["request"], to_client_id=j_obj["to_client_id"], from_client_id=j_obj["from_client_id"], data=j_obj["data"])

    def toBytes(self):
        return str(self).encode("utf-8")

    @classmethod
    def fromBytes(cls, bytes):
        json_str = bytes.decode("utf-8")
        return cls.fromJson(json_str)