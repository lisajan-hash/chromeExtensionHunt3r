import json

def json_data(Success=None, Error=False, Message=None,Data=None):
    response = {
        "Success": Success if Success else None,
        "Message": Message if Message else None,
        "Error": Error if Error else None,
        "Data": Data if Data else None
    }
    return json.dumps(response)