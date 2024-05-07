import json
 
def attempt_json_deserialize(data):
    try:
        json_object = json.loads(data)
    except (TypeError, json.decoder.JSONDecodeError): pass
    
    return json_object