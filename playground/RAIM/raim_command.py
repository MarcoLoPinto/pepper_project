import random
import json
import uuid

class Command():
    def __init__(self, request=False, id=str(uuid.uuid4()), to_client_id="0", from_client_id="", data={}, is_successful = True):
        self.request = request # If this is true, then the client will expect a response. If is false, this is either e standalone command or a response
        self.id = id
        self.to_client_id = to_client_id
        self.from_client_id = from_client_id
        self.data = data
        self.is_successful = is_successful # Refering to a response only. Indicates if the request is succesful and this is a ack response otherwise a nack
    
    def gen_response(self, is_successful = True, data = {}, to_client_id = None, from_client_id = None, request = False):
        return Command(
            request=request,
            id=self.id,
            to_client_id=to_client_id if to_client_id is not None else self.from_client_id,
            from_client_id=from_client_id if from_client_id is not None else self.to_client_id,
            data=data,
            is_successful=is_successful
        )

    def serialize(self):
        return {
            "request": self.request, 
            "id": self.id, 
            "to_client_id": self.to_client_id, 
            "from_client_id": self.from_client_id, 
            "data": self.data, 
            "is_successful": self.is_successful
        }
    
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
        return cls(
            request=j_obj["request"], 
            id=j_obj["id"], 
            to_client_id=j_obj["to_client_id"], 
            from_client_id=j_obj["from_client_id"], 
            data=j_obj["data"],
            is_successful=j_obj["is_successful"],
        )

    def toBytes(self):
        return str(self).encode("utf-8")

    @classmethod
    def fromBytes(cls, bytes):
        json_str = bytes.decode("utf-8")
        return cls.fromJson(json_str)